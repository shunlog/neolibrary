from neolibrary import app, graph
from neolibrary.models import Book, Author, User, Tag

def sidebar():
    sidebar = {}
    authors = Author().match(graph).limit(5)
    books = Book().match(graph).limit(5)
    tags = Tag().match(graph).limit(5)
    sidebar['authors'] = authors
    sidebar['books'] = books
    sidebar['tags'] = tags
    return sidebar
