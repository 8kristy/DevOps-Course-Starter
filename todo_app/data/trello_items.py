import os, requests

base_url = "https://api.trello.com/1/"

headers = {
  "Accept": "application/json"
}

query = {
  'key': os.getenv('TRELLO_API_KEY'),
  'token': os.getenv('TRELLO_API_TOKEN')
}

def get_list_ids():
    """
    Fetches the IDs for the lists called "To Do" and "Done" in the Trello board.

    Returns:
        to_do_list_id: The ID of the list called "To Do"
        done_list_id: The ID of the list called "Done"
    """
    url = base_url + f"boards/{os.getenv('TRELLO_BOARD_ID')}/lists"
    lists = requests.request("GET", url, headers=headers, params=query).json()
    to_do_list_id = next((x for x in lists if x["name"] == "To Do"), None)["id"]
    done_list_id = next((x for x in lists if x["name"] == "Done"), None)["id"]
    return to_do_list_id, done_list_id

def get_cards_from_list(id):
    """
    Fetches the cards for the specified list

    Returns:
        list: The list of card objects that have the ID and the title of the card
    """
    url = base_url + f"lists/{id}/cards"
    cards = requests.request("GET", url, headers=headers, params=query).json()
    return [{"id": x["id"], "title": x["name"]} for x in cards]

def get_items():
    """
    Fetches all saved items from the Trello board.

    Returns:
        list: The list of saved items.
    """
    to_do_list_id, done_list_id = get_list_ids()
    to_do_cards = [dict(x, status='Completed') for x in get_cards_from_list(to_do_list_id)]
    done_cards = [dict(x, status='Not Started') for x in get_cards_from_list(done_list_id)]
    return to_do_cards + done_cards

def get_item(id):
    """
    Fetches the item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)


def add_item(title):
    """
    Adds a new item with the specified title to the Trello board.

    Args:
        title: The title of the item.

    Returns:
        item: The new item.
    """
    pass


def save_item(item):
    """
    Updates an existing item on the board by moving it to a different list. 
    If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    pass

def remove_item(id):
    """
    Removes an item from the Trello board. If no existing item matches the ID of the specified item, nothing is removed.

    Args:
        id: Id of the item to remove.
    """
    pass

