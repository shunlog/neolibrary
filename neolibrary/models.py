from datetime import datetime
from neolibrary import graph, login_manager
from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo
from flask_login import UserMixin
from itertools import groupby

@login_manager.user_loader
def load_user(username):
    return User.match(graph).where(username=username).first()

def __count__(obj):
    return

class Book(GraphObject):
    __primarykey__ = "title"

    n_limit = 8
    count = graph.run("match(n:Book) return count(n)").evaluate()
    pages = count // n_limit if count % n_limit == 0 else count // n_limit + 1


    def get_id(self):
        s = str(self.__node__)
        return s[s.find("_")+1:s.find(":")]

    def iter_pages(self,current_page, left_edge=1, right_edge=1, left_current=1, right_current=1):
        pages = self.pages
        ls = [i for i in range(1,self.pages+1)]
        ls2 = [i for i in range(current_page-left_current-1, current_page+right_current)]
        for i in range(left_edge,pages-right_edge):
            if i not in ls2:
                ls[i] = None
        ls = [i[0] for i in groupby(ls)]
        return ls

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

    books_read = RelatedTo(Book, "READ")
    books_liked = RelatedTo(Book, "LIKED")
    books_disliked = RelatedTo(Book, "DISLIKED")

    def get_id(self):
        s = str(self.__node__)
        return s[s.find("_")+1:s.find(":")]

    def get_username(self):
        return self.username.encode('utf-8')
