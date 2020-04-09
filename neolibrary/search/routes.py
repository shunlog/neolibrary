from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from neolibrary import graph, book_covers
from neolibrary.main.utils import sidebar
from neolibrary.models import Book, Author, User, Tag
from neolibrary.search.forms import SearchForm

search_bl = Blueprint('search', __name__)

@search_bl.route("/search", methods=['GET', 'POST'])
def search():

    search = SearchForm(request.form)

    if request.method == 'POST':
        search_str = search.data['search']

        if search.data['select'] == "Book":
            if search.data['search'] == '':
                books = Book().match(graph)
            else:
                books = Book().match(graph).where("_.title =~ '(?i).*{0}.*'".format(search_str))
            if not books:
                flash('No results found!')
            return render_template('search.html', books=books, form=search, image_folder=book_covers, title="Search")

        elif search.data['select'] == "Author":
            if search.data['search'] == '':
                authors = Author().match(graph)
            else:
                authors = Author().match(graph).where("_.name =~ '(?i).*{0}.*'".format(search_str))
            if not authors:
                flash('No results found!')
            return render_template('search.html', authors=authors, form=search, image_folder=book_covers, title="Search")

        elif search.data['select'] == "Tag":
            if search.data['search'] == '':
                tags = Tag().match(graph)
                print(search.data['select'])
            else:
                tags = Tag().match(graph).where("_.name =~ '(?i).*{0}.*'".format(search_str))
            if not tags:
                flash('No results found!')
            return render_template('search.html', tags=tags, form=search, image_folder=book_covers, title="Search")
    return render_template('search.html', form=search, title="Search")
