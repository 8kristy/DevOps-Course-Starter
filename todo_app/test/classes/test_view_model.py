import pytest
from todo_app.data.classes.Item import Item, ItemStatus
from todo_app.data.classes.ViewModel import ViewModel

@pytest.fixture
def view_model_with_items():
    items = { Item(1, "item1", ItemStatus.DONE), Item(2, "item2", ItemStatus.TODO), Item(3, "item3", ItemStatus.DONE) }
    return ViewModel(items)

def test_view_model_done_returns_completed_items_if_present(view_model_with_items):
    # Act
    done_items = view_model_with_items.done_items

    # Assert
    assert len(done_items) == 2
    assert 1 in [x.id for x in done_items]
    assert 2 not in [x.id for x in done_items]
    assert 3 in [x.id for x in done_items]

def test_view_model_done_returns_to_do_items_if_present(view_model_with_items):
    # Act
    done_items = view_model_with_items.to_do_items

    # Assert
    assert len(done_items) == 1
    assert 1 not in [x.id for x in done_items]
    assert 2 in [x.id for x in done_items]
    assert 3 not in [x.id for x in done_items]

