from flask import render_template, Blueprint, request
from flask_login import current_user
from neolibrary.models import Book
from neolibrary import graph, book_covers
from neolibrary.main.utils import init_sidebar
from neolibrary.models import Book
from neolibrary.books.utils import match_book, iter_pages

main = Blueprint('main', __name__)
n_limit = Book.n_limit

@main.route("/")
def home():
    if current_user.is_authenticated:
        sidebar = init_sidebar(current_user)

        books_recommended = {}
        query = "match (b:Book)<-[:LIKED]-(:User)-[:LIKED]->(c:Book)<-[:LIKED]-(u:User)\
                    where u.username=$username and not (u)-->(b)\
                    return b, count(c)\
                    order by count(c) desc\
                    limit $limit"
        dt = graph.run(query, username=current_user.username, limit=n_limit)
        books_recommended["users"] = [Book.wrap(node) for node,c in dt]

        query = "match (b:Book)<-[:TAGGED]-()-[:TAGGED]->(c:Book)<-[:LIKED]-(u:User)\
                    where u.username=$username and not (u)-->(b)\
                    return b, count(c)\
                    order by count(c) desc\
                    limit $limit"
        dt = graph.run(query, username=current_user.username, limit=n_limit)
        books_recommended["tags"] = [Book.wrap(node) for node,c in dt]

        query = "match (b:Book)<-[:WROTE]-()-[:WROTE]->(c:Book)<-[:LIKED]-(u:User)\
                    where u.username=$username and not (u)-->(b)\
                    return b, count(c)\
                    order by count(c) desc\
                    limit $limit"
        dt = graph.run(query, username=current_user.username, limit=n_limit)
        books_recommended["authors"] = [Book.wrap(node) for node,c in dt]

        return render_template('home.html', title='Home',sidebar=sidebar,
                                books_recommended=books_recommended, book_covers=book_covers)
    else:
        sidebar = init_sidebar(None)
        query = "match(b:Book) optional match (b)--(u:User) return b, count(u)\
                order by count(u) desc, b.title limit $limit"
        dt = graph.run(query,limit=n_limit)
        books = [Book.wrap(node[0]) for node,c in dt]

        return render_template('home.html', title='Home',sidebar=sidebar,
                                books=books, book_covers=book_covers)

