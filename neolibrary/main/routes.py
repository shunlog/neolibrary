from flask import render_template, Blueprint
from neolibrary.models import Book
from neolibrary import graph, book_covers
from neolibrary.main.utils import sidebar
from neolibrary.models import Book

main = Blueprint('main', __name__)

@main.route("/")
def home():
    books = Book().match(graph)
    return render_template('home.html', title='home',sidebar=sidebar(), books=books, image_folder=book_covers)

