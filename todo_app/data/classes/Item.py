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
    def from_trello_card(cls, card, list):
        status = ItemStatus.DONE if list['id'] == os.getenv("TRELLO_DONE_LIST_ID") else ItemStatus.TODO
        return cls(card['id'], card['name'], status)