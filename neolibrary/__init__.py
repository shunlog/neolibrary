from flask import Flask
from py2neo import Graph
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from neolibrary.config import Config


graph = Graph(password=Config.DB_PASSWORD)
bcrypt = Bcrypt()

book_covers = Config.BOOK_COVERS
profile_pics = Config.PROFILE_PICS
ftp_user = Config.FTP_USER
ftp_password = Config.FTP_PASSWORD
host_ip = Config.HOST_IP
host_dir = Config.HOST_DIR
book_covers_path = Config.BOOK_COVERS_PATH
profile_pics_path = Config.PROFILE_PICS_PATH

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
    from neolibrary.test.routes import test

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(books)
    app.register_blueprint(authors)
    app.register_blueprint(tags)
    app.register_blueprint(search_bl)
    app.register_blueprint(test)

    return app
