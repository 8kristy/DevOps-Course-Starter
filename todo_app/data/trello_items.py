import os, requests

base_url = "https://api.trello.com/1/"

headers = {
  "Accept": "application/json"
}

query = {
  'key': os.getenv('TRELLO_API_KEY'),
  'token': os.getenv('TRELLO_API_TOKEN')
}

board_id = os.getenv('TRELLO_BOARD_ID')
to_do_list_id = os.getenv("TRELLO_TO_DO_LIST_ID")
done_list_id = os.getenv("TRELLO_DONE_LIST_ID")

status_map_by_id = { 
    to_do_list_id: "Not Started", 
    done_list_id: "Completed" 
}

def get_items():
    """
    Fetches all saved items from the Trello board.

    Returns:
        list: The list of saved items.
    """
    url = base_url + f"boards/{board_id}/cards"
    cards = requests.request("GET", url, headers=headers, params=query).json()
    return [{"id": x["id"], "title": x["name"], "status": status_map_by_id[x["idList"]]} for x in cards]

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
    url = base_url + f"cards"
    newItem = requests.request("POST", url, headers=headers, params={**query, **{"idList": to_do_list_id, "name": title}}).json()
    return {"id": newItem["id"], "status": "Not Started", "title": newItem["name"]}

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

