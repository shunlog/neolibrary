from datetime import datetime
from neolibrary import graph, login_manager
from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo
from flask_login import UserMixin

@login_manager.user_loader
def load_user(username):
    return User.match(graph).where(username=username).first()


class Book(GraphObject):
    __primarykey__ = "title"

    def get_id(self):
        s = str(self.__node__)
        return s[s.find("_")+1:s.find(":")]

    def count_authors(self):
        count = 0
        for a in self.authors:
            count += 1
        return count

    title = Property()
    image_file = Property()

    authors = RelatedFrom("Author", "WROTE")
    users_read = RelatedFrom("User", "READ")
    users_liked = RelatedFrom("User", "LIKED")
    users_disliked = RelatedFrom("User", "DISLIKED")


class Author(GraphObject):
    __primarykey__ = "name"

    def get_id(self):
        s = str(self.__node__)
        return s[s.find("_")+1:s.find(":")]

    def count_books(self):
        count = 0
        for b in self.books:
            count += 1
        return count

    name = Property()
    books = RelatedTo("Book", "WROTE")


class User(GraphObject, UserMixin):
    __primarykey__ = "username"

    username = Property()
    password = Property()
    email = Property()
    image_file = Property()

    books_read = RelatedTo(Book, "READ")
    books_liked = RelatedTo(Book, "LIKED")
    books_disliked = RelatedTo(Book, "DISLIKED")

    def get_node_id(self):
        s = str(self.__node__)
        return s[s.find("_")+1:s.find(":")]

    def get_id(self):
        return self.username.encode('utf-8')
