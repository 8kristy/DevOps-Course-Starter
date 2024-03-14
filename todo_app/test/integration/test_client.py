import json
import os
from dotenv import load_dotenv, find_dotenv
import pytest
import requests
from todo_app import app
from mock import Mock, ANY


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data


def stub(url, headers={}, params={}):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')

    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do',
            'cards': [{'id': '456', 'name': 'Test card'}]
        }]
        return StubResponse(fake_response_data)

    raise Exception(f'Integration test did not expect URL "{url}"')


def to_do_card_stub(url, headers={}, params={}):
    return StubResponse({'idList': os.environ.get('TRELLO_TO_DO_LIST_ID')})


def done_card_stub(url, headers={}, params={}):
    return StubResponse({'idList': os.environ.get('TRELLO_DONE_LIST_ID')})


def test_index_page(monkeypatch, client):
    # Arrange
    monkeypatch.setattr(requests, 'get', stub)

    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == 200
    assert 'Test card' in response.data.decode()


def test_add_item(monkeypatch, client):
    # Arrange
    item_name = "fake new item title"
    my_mock = Mock()
    monkeypatch.setattr(requests, 'post', my_mock)

    # Act
    client.post('/add-item', data=dict(newItem=item_name))

    # Assert
    assert my_mock.call_count == 1
    assert my_mock.call_args.args[0] == f"https://api.trello.com/1/cards"
    assert my_mock.call_args.kwargs["params"]["idList"] == os.environ.get('TRELLO_TO_DO_LIST_ID')
    assert my_mock.call_args.kwargs["params"]["name"] == item_name


def test_move_item_to_done(monkeypatch, client):
    # Arrange
    card_id = "123abc"
    monkeypatch.setattr(requests, 'get', to_do_card_stub)
    my_mock = Mock()
    monkeypatch.setattr(requests, 'put', my_mock)

    # Act
    client.post('/update-item', data=json.dumps(dict(id=card_id)),
                content_type='application/json')

    # Assert
    assert my_mock.call_count == 1
    assert my_mock.call_args.args[0] == f"https://api.trello.com/1/cards/{card_id}"
    assert my_mock.call_args.kwargs["params"]["idList"] == os.environ.get('TRELLO_DONE_LIST_ID')


def test_move_item_to_to_do(monkeypatch, client):
    # Arrange
    card_id = "123abc"
    monkeypatch.setattr(requests, 'get', done_card_stub)
    my_mock = Mock()
    monkeypatch.setattr(requests, 'put', my_mock)

    # Act
    client.post('/update-item', data=json.dumps(dict(id=card_id)),
                content_type='application/json')

    # Assert
    assert my_mock.call_count == 1
    assert my_mock.call_args.args[0] == f"https://api.trello.com/1/cards/{card_id}"
    assert my_mock.call_args.kwargs["params"]["idList"] == os.environ.get('TRELLO_TO_DO_LIST_ID')


def test_remove_item(monkeypatch, client):
    # Arrange
    card_id = "123abc"
    my_mock = Mock()
    monkeypatch.setattr(requests, 'delete', my_mock)

    # Act
    client.post('/remove-item', data=json.dumps(dict(id=card_id)), content_type='application/json')

    # Assert
    assert my_mock.call_count == 1
    assert my_mock.call_args.args[0] == f"https://api.trello.com/1/cards/{card_id}"
