from flask import render_template, Blueprint, request
from flask_login import current_user
from neolibrary.models import Book
from neolibrary import graph, book_covers
from neolibrary.main.utils import sidebar
from neolibrary.models import Book
from neolibrary.books.utils import match_book, data_to_obj_ls, iter_pages

main = Blueprint('main', __name__)
n_limit = Book.n_limit

@main.route("/")
def home():

    if current_user.is_authenticated:
        books_recommended = {}
        query = "match (b:Book)<-[:LIKED]-(:User)-[:LIKED]->(c:Book)<-[:LIKED]-(u:User)\
                    where u.username=$username and not (u)-->(b)\
                    return b, count(c)\
                    order by count(c) desc\
                    limit $limit"
        dt = graph.run(query, username=current_user.username, limit=n_limit)
        books_recommended["users"] = data_to_obj_ls(dt)

        query = "match (b:Book)<-[:TAGGED]-()-[:TAGGED]->(c:Book)<-[:LIKED]-(u:User)\
                    where u.username=$username and not (u)-->(b)\
                    return b, count(c)\
                    order by count(c) desc\
                    limit $limit"
        dt = graph.run(query, username=current_user.username, limit=n_limit)
        books_recommended["tags"] = data_to_obj_ls(dt)

        query = "match (b:Book)<-[:WROTE]-()-[:WROTE]->(c:Book)<-[:LIKED]-(u:User)\
                    where u.username=$username and not (u)-->(b)\
                    return b, count(c)\
                    order by count(c) desc\
                    limit $limit"
        dt = graph.run(query, username=current_user.username, limit=n_limit)
        books_recommended["authors"] = data_to_obj_ls(dt)

        return render_template('home.html', title='home',sidebar=sidebar(),
                                books_recommended=books_recommended, image_folder=book_covers)
    else:
        query = "match(b:Book) optional match (b)--(u:User) return b, count(u)\
                order by count(u) desc, b.title limit $limit"
        dt = graph.run(query,limit=n_limit).data()
        books = data_to_obj_ls(dt)

        return render_template('home.html', title='home',sidebar=sidebar(),
                                books=books, image_folder=book_covers)

@main.route("/recommended")
def recommended():
    if current_user.is_authenticated:
        pages = Book().pages_recommended(current_user.username)
    else:
        pages = Book().pages
    page = request.args.get('page',1, type=int)
    n_skip = abs(n_limit * (page - 1))
    # validate page number
    if page > pages:
        page = pages
    elif page < 1:
        page = 1

    query = "match(b:Book) optional match (b)--(u:User) return b, count(u)\
            order by count(u) desc, b.title skip $skip limit $limit"
    dt = graph.run(query, limit=n_limit, skip=n_skip).data()
    books = data_to_obj_ls(dt)

    page_ls = iter_pages(pages, page, 2, 1, 1, 3)

    return render_template('recommended.html', title='home', sidebar=sidebar(), current_page=page,
                            books=books, page_ls=page_ls, image_folder=book_covers)
