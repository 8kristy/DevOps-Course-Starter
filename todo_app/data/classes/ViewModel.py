from todo_app.data.classes.Item import ItemStatus

class ViewModel:
    def __init__(self, items):
        self._items = items
 
    @property
    def items(self):
        return self._items
    
    @property
    def done_items(self):
        return [x for x in self._items if x.status == ItemStatus.DONE]
    
    @property
    def to_do_items(self):
        return [x for x in self._items if x.status == ItemStatus.TODO]