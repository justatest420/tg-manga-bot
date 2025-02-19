import os
from typing import Type, List, Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from bson.objectid import ObjectId
from tools import LanguageSingleton

from config import env_vars

class ChapterFile:
    def __init__(self, url: str, file_id: Optional[str] = None, file_unique_id: Optional[str] = None, cbz_id: Optional[str] = None, cbz_unique_id: Optional[str] = None):
        self.url = url
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.cbz_id = cbz_id
        self.cbz_unique_id = cbz_unique_id

class MangaOutput:
    def __init__(self, user_id: str, output: int):
        self.user_id = user_id
        self.output = output

class Subscription:
    def __init__(self, url: str, user_id: str):
        self.url = url
        self.user_id = user_id

class LastChapter:
    def __init__(self, url: str, chapter_url: str):
        self.url = url
        self.chapter_url = chapter_url

class MangaName:
    def __init__(self, url: str, name: str):
        self.url = url
        self.name = name

class DB():
    def __init__(self, dbname: str = env_vars['DB_URL'], dbname_str: str = 'mangadb'):
        self.client = MongoClient(dbname)
        self.db = self.client[dbname_str]
        self.chapter_files: Collection = self.db['chapter_files']
        self.manga_outputs: Collection = self.db['manga_outputs']
        self.subscriptions: Collection = self.db['subscriptions']
        self.last_chapters: Collection = self.db['last_chapters']
        self.manga_names: Collection = self.db['manga_names']

    async def connect(self):
        # MongoDB connection is established on initialization, so this method is not strictly necessary.
        pass

    async def add(self, other):
        if isinstance(other, ChapterFile):
            self.chapter_files.insert_one(other.__dict__)
        elif isinstance(other, MangaOutput):
            self.manga_outputs.insert_one(other.__dict__)
        elif isinstance(other, Subscription):
            self.subscriptions.insert_one(other.__dict__)
        elif isinstance(other, LastChapter):
            self.last_chapters.insert_one(other.__dict__)
        elif isinstance(other, MangaName):
            self.manga_names.insert_one(other.__dict__)

    async def get(self, obj_class: Type, query_value: str) -> Optional[object]:
        """Find a document in the database based on the class and a query value (e.g., URL or ID)."""
        
        # Determine the correct collection based on the class type
        collection = None
        if obj_class == ChapterFile:
            collection = self.chapter_files
        elif obj_class == MangaOutput:
            collection = self.manga_outputs
        elif obj_class == Subscription:
            collection = self.subscriptions
        elif obj_class == LastChapter:
            collection = self.last_chapters
        elif obj_class == MangaName:
            collection = self.manga_names
        else:
            raise ValueError("Unsupported object class")

        # Build the query based on the class and the provided query value
        query = {}
        
        if obj_class == ChapterFile:
            query = {"url": query_value}
        elif obj_class == MangaOutput:
            query = {"user_id": query_value}
        elif obj_class == Subscription:
            query = query_value
        elif obj_class == LastChapter:
            query = {"url": query_value}
        elif obj_class == MangaName:
            query = {"url": query_value}
        
        # Find the document in the collection
        result = collection.find_one(query)
        
        if result:
            del result['_id']
            return obj_class(**result)
        else:
            return None
    
    async def get_all(self, obj_class: Type[object]) -> List[object]:
        """Retrieve all documents from the specified collection and convert them to class instances."""
        
        collection = None
        if obj_class == ChapterFile:
            collection = self.chapter_files
        elif obj_class == MangaOutput:
            collection = self.manga_outputs
        elif obj_class == Subscription:
            collection = self.subscriptions
        elif obj_class == LastChapter:
            collection = self.last_chapters
        elif obj_class == MangaName:
            collection = self.manga_names
        else:
            raise ValueError("Unsupported object class")
        
        cursor = collection.find()
        
        result = []
        for document in cursor:
            del document['_id']
            result.append(obj_class(**document))
        
        return result


    async def erase(self, other):
        if isinstance(other, ChapterFile):
            self.chapter_files.delete_one(other.__dict__)
        elif isinstance(other, MangaOutput):
            self.manga_outputs.delete_one(other.__dict__)
        elif isinstance(other, Subscription):
            self.subscriptions.delete_one(other.__dict__)
        elif isinstance(other, LastChapter):
            self.last_chapters.delete_one(other.__dict__)
        elif isinstance(other, MangaName):
            self.manga_names.delete_one(other.__dict__)

    async def get_chapter_file_by_id(self, id: str):
        return self.chapter_files.find_one({
            "$or": [
                {"file_unique_id": id},
                {"cbz_unique_id": id},
            ]
        })

    async def get_subs(self, user_id: str, filters=None) -> List[MangaName]:
        query = {"user_id": user_id}
        if filters:
            query["$or"] = [{"name": {"$regex": f".*{filter_}.*", "$options": "i"}} for filter_ in filters]
        subscriptions = self.subscriptions.find(query)
        manga_names = []
        for sub in subscriptions:
            manga_name = self.manga_names.find_one({"url": sub["url"]})
            if manga_name:
                del manga_name['_id']
                manga_names.append(MangaName(**manga_name))
        return manga_names

    async def erase_subs(self, user_id: str) -> int:
        result = self.subscriptions.delete_many({"user_id": user_id})
        return result.deleted_count
