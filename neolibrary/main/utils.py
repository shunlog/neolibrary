from flask import current_app as app
from neolibrary import  graph
from neolibrary.models import Book, Author, User, Tag

def init_sidebar(user):
    sidebar = {}
    if user:
        authors = Author().match(graph).limit(5)
        books = Book().match(graph).limit(5)
        tags = Tag().match(graph).limit(5)
        return sidebar
    else:
        authors = Author().match(graph).limit(5)
        books = Book().match(graph).limit(5)
        tags = Tag().match(graph).limit(5)
    sidebar['authors'] = authors
    sidebar['books'] = books
    sidebar['tags'] = tags
    return sidebar
