from flask import Flask, render_template, request, redirect
from todo_app.data.classes.ViewModel import ViewModel
from todo_app.data.cosmos_db_items import CosmosDbService

from todo_app.flask_config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    app.cosmosDbService = CosmosDbService()

    @app.route('/')
    def index():
        items = app.cosmosDbService.get_items()
        items = sorted(items, key=lambda x: x.status.value)
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add-item', methods=['POST'])
    def addItem():
        app.cosmosDbService.add_item(request.form.get("newItem"))
        return redirect('/') 

    @app.route('/update-item', methods=['POST'])
    def updateItem():
        app.cosmosDbService.update_item(request.json.get("id"))
        return redirect('/')

    @app.route('/remove-item', methods=['POST'])
    def removeItem():
        app.cosmosDbService.remove_item(request.json.get("id"))
        return redirect('/')
    
    return app
