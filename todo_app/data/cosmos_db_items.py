import os, pymongo
from bson import ObjectId
from todo_app.data.classes.Item import Item

class CosmosDbService():
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv("COSMOS_DB_CONNECTION_STRING"))
        self.db = self.client[os.getenv("COSMOS_DB_DATABASE_NAME")]
        self.collection = self.db[os.getenv("COSMOS_DB_COLLECTION_NAME")]
        
    def get_items(self):
        """
        Fetches all items from the database.

        Returns:
            list: The list of items.
        """
        items = self.collection.find()
        return [Item.from_cosmos_db_item(item) for item in items]

    def add_item(self, title):
        """
        Adds a new item with the specified title to the database.

        Args:
            title: The title of the item.
        """
        self.collection.insert_one({"item": title, "isDone": False})       

    def update_item(self, id):
        """
        Updates an existing item in the db.

        Args:
            id: The ID of the item to update.
        """
        item = self.collection.find_one({"_id": ObjectId(id)})
        isDone = False if item["isDone"] else True
        self.collection.update_one({"_id": ObjectId(id)}, {"$set": {"isDone": isDone}})

    def remove_item(self, id):
        """
        Removes an item from the db. If no existing item matches the ID of the specified item, nothing is removed.

        Args:
            id: Id of the item to remove.
        """
        self.collection.delete_one({"_id": ObjectId(id)})

