import os
from flask import Flask, render_template, request, redirect
from todo_app.data.session_items import remove_item
from todo_app.data.trello_items import get_items, add_item, update_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    items = sorted(items, key=lambda x: x.status, reverse=True)
    return render_template("index.html", items=items, done_list_name=os.getenv("TRELLO_DONE_LIST_NAME"))

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
