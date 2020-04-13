from flask import render_template, Blueprint, request
from neolibrary.models import Book
from neolibrary import graph, book_covers
from neolibrary.main.utils import sidebar
from neolibrary.models import Book

main = Blueprint('main', __name__)
n_limit = Book.n_limit

@main.route("/")
def home():
    pages = Book().pages
    page = request.args.get('page',1, type=int)
    # validate page number
    if page > pages:
        page = pages
    elif page < 1:
        page = 1

    n_skip = abs(n_limit * (page - 1))
    books = Book().match(graph).skip(n_skip).limit(n_limit)

    page_ls = Book().iter_pages(page, left_edge=2, right_edge=1, left_current=1, right_current=3)

    return render_template('home.html', title='home',sidebar=sidebar(),
                           books=books, current_page = page, page_ls = page_ls,
                           image_folder=book_covers)
