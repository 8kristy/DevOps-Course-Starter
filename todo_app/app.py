from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, login_user
from todo_app.data.classes.ViewModel import ViewModel
from todo_app.data.classes.User import User
from todo_app.data.cosmos_db_items import CosmosDbService

from todo_app.flask_config import Config

from urllib.parse import urlencode
import os, requests

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    app.cosmosDbService = CosmosDbService()

    login_manager = LoginManager()
    github_base_url = "https://github.com/login/oauth"

    @login_manager.unauthorized_handler
    def unauthenticated():
        params = {
            "client_id": os.getenv("OAUTH_CLIENT_ID")
        }
        return redirect(f"{github_base_url}/authorize?{urlencode(params)}"
)

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    login_manager.init_app(app)

    @app.route('/login/callback')
    def loginCallback():
        code = request.args.get('code')
        json_header = {"Accept": "application/json"}
        params = {
            "client_id": os.getenv("OAUTH_CLIENT_ID"),
            "client_secret": os.getenv("OAUTH_CLIENT_SECRET"),
            "code": code
        }

        access_token = requests.post(f"{github_base_url}/access_token", headers=json_header, params=params).json()["access_token"]
        auth_header = {"Authorization": f"Bearer {access_token}"}
        user_info = requests.get("https://api.github.com/user", headers={**json_header, **auth_header}, params=params).json()
        login_user(User(user_info["id"]))
        return redirect('/') 

    @app.route('/')
    @login_required
    def index():
        items = app.cosmosDbService.get_items()
        items = sorted(items, key=lambda x: x.status.value)
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add-item', methods=['POST'])
    @login_required
    def addItem():
        app.cosmosDbService.add_item(request.form.get("newItem"))
        return redirect('/') 

    @app.route('/update-item', methods=['POST'])
    @login_required
    def updateItem():
        app.cosmosDbService.update_item(request.json.get("id"))
        return redirect('/')

    @app.route('/remove-item', methods=['POST'])
    @login_required
    def removeItem():
        app.cosmosDbService.remove_item(request.json.get("id"))
        return redirect('/')
    
    return app
