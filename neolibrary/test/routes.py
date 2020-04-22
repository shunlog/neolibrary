from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from neolibrary import graph, book_covers
from neolibrary.models import Book, Author, User, Tag
from neolibrary.search.utils import str_to_regexp
from neolibrary.books.utils import iter_pages

test = Blueprint('test', __name__)

@test.route("/test", methods=['GET', 'POST'])
def testing():
    print("______________________DATA1_____________________________")
    dt = graph.run("match (a)-[:WROTE]->(b2)<-[:LIKED]-(u2)-[:LIKED]\
                    -(b)<-[:LIKED]-(u:User{username:'admin'})\
                    where not (a)-->()<-[:LIKED]-(u)\
                    return a")
    ls = [Author.wrap(node[0]) for node in dt]
    print(ls)

    print("_____________________DATA2______________________________")
    dt2 = graph.run("match(b:Book) optional match (b)--(u:User)\
            return b, count(u) order by count(u) desc, b.title limit 6")
    ls = [Book.wrap(b) for b,c in dt2]
    print(ls)

    print("_____________________DATA3______________________________")
    query = "match (b:Book)<-[:WROTE]-()-[:WROTE]->(c:Book)<-[:LIKED]-(u:User)\
                where u.username=$username and not (u)-->(b)\
                return b, count(c)\
                order by count(c) desc\
                limit $limit"
    dt = graph.run(query, username='admin', limit=4)
    ls = [Book.wrap(node) for node,c in dt]
    print(ls)

    return render_template('test.html')
