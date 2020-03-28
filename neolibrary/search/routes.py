from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from neolibrary import app, graph
from neolibrary.main.utils import sidebar
from neolibrary.models import Book, Author, User

search_bl = Blueprint('search', __name__)

@search_bl.route("/search")
def search():
    books = Book().match(graph)
    return render_template('search.html', title='search', sidebar=sidebar())
