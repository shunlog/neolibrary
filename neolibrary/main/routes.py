from flask import render_template, Blueprint, request, url_for
from flask_login import current_user
from neolibrary.models import Book
from neolibrary import graph, book_covers, book_covers_path, Config
from neolibrary.main.utils import init_sidebar
from neolibrary.models import Book
from neolibrary.books.utils import match_book, iter_pages

main = Blueprint('main', __name__)


@main.route("/")
def home():
    global book_covers_path
    if not book_covers_path:
        book_covers_path = url_for('static', filename=book_covers)
    if current_user.is_authenticated:
        sidebar = init_sidebar(current_user)

        books_recommended = {}
        query = "match (b:Book)<-[:LIKED]-(:User)-[:LIKED]->(c:Book)<-[:LIKED]-(u:User)\
                    where u.username=$username and not (u)-->(b)\
                    return b, count(c)\
                    order by count(c) desc\
                    limit $limit"
        dt = graph.run(query, username=current_user.username, limit=Config.BOOKS_LIMIT_HOME)
        books_recommended["users"] = [Book.wrap(node) for node,c in dt]

        query = "match (b:Book)<-[:TAGS]-()-[:TAGS]->(c:Book)<-[:LIKED]-(u:User)\
                    where u.username=$username and not (u)-->(b)\
                    return b, count(c)\
                    order by count(c) desc\
                    limit $limit"
        dt = graph.run(query, username=current_user.username, limit=Config.BOOKS_LIMIT_HOME)
        books_recommended["tags"] = [Book.wrap(node) for node,c in dt]

        query = "match (b:Book)<-[:WROTE]-()-[:WROTE]->(c:Book)<-[:LIKED]-(u:User)\
                    where u.username=$username and not (u)-->(b)\
                    return b, count(c)\
                    order by count(c) desc\
                    limit $limit"
        dt = graph.run(query, username=current_user.username, limit=Config.BOOKS_LIMIT_HOME)
        books_recommended["authors"] = [Book.wrap(node) for node,c in dt]


        return render_template('home.html', title='Home',sidebar=sidebar,
                                books_recommended=books_recommended, book_covers_path=book_covers_path)
    else:
        sidebar = init_sidebar(None)
        query = "match(b:Book) optional match (b)--(u:User) return b, count(u)\
                order by count(u) desc, b.title limit $limit"
        dt = graph.run(query,limit=Config.BOOKS_LIMIT_HOME)
        books = [Book.wrap(node) for node,c in dt]

        return render_template('home.html', title='Home',sidebar=sidebar,
                                books=books, book_covers_path=book_covers_path)
