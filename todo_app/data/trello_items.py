import os, requests
from todo_app.data.classes.Item import Item

base_url = "https://api.trello.com/1/"

headers = {
  "Accept": "application/json"
}

query = {
  'key': os.getenv('TRELLO_API_KEY'),
  'token': os.getenv('TRELLO_API_TOKEN')
}

def get_items():
    """
    Fetches all saved items from the Trello board.

    Returns:
        list: The list of saved items.
    """
    url = base_url + f"boards/{os.getenv('TRELLO_BOARD_ID')}/lists"
    lists = requests.get(url, headers=headers, params={**query, **{"cards": "open"}}).json()
    return [Item.from_trello_card(card, list) for list in lists for card in list["cards"]]

def add_item(title):
    """
    Adds a new item with the specified title to the Trello board.

    Args:
        title: The title of the item.
    """
    url = base_url + f"cards"
    requests.post(url, headers=headers, params={**query, **{"idList": os.getenv("TRELLO_TO_DO_LIST_ID"), "name": title}}).json()

def update_item(id):
    """
    Updates an existing item on the board by moving it to a different list. 

    Args:
        id: The ID of the item to update.
    """
    url = base_url + f"cards/{id}"
    card = requests.request("GET", url, headers=headers, params=query).json()
    list_to_move_to_id = os.getenv("TRELLO_DONE_LIST_ID") if card["idList"] == os.getenv("TRELLO_TO_DO_LIST_ID") else os.getenv("TRELLO_TO_DO_LIST_ID")
    requests.put(url, headers=headers, params={**query, **{"idList": list_to_move_to_id}})

def remove_item(id):
    """
    Removes an item from the Trello board. If no existing item matches the ID of the specified item, nothing is removed.

    Args:
        id: Id of the item to remove.
    """
    url = base_url + f"cards/{id}"
    requests.delete(url, headers=headers, params=query).json()

