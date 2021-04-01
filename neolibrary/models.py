from datetime import datetime

from flask import current_app as app
from neolibrary import graph, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo
from flask_login import UserMixin

@login_manager.user_loader
def load_user(username):
    return User.match(graph).where(username=username).first()


class Book(GraphObject):
    __primarykey__ = "name"

    count = graph.run("match(n:Book) return count(n)").evaluate()

    def get_id(self):
        s = str(self.__node__)
        return s[s.find("_")+1:s.find(":")]

    name = Property()
    title = Property()
    image_file = Property()
    image_url = Property()
    small_image_url = Property()

    authors = RelatedFrom("Author", "WROTE")
    tags = RelatedFrom("Tag", "TAGS")
    users_read = RelatedFrom("User", "READ")
    users_liked = RelatedFrom("User", "LIKED")
    users_disliked = RelatedFrom("User", "DISLIKED")


class Author(GraphObject):
    __primarykey__ = "name"

    name = Property()
    books = RelatedTo("Book", "WROTE")

    def book_count(self):
        count = graph.run("match (b:Book)<-[:WROTE]-(a:Author) where a.name='"+
                          self.name+"' return count(b)").evaluate()
        return count

    def get_id(self):
        s = str(self.__node__)
        return s[s.find("_")+1:s.find(":")]

class Tag(GraphObject):
    __primarykey__ = "name"

    name = Property()
    books = RelatedTo("Book", "TAGS")

    def book_count(self):
        count = graph.run("match (b:Book)<-[:TAGS]-(t:Tag) where t.name='"+
                          self.name+"' return count(b)").evaluate()
        return count

    def get_id(self):
        s = str(self.__node__)
        return s[s.find("_")+1:s.find(":")]

class User(GraphObject, UserMixin):
    __primarykey__ = "username"

    username = Property()
    password = Property()
    email = Property()
    image_file = Property()
    is_admin = Property()
    count = graph.run("match (u:User) return count(u)").evaluate()

    books_read = RelatedTo(Book, "READ")
    books_liked = RelatedTo(Book, "LIKED")
    books_disliked = RelatedTo(Book, "DISLIKED")

    def get_node_id(self):
        s = str(self.__node__)
        id = s[s.find("_")+1:s.find(":")]
        print("ID:",id)
        return id

    def get_id(self):
        return self.username.encode('utf-8')

