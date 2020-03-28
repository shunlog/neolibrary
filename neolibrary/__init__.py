from flask import Flask
from py2neo import Graph
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

graph = Graph(password="adminadmin")
bcrypt = Bcrypt(app)
book_covers='static/book_covers/'
profile_pics='static/profile_pics/'

login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from neolibrary.main.routes import main
from neolibrary.users.routes import users
from neolibrary.books.routes import books
from neolibrary.authors.routes import authors
from neolibrary.search.routes import search_bl

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(books)
app.register_blueprint(authors)
app.register_blueprint(search_bl)
