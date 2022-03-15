from datetime import datetime as dt
from os import getenv
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")


# db_name
db = client[getenv("DATABASE")]


class Post:
    def __init__(self, title, author, tags, content) -> None:
        self.id = 1
        self.created_at = dt.now().strftime("%d/%m/%Y %H:%M:%S")
        self.updated_at = None
        self.title = title
        self.author = author
        self.tags = tags
        self.content = content
