from flask import render_template, url_for, flash, redirect, request, Blueprint
from neolibrary.models import Book
from neolibrary import app, graph, bcrypt, book_covers, profile_pics
from neolibrary.main.utils import sidebar
from neolibrary.models import Book, Author, User
from neolibrary.books.utils import delete_book_cover
from flask_login import login_user, current_user, logout_user, login_required

main = Blueprint('main', __name__)



@main.route("/")
def home():
    books = Book().match(graph)
    return render_template('home.html', title='home',sidebar=sidebar(), books=books, image_folder=book_covers)

