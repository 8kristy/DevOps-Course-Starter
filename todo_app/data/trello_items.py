import os, requests
from todo_app.data.classes.Item import Item

class TrelloService():
    def __init__(self):
        self.base_url = "https://api.trello.com/1/"
        self.headers = {"Accept": "application/json"}
        self.query = {
            "key": os.getenv("TRELLO_API_KEY"),
            "token": os.getenv("TRELLO_API_TOKEN")
        }
        self.board_id = os.getenv("TRELLO_BOARD_ID")
        self.to_do_list_id = os.getenv("TRELLO_TO_DO_LIST_ID")
        self.done_list_id = os.getenv("TRELLO_DONE_LIST_ID")

    def get_items(self):
        """
        Fetches all saved items from the Trello board.

        Returns:
            list: The list of saved items.
        """
        url = self.base_url + f"boards/{self.board_id}/lists"
        lists = requests.get(url, headers=self.headers, params={**self.query, **{"cards": "open"}}).json()
        return [Item.from_trello_card(card, list) 
                for list in lists 
                for card in list["cards"]]

    def add_item(self, title):
        """
        Adds a new item with the specified title to the Trello board.

        Args:
            title: The title of the item.
        """
        url = self.base_url + f"cards"
        requests.post(url, headers=self.headers, params={**self.query, **{"idList": self.to_do_list_id, "name": title}}).json()

    def update_item(self, id):
        """
        Updates an existing item on the board by moving it to a different list. 

        Args:
            id: The ID of the item to update.
        """
        url = self.base_url + f"cards/{id}"
        card = requests.get(url, headers=self.headers, params=self.query).json()
        list_to_move_to_id = self.done_list_id if card["idList"] == self.to_do_list_id else self.to_do_list_id
        requests.put(url, headers=self.headers, params={**self.query, **{"idList": list_to_move_to_id}})

    def remove_item(self, id):
        """
        Removes an item from the Trello board. If no existing item matches the ID of the specified item, nothing is removed.

        Args:
            id: Id of the item to remove.
        """
        url = self.base_url + f"cards/{id}"
        requests.delete(url, headers=self.headers, params=self.query)

