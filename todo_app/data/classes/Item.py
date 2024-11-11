import os
from enum import Enum
 
class ItemStatus(Enum):
    TODO = 0
    DONE = 1

class Item:
    def __init__(self, id, name, status = ItemStatus.TODO):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def from_cosmos_db_item(cls, item):
        status = ItemStatus.DONE if item['isDone'] else ItemStatus.TODO
        return cls(item['_id'], item['item'], status)