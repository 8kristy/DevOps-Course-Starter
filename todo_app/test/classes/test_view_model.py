from todo_app.data.classes.Item import Item, ItemStatus
from todo_app.data.classes.ViewModel import ViewModel


def test_view_model_done_returns_completed_item_if_present():
    # Arrange
    items = { Item(1, "item1", ItemStatus.DONE), Item(2, "item2", ItemStatus.TODO), Item(3, "item3", ItemStatus.DONE) }
    view_model = ViewModel(items)

    # Act
    done_items = view_model.done_items

    # Assert
    assert len(done_items) == 2
    assert 1 in [x.id for x in done_items]
    assert 2 not in [x.id for x in done_items]
    assert 3 in [x.id for x in done_items]
