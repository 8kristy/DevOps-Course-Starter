from flask import Flask, render_template, request, redirect
from todo_app.data.classes.Item import ItemStatus
from todo_app.data.trello_items import get_items, add_item, update_item, remove_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    items = sorted(items, key=lambda x: x.status.value)
    return render_template('index.html', items=items, item_status=ItemStatus)

@app.route('/add-item', methods=['POST'])
def addItem():
    add_item(request.form.get("newItem"))
    return redirect('/') 

@app.route('/update-item', methods=['POST'])
def updateItem():
    update_item(request.json.get("id"))
    return redirect('/')

@app.route('/remove-item', methods=['POST'])
def removeItem():
    remove_item(request.json.get("id"))
    return redirect('/')
