from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from neolibrary import graph, book_covers
from neolibrary.main.utils import sidebar
from neolibrary.models import Book, Author, User, Tag
from neolibrary.search.forms import SearchForm
from neolibrary.books.utils import match_list, iter_pages

search_bl = Blueprint('search', __name__)
n_limit = Book.n_limit

@search_bl.route("/search", methods=['GET', 'POST'])
def search():

    search = SearchForm(request.form)
    page = request.args.get('page',1, type=int)
    search_str = request.args.get('search', type=str)
    # match romanian chars

    if search_str and search_str != '':
        search_str = search_str.replace('a', '[aâă]').replace('A', '[AÂĂ]').replace('t', '[tț]').replace('T', '[TȚ]').replace('s', '[sș]').replace('S', '[SȘ]').replace('i', '[iȋ]').replace('I', '[IȊ]')
        print(search_str)

        query = "match (a:Author)-->(b:Book)\
            where b.title=~'(?i).*" + search_str + ".*' \
            return b union\
            match (b)<--(t:Tag)\
            where t.name=~'(?i).*" + search_str + ".*' \
            return b union\
            match (b)<--(a:Author)\
            where a.name=~'(?i).*" + search_str + ".*' \
            return distinct b"

        books = match_list(query, 'b')
        count = len(books)
        pages = count // n_limit if count % n_limit == 0 else count // n_limit + 1
        if page > pages:
            page = pages
        elif page < 1:
            page = 1
        page_ls = iter_pages(pages, page, 2, 1, 1, 3)

        n_skip = abs(n_limit * (page - 1))
        books = books[n_skip:n_skip+n_limit]

        return render_template('search.html', books=books, form=search, image_folder=book_covers,
                            title="Search", page_ls=page_ls,
                            search=search_str, current_page=page)

    pages = Book().pages
    if page > pages:
        page = pages
    elif page < 1:
        page = 1

    n_skip = abs(n_limit * (page - 1))
    books = Book().match(graph).limit(n_limit).skip(n_skip)
    page_ls = iter_pages(pages, page, 2, 1, 1, 3)
    return render_template('search.html', form=search, title="Search", search=search_str,
                        books=books, image_folder=book_covers, page_ls=page_ls,
                        current_page=page)
