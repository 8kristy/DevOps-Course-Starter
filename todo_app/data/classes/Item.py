import os

class Item:
    def __init__(self, id, name, status = 'To Do'):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def from_trello_card(cls, card, list):
        status = "Completed" if list['name'] == os.getenv("TRELLO_DONE_LIST_NAME") else "Not Started"
        return cls(card['id'], card['name'], status)