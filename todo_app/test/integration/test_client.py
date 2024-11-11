import pytest, json, os, mongomock
from dotenv import load_dotenv, find_dotenv
from todo_app import app
from mock import Mock 
from bson import ObjectId

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

def stub_item(isDone):
    return lambda _: {
            "_id": ObjectId("abc123abc123abc123abc123"), 
            "item": "test item", 
            "isDone": isDone
        }

def test_index_page(monkeypatch, client):
    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == 200


def test_add_item(monkeypatch, client):
    # Arrange
    item_name = "fake new item title"
    my_mock = Mock()
    monkeypatch.setattr(client.application.cosmosDbService.collection, 'insert_one', my_mock)

    # Act
    client.post('/add-item', data=dict(newItem=item_name))

    # Assert
    assert my_mock.call_count == 1
    assert my_mock.call_args.args[0] == {"item": item_name, "isDone": False}


def test_move_item_to_done(monkeypatch, client):
    # Arrange
    item_id = "123abc123abc123abc123abc"
    my_mock = Mock()
    monkeypatch.setattr(client.application.cosmosDbService.collection, 'update_one', my_mock)
    monkeypatch.setattr(client.application.cosmosDbService.collection, 'find_one', stub_item(False))

    # Act
    client.post('/update-item', data=json.dumps(dict(id=item_id)),
                content_type='application/json')

    # Assert
    assert my_mock.call_count == 1
    assert my_mock.call_args.args[0] == {"_id": ObjectId(item_id)}, {"$set": {"isDone": True}}


def test_move_item_to_to_do(monkeypatch, client):
    # Arrange
    item_id = "123abc123abc123abc123abc"
    my_mock = Mock()
    monkeypatch.setattr(client.application.cosmosDbService.collection, 'update_one', my_mock)
    monkeypatch.setattr(client.application.cosmosDbService.collection, 'find_one', stub_item(True))

    # Act
    client.post('/update-item', data=json.dumps(dict(id=item_id)),
                content_type='application/json')

    # Assert
    assert my_mock.call_count == 1
    assert my_mock.call_args.args[0] == {"_id": ObjectId(item_id)}, {"$set": {"isDone": False}}


def test_remove_item(monkeypatch, client):
    # Arrange
    item_id = "123abc123abc123abc123abc"
    my_mock = Mock()
    monkeypatch.setattr(client.application.cosmosDbService.collection, 'delete_one', my_mock)

    # Act
    client.post('/remove-item', data=json.dumps(dict(id=item_id)), content_type='application/json')

    # Assert
    assert my_mock.call_count == 1
    assert my_mock.call_args.args[0] ==  {"_id": ObjectId(item_id)}
