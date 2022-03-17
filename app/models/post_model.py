from os import getenv
from webbrowser import get
from pymongo import ReturnDocument
from pymongo import MongoClient
from pymongo import DESCENDING
from typing import Union

from app.utils import current_dt


client = MongoClient("mongodb://localhost:27017/")


db = client[getenv("DATABASE")]


class Post:
    def __init__(self, title: str, author: str, tags: list, content: str) -> None:
        self.id: int = self.new_id()
        self.created_at: str = current_dt()
        self.updated_at = None
        self.title = title
        self.author = author
        self.tags = tags
        self.content = content

    def create_new(self):
        db.posts.insert_one(self.__dict__)

    @staticmethod
    def get_all():
        return db.posts.find()

    @staticmethod
    def get_by_id(post_id: int):
        return db.posts.find_one({"id": post_id})

    @staticmethod
    def patch_by_id(post_id: int, update_content):
        return db.posts.find_one_and_update(
            {"id": post_id},
            {"$set": {**update_content, "updated_at": current_dt()}},
            return_document=ReturnDocument.AFTER,
        )

    @staticmethod
    def delete_by_id(post_id: int):
        return db.posts.find_one_and_delete({"id": post_id})

    @staticmethod
    def serialize(post: Union["Post", dict]):
        if type(post) is dict:
            del post["_id"]
        elif type(post) is Post:
            del post._id
        return post

    def new_id(self):
        last_post = list(db.posts.find().sort("id", DESCENDING).limit(1))

        if last_post:
            return last_post[0]["id"] + 1

        return 1

    def __delattr__(self, attribute):
        object.__delattr__(self, attribute)
