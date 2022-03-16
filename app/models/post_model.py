from pymongo import MongoClient
from pymongo import ReturnDocument

from app.helpers import current_dt, serialize

client = MongoClient("mongodb://localhost:27017/")

# db_name
db = client["kenzie"]


class Post:
    def __init__(self, title: str, author: str, tags: list, content: str) -> None:
        self.id: int = Post.new_id()
        self.created_at: str = current_dt()
        self.updated_at = None
        self.title = title
        self.author = author
        self.tags = tags
        self.content = content

    def create_new(self):
        db.posts.insert_one(self.__dict__)
        return Post.get_by_id(self.id)

    @staticmethod
    def get_all():
        posts_list = db.posts.find()
        return posts_list

    @staticmethod
    def get_by_id(post_id: int):
        curr_post = db.posts.find_one({"id": post_id})
        return serialize(curr_post)

    @staticmethod
    def patch_by_id(post_id: int, update_content):
        updated = db.posts.find_one_and_update(
            {"id": post_id},
            {"$set": {**update_content, "updated_at": current_dt()}},
            return_document=ReturnDocument.AFTER,
        )
        return serialize(updated)

    @classmethod
    def delete_by_id(cls, post_id: int):
        curr_post = cls.get_by_id(post_id)
        db.posts.delete_one(curr_post)
        return curr_post

    @classmethod
    def new_id(cls):
        all_posts = cls.get_all()
        new_id = len(list(all_posts)) + 1
        return new_id
