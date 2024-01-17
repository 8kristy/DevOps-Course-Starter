from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.session_items import get_items, add_item, get_item, save_item

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
    return redirect(url_for('index')) 

@app.route('/update-item', methods=['POST'])
def updateItem():
    id = request.json.get("id").split("_")[1]
    item = get_item(id)
    item["status"] = "Completed" if item["status"] == "Not Started" else "Not Started"
    save_item(item)
    return redirect(url_for('index')) 
