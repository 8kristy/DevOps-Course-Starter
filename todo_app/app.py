from flask import Flask, render_template, request, redirect
from todo_app.data.classes.ViewModel import ViewModel
from todo_app.data.trello_items import TrelloService

from todo_app.flask_config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    trelloService = TrelloService()

    @app.route('/')
    def index():
        items = trelloService.get_items()
        items = sorted(items, key=lambda x: x.status.value)
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add-item', methods=['POST'])
    def addItem():
        trelloService.add_item(request.form.get("newItem"))
        return redirect('/') 

    @app.route('/update-item', methods=['POST'])
    def updateItem():
        trelloService.update_item(request.json.get("id"))
        return redirect('/')

    @app.route('/remove-item', methods=['POST'])
    def removeItem():
        trelloService.remove_item(request.json.get("id"))
        return redirect('/')
    
    return app
