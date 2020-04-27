from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, jsonify
from flask_login import current_user, login_required
from werkzeug.datastructures import MultiDict
from neolibrary import graph, book_covers, book_covers_path
from neolibrary.models import Book, Author, User, Tag
from neolibrary.search.forms import SearchForm
from neolibrary.search.utils import str_to_regexp
from neolibrary.books.utils import iter_pages

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

    if search.data['select'] == "All":
        page = request.args.get('page',1, type=int)
        # match romanian chars

        if search_str and search_str != '':

            search_regexp = str_to_regexp(search_str)

            query = "match (b:Book)\
                where b.title=~$search_regexp \
                return b union\
                match (b)<--(t:Tag)\
                where t.name=~$search_regexp \
                return b union\
                match (b)<--(a:Author)\
                where a.name=~$search_regexp \
                return distinct b"

            dt = graph.run(query,search_regexp=search_regexp)
            books = [Book.wrap(node[0]) for node in dt]

            count = len(books)
            pages = count // n_limit if count % n_limit == 0 else count // n_limit + 1
            if page > pages:
                page = pages
            elif page < 1:
                page = 1
            page_ls = iter_pages(pages, page, 2, 1, 1, 3)

            n_skip = abs(n_limit * (page - 1))
            books = books[n_skip:n_skip+n_limit]

            if books:
                return render_template('search.html', books=books, form=search, book_covers_path=book_covers_path,
                                title="Search", page_ls=page_ls, select = select_str,
                                search=search_str, current_page=page)
            else:
                flash("Couldn't find any books","danger")

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
