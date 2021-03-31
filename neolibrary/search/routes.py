from math import ceil
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, jsonify
from flask_login import current_user, login_required
from werkzeug.datastructures import MultiDict
from neolibrary import graph, book_covers, book_covers_path
from neolibrary.models import Book, Author, User, Tag
from neolibrary.config import Config
from neolibrary.search.forms import SearchForm
from neolibrary.search.utils import str_to_regexp
from neolibrary.books.utils import iter_pages, validate_page_number

search_bl = Blueprint('search', __name__)
n_limit = Book.n_limit


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


    if search.data['select'] == "All":
        if search_str and search_str != '':
            search_regexp = str_to_regexp(search_str)
            query = "match (b:Book) where b.title=~$search_regexp return b union\
                match (b)<--(t:Tag) where t.name=~$search_regexp return b union\
                match (b)<--(a:Author) where a.name=~$search_regexp return distinct b"
            dt = graph.run(query,search_regexp=search_regexp)
            books = [Book.wrap(node[0]) for node in dt]

            count = len(books)
            pages = count // n_limit if count % n_limit == 0 else count // n_limit + 1
            page = validate_page_number(page, pages)
            n_skip = abs(n_limit * (page - 1))
            page_ls = iter_pages(pages, page)

            books = books[n_skip:n_skip+n_limit]
            if books:
                return render_template('search.html', books=books, form=search, book_covers_path=book_covers_path,
                                title="Search", page_ls=page_ls, select = select_str,
                                search=search_str, current_page=page)
            else:
                flash("Couldn't find any books matching that query","danger")

    elif search.data['select'] == "Author":
        if search_str and search_str != '':
            search_regexp = str_to_regexp(search_str)
            lim = Config.AUTHORS_LIMIT

            query = "match (:Book)<--(a:Author) where a.name=~$search \
            with distinct a return count(a)"
            dt = graph.run(query, search=search_regexp)

            count = dt.evaluate()
            pages = ceil(count/lim)
            page = validate_page_number(page, pages)
            n_skip = abs(n_limit * (page - 1))
            page_ls = iter_pages(pages, page)

            query_authors = "match (b:Book)<--(a:Author) where a.name=~$search \
            return a, count(b) order by count(b) desc skip $skip limit $limit"
            dt = graph.run(query_authors, search=search_regexp,
                           limit=lim, skip=(page-1)*lim)
            authors = [Author.wrap(node[0]) for node in dt]
            return render_template('search.html', form=search, title="Search", search=search_str,
                                   authors=authors, page_ls=page_ls, current_page=page,
                                   select=select_str)

    elif search.data['select'] == "Tag":
        if search_str and search_str != '':
            search_regexp = str_to_regexp(search_str)
            query = "match (b:Book)<--(t:Tag) where t.name=~$search_regexp \
            return t, count(b) order by count(b) desc"
            dt = graph.run(query, search_regexp=search_regexp)
            tags = [Tag.wrap(node[0]) for node in dt]
            return render_template('search.html', form=search, title="Search", search=search_str,
                                   tags=tags)

    query = "match(b:Book) optional match (b)--(u:User) return b, count(u)\
            order by count(u) desc, b.title limit $limit"

    dt = graph.run(query,limit=n_limit)
    books = [Book.wrap(node[0]) for node in dt]
    return render_template('search.html', form=search, title="Search", search=search_str,
                           books=books, book_covers_path=book_covers_path)

@search_bl.route('/autocomplete', methods=['GET','POST'])
def autocomplete():
    if request.method == "POST":
        search_str_tags = request.form['search_tags']
        search_str_authors = request.form['search_authors']

        search_regexp_tags = str_to_regexp(search_str_tags)
        search_regexp_authors = str_to_regexp(search_str_authors)

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
