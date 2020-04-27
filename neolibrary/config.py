import os

class Config:
        GRAPHENEDB_URL = os.getenv("GRAPHENEDB_BOLT_URL")
        GRAPHENEDB_USER = os.getenv("GRAPHENEDB_BOLT_USER")
        GRAPHENEDB_PASSWORD = os.getenv('GRAPHENEDB_BOLT_PASSWORD')
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        SECRET_KEY = os.getenv('SECRET_KEY')
        BOOK_COVERS = os.getenv('BOOK_COVERS')
        PROFILE_PICS = os.getenv('PROFILE_PICS')
        FTP_USER = os.getenv("FTP_USER")
        FTP_PASSWORD = os.getenv("FTP_PASSWORD")
        HOST_IP = os.getenv("HOST_IP")
        HOST_DIR = os.getenv("HOST_DIR")
