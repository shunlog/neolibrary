from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from neolibrary import graph, book_covers
from neolibrary.main.utils import sidebar
from neolibrary.models import Book, Author, User, Tag
from neolibrary.search.forms import SearchForm
from neolibrary.books.utils import data_to_obj_ls, iter_pages

search_bl = Blueprint('search', __name__)
n_limit = Book.n_limit

@search_bl.route("/search", methods=['GET', 'POST'])
def search():

    print("================================================")
    search = SearchForm(request.form)
    page = request.args.get('page',1, type=int)
    search_str = request.args.get('search', type=str)
    # match romanian chars

    if search_str and search_str != '':
        print(search_str)
        search_regexp = search_str.replace('a', '[aâă]').replace('A', '[AÂĂ]').replace('t', '[tț]').replace('T', '[TȚ]').replace('s', '[sș]').replace('S', '[SȘ]').replace('i', '[iȋ]').replace('I', '[IȊ]')
        search_regexp = "(?i).*" + search_str + ".*"
        print(search_regexp)


        query = "match (a:Author)-->(b:Book)\
            where b.title=~$search_str \
            return b union\
            match (b)<--(t:Tag)\
            where t.name=~$search_str \
            return b union\
            match (b)<--(a:Author)\
            where a.name=~$search_str \
            return distinct b"

        dt = graph.run(query,search_str=search_regexp).data()
        books = data_to_obj_ls(dt)

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
            return render_template('search.html', books=books, form=search, image_folder=book_covers,
                            title="Search", page_ls=page_ls,
                            search=search_str, current_page=page)
        else:
            flash("Couldn't find any books","danger")

    query = "match(b:Book) optional match (b)--(u:User) return b, count(u)\
            order by count(u) desc, b.title limit $limit"

    dt = graph.run(query,limit=n_limit).data()
    books = data_to_obj_ls(dt)
    return render_template('search.html', form=search, title="Search", search=search_str,
                        books=books, image_folder=book_covers)
