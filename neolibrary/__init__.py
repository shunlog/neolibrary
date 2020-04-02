from flask import Flask
from py2neo import Graph
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from neolibrary.config import Config

app = Flask(__name__)
app.config.from_object(Config)

graph = Graph(password=Config.DB_PASSWORD)
bcrypt = Bcrypt(app)

book_covers = Config.book_covers
profile_pics = Config.profile_pics

login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from neolibrary.main.routes import main
from neolibrary.users.routes import users
from neolibrary.books.routes import books
from neolibrary.authors.routes import authors
from neolibrary.tags.routes import tags
from neolibrary.search.routes import search_bl

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(books)
app.register_blueprint(authors)
app.register_blueprint(tags)
app.register_blueprint(search_bl)
