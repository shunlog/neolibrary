from neolibrary import app, graph
from neolibrary.models import Book, Author, User

def sidebar():
    sidebar = {}
    authors = Author().match(graph).limit(5)
    books = Book().match(graph).limit(5)
    sidebar['authors'] = authors
    sidebar['books'] = books
    return sidebar
