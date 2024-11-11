import os, requests, pymongo
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
        pass

    def add_item(self, title):
        """
        Adds a new item with the specified title to the database.

        Args:
            title: The title of the item.
        """
        pass       

    def update_item(self, id):
        """
        Updates an existing item in the db.

        Args:
            id: The ID of the item to update.
        """
        pass

    def remove_item(self, id):
        """
        Removes an item from the db. If no existing item matches the ID of the specified item, nothing is removed.

        Args:
            id: Id of the item to remove.
        """
        pass

