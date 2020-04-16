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
    __primarykey__ = "title"

    n_limit = 8
    count = graph.run("match(n:Book) return count(n)").evaluate()
    pages = count // n_limit if count % n_limit == 0 else count // n_limit + 1

    def pages_recommended(self, username):
        count_recommended = graph.run('''match (b1:Book)<-[:WROTE]-(:Author)-[:WROTE]->(b_liked:Book)<-[:LIKED]-(u:User{username:"'''+username+'''"})
                            where not (u)-[]->(b1)
                            return count(b1)''').evaluate()
        pages = count_recommended // self.n_limit if\
                count_recommended % self.n_limit == 0 else\
                count_recommended // self.n_limit + 1
        return pages

    def get_id(self):
        s = str(self.__node__)
        return s[s.find("_")+1:s.find(":")]


    title = Property()
    image_file = Property()

    authors = RelatedFrom("Author", "WROTE")
    tags = RelatedFrom("Tag", "TAGGED")
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
    books = RelatedTo("Book", "TAGGED")

    def book_count(self):
        count = graph.run("match (b:Book)<-[:TAGGED]-(t:Tag) where t.name='"+
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

