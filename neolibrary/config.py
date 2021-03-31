import os

class Config:
    # local database
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    SECRET_KEY = os.getenv('SECRET_KEY')
    # directory path that contains the folders indicated
    # in book_COVERS and PROFILE_PICS
    HOST_DIR = os.getenv("HOST_DIR")
    # folder path from static that stores pics
    PROFILE_PICS = os.getenv('PROFILE_PICS')
    BOOK_COVERS = os.getenv('BOOK_COVERS')

    # ftp to server that hosts pics
    FTP_USER = os.getenv("FTP_USER")
    FTP_PASSWORD = os.getenv("FTP_PASSWORD")
    HOST_IP = os.getenv("HOST_IP")
    # link to the site
    BOOK_COVERS_PATH = os.getenv('BOOK_COVERS_PATH')
    PROFILE_PICS_PATH = os.getenv('PROFILE_PICS_PATH')
