from math import ceil
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, jsonify
from flask_login import current_user, login_required
from werkzeug.datastructures import MultiDict
from neolibrary import graph, book_covers, book_covers_path
from neolibrary.models import Book, Author, User, Tag
from neolibrary.config import Config
from neolibrary.search.forms import SearchForm
from neolibrary.search.utils import string_to_regexp
from neolibrary.books.utils import iter_pages, validate_page_number

search_bl = Blueprint('search', __name__)


@search_bl.route("/search", methods=['GET', 'POST'])
def search():
    global book_covers_path
    if not book_covers_path:
        book_covers_path = url_for('static', filename=book_covers)
    search_str = request.args.get('search', type=str)
    select_str = request.args.get('select')
    search = SearchForm()
    search.search.data = search_str
    search.select.data = select_str
    page = request.args.get('page',1, type=int)


    def url_for_page(page_num):
        return url_for('search.search', page=page_num,
                       search=search_str, select=select_str)

    if search.data['select'] == "Book":
        if search_str and search_str != '':
            search_regexp = string_to_regexp(search_str)
            lim = Config.BOOKS_LIMIT

            query = "match (b:Book) where b.name=~$search return count(b)"
            dt = graph.run(query, search=search_regexp)
            count = dt.evaluate()
            print(count)

            pages = ceil(count/lim)
            page = validate_page_number(page, pages)
            page_ls = iter_pages(pages, page)

            query = "match (b:Book) where b.name=~$search return b\
                skip $skip limit $limit"
            dt = graph.run(query, search=search_regexp, limit=lim,
                           skip=(page-1)*lim)
            books = [Book.wrap(node[0]) for node in dt]

            if not books:
                flash("Couldn't find any books matching that query","danger")
            return render_template('search.html', books=books, form=search,
                                   book_covers_path=book_covers_path, title="Search",
                                   page_ls=page_ls, current_page=page,
                                   url_for_page=url_for_page)

    elif search.data['select'] == "Author":
        if search_str and search_str != '':
            search_regexp = string_to_regexp(search_str)
            lim = Config.AUTHORS_LIMIT

            query = "match (:Book)<--(a:Author) where a.name=~$search \
            with distinct a return count(a)"
            dt = graph.run(query, search=search_regexp)
            count = dt.evaluate()

            pages = ceil(count/lim)
            page = validate_page_number(page, pages)
            page_ls = iter_pages(pages, page)

            query_authors = "match (b:Book)<--(a:Author) where a.name=~$search \
            return a, count(b) order by count(b) desc skip $skip limit $limit"
            dt = graph.run(query_authors, search=search_regexp,
                           limit=lim, skip=(page-1)*lim)
            authors = [Author.wrap(node[0]) for node in dt]
            if not authors:
                flash("Couldn't find any authors matching that query","danger")
            return render_template('search.html', form=search, title="Search",
                                   authors=authors, page_ls=page_ls, current_page=page,
                                   url_for_page=url_for_page)

    elif search.data['select'] == "Tag":
        if search_str and search_str != '':
            search_regexp = string_to_regexp(search_str)
            lim = Config.AUTHORS_LIMIT

            query = "match (:Book)<--(a:Tag) where a.name=~$search \
            with distinct a return count(a)"
            dt = graph.run(query, search=search_regexp)
            count = dt.evaluate()
            pages = ceil(count/lim)
            page = validate_page_number(page, pages)
            page_ls = iter_pages(pages, page)

            query = "match (b:Book)<--(t:Tag) where t.name=~$search_regexp \
            return t, count(b) order by count(b) desc skip $skip limit $limit"
            dt = graph.run(query, search_regexp=search_regexp,
                           limit=lim, skip=(page-1)*lim)
            tags = [Tag.wrap(node[0]) for node in dt]
            if not tags:
                flash("Couldn't find any tags matching that query","danger")
            return render_template('search.html', form=search, title="Search",
                                   tags=tags, page_ls=page_ls, current_page=page,
                                   url_for_page=url_for_page)

    query = "match(b:Book) optional match (b)--(u:User) return b, count(u)\
            order by count(u) desc, b.title limit $limit"

    dt = graph.run(query,limit=Config.BOOKS_LIMIT)
    books = [Book.wrap(node[0]) for node in dt]
    return render_template('search.html', form=search, title="Search", search=search_str,
                           books=books, book_covers_path=book_covers_path)

@search_bl.route('/autocomplete', methods=['GET','POST'])
def autocomplete():
    if request.method == "POST":
        search_str_tags = request.form['search_tags']
        search_str_authors = request.form['search_authors']

        search_regexp_tags = string_to_regexp(search_str_tags)
        search_regexp_authors = string_to_regexp(search_str_authors)

        tags = Tag().match(graph).where('_.name =~ "{}"'.format(search_regexp_tags))
        tags_ls = []
        for t in tags:
            tags_ls.append(t.name)

        authors = Author().match(graph).where('_.name =~ "{}"'.format(search_regexp_authors))
        authors_ls = []
        for a in authors:
            authors_ls.append(a.name)

        obj = {'tags':tags_ls, 'authors': authors_ls}
        return jsonify(json_list=obj)
