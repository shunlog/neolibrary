from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from neolibrary import graph, book_covers
from neolibrary.models import Book, Author, User, Tag
from neolibrary.search.utils import string_to_regexp, run_advanced_search
from neolibrary.books.utils import iter_pages

test = Blueprint('test', __name__)

@test.route("/test", methods=['GET', 'POST'])
def testing():

    ls = [["Book", "A.*"],["Tag", 'business'],["Tag",'academic']]

    dt = run_advanced_search(graph, ls)
    for i in dt:
        print(Book.wrap(i[0]))


    return "Successful"
    return render_template('test.html')
