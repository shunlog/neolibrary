from flask import current_app as app
from neolibrary import  graph
from neolibrary.models import Book, Author, User, Tag

limit = 5

def init_sidebar(user):
    sidebar = {}
    if user:
        dt_authors = graph.run("match (a)-[:WROTE]->(b2)<-[:LIKED]-(u2)-[:LIKED]\
                -(b)<-[:LIKED]-(u:User{username: $username})\
                where not (a)-->()<-[:LIKED]-(u) return distinct a limit $limit",
                limit=limit, username=user.username)
        authors = [Author.wrap(node[0]) for node in dt_authors]

        dt_tags = graph.run("match (t)-[:TAGS]->(b2)<-[:LIKED]-(u2)-[:LIKED]\
                -(b)<-[:LIKED]-(u:User{username: $username})\
                where not (t)-->()<-[:LIKED]-(u)\
                return distinct t limit $limit",
                limit=limit, username=user.username)
        tags = [Tag.wrap(node[0]) for node in dt_tags]
    else:
        authors = Author().match(graph).limit(5)
        tags = Tag().match(graph).limit(5)
    sidebar['authors'] = authors
    sidebar['tags'] = tags
    return sidebar
