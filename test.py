from time import time
from flask import render_template, url_for, flash, redirect
from py2neo import Graph, Relationship, NodeMatcher
from neolibrary import app, graph, bcrypt
from neolibrary.models import Book, Author, User 
from neolibrary.books.routes import match_node, match_list_of_nodes
from PIL import Image

book = match_node("create (b:Book) return b", 'b')
# dt = graph.run("create (b:Book) return b").data()
# b = dt[0]['b']
# book = Book().wrap(b)

print(book)


'''
Two ways of paginating the result
1) Run query
2) Use limit() and skip() methods 
'''
# s = 0
# l = 2

## Way 1
# while True:
    # print("-------------------")
    # ls = match_list_of_nodes("match (b:Book) return b skip {} limit {}".format(s,l), 'b')
    # if not ls:
        # break
    # s += l
    # for n in ls:
        # print(n.title)

## Way 2
# while True:
    # print("-------------------")
    # books = Book().match(graph).limit(l).skip(s)
    # if not books.first():
        # break
    # s += l
    # for b in books:
        # print(b)






'''
This test shows us that the difference in running the command 
and then getting the object by 

node = graph.run(query).data()[0]['name_of_return_var']
and obj = Obj().wrap(node)

is even a bit faster than using the ogm and getting the obj by

.match(graph, "title").first()
'''
# start = time()

# for i in range(n):
    # dt = graph.run("match (b:Book) where b.title = 'Poezii' return b")
    # node = dt.data()[0]['b']
    # book = Book().wrap(node)

# end = time()
# print(end - start)


# start = time()

# for i in range(n):
    # book = Book().match(graph, "Poezii").first()

# end = time()
# print(end - start)

'''
As expected, there is no much difference between running a function and getting
the obj directly so a function would come in handy
'''

# def match_node(query, node):
    # try:
        # dt = graph.run(query)
        # node = dt.data()[0][node]
        # book = Book().wrap(node)
        # return book
    # except:
        # print("Error running query!")

# n = 10000

# start = time()

# for i in range(n):
    # dt = graph.run("match (b:Book) where b.title = 'Poezii' return b")
    # node = dt.data()[0]['b']
    # book = Book().wrap(node)

# end = time()
# print(end - start)


# start = time()

# for i in range(n):
    # book = match_node("match (b:Book) where b.title = 'Poezii' return b", 'b')

# end = time()
# print(end - start)
