from flask import Flask, render_template, request, redirect
from todo_app.data.session_items import get_item, save_item, remove_item
from todo_app.data.trello_items import get_items, add_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    items = sorted(items, key=lambda x: x["status"], reverse=True)
    return render_template("index.html", items=items)

@app.route('/add-item', methods=['POST'])
def addItem():
    add_item(request.form.get("newItem"))
    return redirect('/') 

@app.route('/update-item', methods=['POST'])
def updateItem():
    item = get_item(request.json.get("id"))
    item["status"] = "Completed" if item["status"] == "Not Started" else "Not Started"
    save_item(item)
    return redirect('/')

@app.route('/remove-item', methods=['POST'])
def removeItem():
    remove_item(request.json.get("id"))
    return redirect('/')
