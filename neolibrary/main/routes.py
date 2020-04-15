from flask import render_template, Blueprint, request
from flask_login import current_user
from neolibrary.models import Book
from neolibrary import graph, book_covers
from neolibrary.main.utils import sidebar
from neolibrary.models import Book
from neolibrary.books.utils import match_book, match_list

main = Blueprint('main', __name__)
n_limit = Book.n_limit

@main.route("/")
def home():

    if current_user.is_authenticated:
        pages = Book().pages_recommended(current_user.username)
    else:
        pages = Book().pages

    page = request.args.get('page',1, type=int)
    # validate page number
    if page > pages:
        page = pages
    elif page < 1:
        page = 1

    n_skip = abs(n_limit * (page - 1))

    if current_user.is_authenticated:
        books_recommended = {}
        books_recommended["users"] = match_list("match (b:Book)<-[:LIKED]-(:User)-[:LIKED]->(c:Book)<-[:LIKED]-(u:User{username:'"+
                    current_user.username+"'})\
                    where not (u)-->(b)\
                    return b, count(c)\
                    order by count(c) desc\
                    limit "+str(n_limit), 'b')
        books_recommended["tags"] = match_list("match (b:Book)<-[:TAGGED]-()-[:TAGGED]->(c:Book)<-[:LIKED]-(u:User{username:'"+
                    current_user.username+"'})\
                    where not (u)-->(b)\
                    return b, count(c)\
                    order by count(c) desc\
                    limit "+str(n_limit), 'b')
        books_recommended["authors"] = match_list("match (b:Book)<-[:WROTE]-()-[:WROTE]->(c:Book)<-[:LIKED]-(u:User{username:'"+
                    current_user.username+"'})\
                    where not (u)-->(b)\
                    return b, count(c)\
                    order by count(c) desc\
                    limit "+str(n_limit), 'b')
        #page_ls = Book().iter_pages_recommended(page, 2, 1, 1, 3, current_user.username)

        return render_template('home.html', title='home',sidebar=sidebar(),
                                books_recommended=books_recommended, image_folder=book_covers)
    else:
        books = Book().match(graph).limit(n_limit).skip(n_skip)
        page_ls = Book().iter_pages(page, 2, 1, 1, 3)

        return render_template('home.html', title='home',sidebar=sidebar(),
                                books=books, current_page = page, page_ls = page_ls,
                                image_folder=book_covers)
