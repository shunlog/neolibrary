import os

class Config:
        GRAPHENEDB_URL = os.getenv("GRAPHENEDB_BOLT_URL")
        GRAPHENEDB_USER = os.getenv("GRAPHENEDB_BOLT_USER")
        GRAPHENEDB_PASSWORD = os.getenv('GRAPHENEDB_BOLT_PASSWORD')
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        SECRET_KEY = os.getenv('SECRET_KEY')
        BOOK_COVERS = os.getenv('BOOK_COVERS')
        PROFILE_PICS = os.getenv('PROFILE_PICS')

