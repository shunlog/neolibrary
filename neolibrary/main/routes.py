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
                                books_recommended=books_recommended, book_covers=book_covers)
    else:
        query = "match(b:Book) optional match (b)--(u:User) return b, count(u)\
                order by count(u) desc, b.title limit $limit"
        dt = graph.run(query,limit=n_limit).data()
        books = data_to_obj_ls(dt)

        return render_template('home.html', title='home',sidebar=sidebar(),
                                books=books, book_covers=book_covers)

