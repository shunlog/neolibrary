from flask import Flask
from py2neo import Graph
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from neolibrary.config import Config
import os


graphenedb_url = Config.GRAPHENEDB_URL
graphenedb_user = Config.GRAPHENEDB_USER
graphenedb_pass = Config.GRAPHENEDB_PASSWORD
if graphenedb_url:
        graph = Graph(graphenedb_url, user=graphenedb_user, password=graphenedb_pass, bolt = True, secure = True, http_port = 24789, https_port = 24780)
else:
        graph = Graph(password=Config.DB_PASSWORD)

bcrypt = Bcrypt()

book_covers = Config.BOOK_COVERS
profile_pics = Config.PROFILE_PICS

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
        app = Flask(__name__)
        app.config.from_object(Config)

        bcrypt.init_app(app)
        login_manager.init_app(app)

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

        return app
