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

board_id = os.getenv('TRELLO_BOARD_ID')
to_do_list_id = os.getenv("TRELLO_TO_DO_LIST_ID")
to_do_list_name = os.getenv("TRELLO_TO_DO_LIST_NAME")
done_list_id = os.getenv("TRELLO_DONE_LIST_ID")
done_list_name = os.getenv("TRELLO_DONE_LIST_NAME")

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
    url = base_url + f"boards/{board_id}/lists"
    lists = requests.request("GET", url, headers=headers, params={**query, **{"cards": "open"}}).json()
    return [Item.from_trello_card(card, list) for list in lists for card in list["cards"]]

def add_item(title):
    """
    Adds a new item with the specified title to the Trello board.

    Args:
        title: The title of the item.
    """
    url = base_url + f"cards"
    requests.request("POST", url, headers=headers, params={**query, **{"idList": to_do_list_id, "name": title}}).json()

def update_item(id):
    """
    Updates an existing item on the board by moving it to a different list. 

    Args:
        id: The ID of the item to update.
    """
    url = base_url + f"cards/{id}"
    card = requests.request("GET", url, headers=headers, params=query).json()
    list_to_move_to_id = done_list_id if card["idList"] == to_do_list_id else to_do_list_id
    requests.request("PUT", url, headers=headers, params={**query, **{"idList": list_to_move_to_id}})

def remove_item(id):
    """
    Removes an item from the Trello board. If no existing item matches the ID of the specified item, nothing is removed.

    Args:
        id: Id of the item to remove.
    """
    url = base_url + f"cards/{id}"
    requests.request("DELETE", url, headers=headers, params=query).json()

