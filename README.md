# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## Running with Docker

First do the steps in [Configuration](#configuration) to configure your environment variables

### Development

`docker compose up --build`

The app should be accessible in the browser via http://localhost:5000/ The code should change without you needing to re-run the container and tests re-run on change.

### Debug

Download the [Docker extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) and [Remote Development extention](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)

Run `docker compose -f docker-compose.debug.yml up --build`

Open the Docker extension on the side, right click your running container and press "Attach Visual Studio Code". A new window should pop up. Wait for it to connect to the container.

Open the `/usr/src/app` folder in the container. Click on the debug/run menu on the new Window and try running the Flask app with debugging on. It will prompt you to install Python Extension, do that.

Run it again and you should be able to access the app on http://localhost:5000/. If you add any break points on your new window connected to the container, the app will stop there and show all the information in the debugger.

### Prod

`docker compose -f .\docker-compose.prod.yml up --build`

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

You can check poetry is installed by running `poetry --version` from a terminal.

**Please note that after installing poetry you may need to restart VSCode and any terminals you are running before poetry will be recognised.**

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## <a name="configuration"></a> Configuration

You need to populate the `COSMOS_DB_CONNECTION_STRING`,`COSMOS_DB_DATABASE_NAME`, `COSMOS_DB_COLLECTION_NAME`, `OAUTH_CLIENT_ID` and `OAUTH_CLIENT_SECRET` variables in the `.env` file. 

Set up your CosmosDB
```
az cosmosdb create --name <cosmos_account_name> --resource-group <resource_group_name> --kind MongoDB --capabilities EnableServerless --server-version 4.2

az cosmosdb mongodb database create --account-name <cosmos_account_name> --name <database_name> --resource-group <resource_group_name>
```

`COSMOS_DB_CONNECTION_STRING` can be found on Azure under your cluster (i.e. cosmos_account_name) -> Settings -> Connection Strings -> Primary connection string

`COSMOS_DB_DATABASE_NAME` is `<database_name>` from earlier command

Create a collection in your DB on Azure. Put the name of the collection to `COSMOS_DB_COLLECTION_NAME`

Create a [GitHub OAuth App](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app) and fill in `OAUTH_CLIENT_ID` and `OAUTH_CLIENT_SECRET` with value from there 

## Running the App

Once the all dependencies have been installed and secret values added, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app 'todo_app/app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 113-666-066
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

# Troubleshooting

If you experience problems when changing between running on Docker and locally (e.g. flask/pytest not found errors):
- Delete `.venv` folder
- Run poetry install (if you're running locally - if you get errors inside Docker don't run this)

# Running the tests 

To run all tests, simply run `poetry run pytest` from the terminal in the root folder. (`poetry run pytest <path\to\file>` to run tests in that file, `poetry run pytest <path\to\file> -k '<test_name>'` to run 1 specific test)

To run tests in VSCode, press the "Testing" item on the left (beaker icon) or Ctrl+Shift+P -> `View: Show Testing` and select `pytest`, then `todo_app` when running the configuration. The tests should appear on the side panel and you should be able to run them through the UI, including adding breakpoints and debugging. 

### Docker

```
docker build --target test --tag todo-app:test .
docker run --mount "type=bind,source=$(pwd),target=/usr/src/app" todo-app:test
```

If running the default `docker-compose.yml` tests will run automatically on code change.

# <a name="ssh"></a>SSH Setup

Run `ssh-keygen`, then

  - **On Linux**

    - Run `ssh-copy-id user@host` and enter the password
    - You can now connect to the machine using `ssh user@host` without a password

  - **On Windows**

    - Connect to the host
    - Append your public key to the `~/.ssh/authorized_keys` file (e.g. `vim ~/.ssh/authorized_keys` and paste it at the end of the file). The public key will either be in `C:\Users\<user>\.ssh` or in the current folder if a custom name was given (this is the `<key>.pub`)
    - Save the file and exit the machine
    - You can now connect to the machine using `ssh user@host -i path/to/private/key`


# Ansible Setup

Ansible is used to put new virtual machines to a desired state. Managed nodes addresses should be kept in `ansible\inventory.ini`.

## First Time Setup

This assumes that the nodes have already been set up
- Copy files inside `\ansible` to the contol node (i.e. `\ansible\.env.j2`, `\ansible\inventory.ini`, `\ansible\playbook.yml` and `\ansible\todoapp.service`)
  - Easiest way to this is to run `scp -r .\ansible\ user@host:`
- Connect to the control node using `ssh user@host`
  - This will prompt for a password; see [SSH Setup](#ssh) if you want to get rid of that
- Navigate to `\ansible` on the control node
- Create an ansible vault 
  - Run `ansible-vault create vars/webservers`
  - Enter a password (you need to remember it)
  - Copy your keys from .env to the vault in the following format (see [Configuration](#configuration) on how to get the values if you don't have them yet):
  ```
  cosmos_db_connection_string: <COSMOS_DB_CONNECTION_STRING>
  cosmos_db_database_name: <COSMOS_DB_DATABASE_NAME>
  cosmos_db_collection_name: <COSMOS_DB_COLLECTION_NAME>
  oauth_client_id: <OAUTH_CLIENT_ID>
  oauth_client_secret: <OAUTH_CLIENT_SECRET>
  ```
  - Save the vault

### Setup without a vault (NOT RECOMMENDED)
Instead of creating a vault you can also just make a file `vars\webservers` and paste the same data as you'd do in the vault into it

## Running

Run `ansible-playbook playbook.yml -i inventory.ini --ask-vault-pass` and enter your vault password (or just `ansible-playbook playbook.yml -i inventory.ini` if you didn't create a vault). 

The configuration should be applied to all managed nodes and you should be able to connect to them using `<node_ip>:5000` from the browser.

## Architecture diagrams

These can be found in `/diagrams`. Theres 3 (context, container and component) diagrams in `C4.svg` and 2 code diagrams the other 2 files.

### Updating diagrams

#### Context, container and component

You can import the `C4.svg` file to draw.io, edit and then export as `.svg` and replace the file.

#### Code

- Install `pylint` (this installs `pyreverse` which can generate the diagrams)
- `cd todo_app`
- `pyreverse -p todo_app .`
- This will generate 2 `.dot` files. You can use tools such as https://dreampuf.github.io/GraphvizOnline to draw the diagrams from those files (alternatively you can install Graphviz and run `pyreverse -o png -p todo_app .`)

# Pipeline Slack Notifications

If you want to receive build notifications on slack:
- Add the `Incoming WebHooks` app to the channel
- Copy Webhook URL from the configuration
- On GitHub: Settings -> Secrets and variables -> Actions -> Repository secrets
- New repository secret
  - Name: SLACK_WEBHOOK_URL
  - Secret: Webhook URL you copied from the Slack app

# Snyk

By default the job succeeds without checking anything. If you want to run a security scan you need to add `SNYK_TOKEN` to the secrets
- On Snyk: (bottom left) Your account -> Account settings -> General -> Auth Token -> Key -> Click to show
- Copy the key
- On GitHub: Settings -> Secrets and variables -> Actions -> Repository secrets
- New repository secret
  - Name: SNYK_TOKEN
  - Secret: Auth token you copied from the Snyk app

# Azure

This repos Docker image: https://hub.docker.com/repository/docker/8kristy/todo-app

## Prerequisites
- Docker
- Docker hub account
- Azure account and resource group
- Azure CLI

## Deployment

### Terraform
- Create a `terraform.tfvars` file in `/terraform`
- Fill in the values for variables defined in `/terraform/variables.tf`
- `terraform apply`

### Script
- Login to Docker using `docker login`
- Login to Azure using `az login`
- If you're on Windows, run 
  ```
  ./azure.ps1 -DockerName "<your_docker_username>" -ResourceGroupName "<your_resource_group>" -AppServicePlanName "<app_service_plan_name>" -WebAppName "globally_unique_web_app_name" -CosmosDbConnectionString <your_cosmos_db_connection_string> -CosmosDbDatabaseName <your_cosmos_db_database_name> -CosmosDbCollectionName <your_cosmos_db_collection_name> -OAuthClientId <oauth_app_client_id> -OAuthClientSecret <oauth_app_client_secret>
  ```
  Alternatively run all the commands in `azure.ps1` manually
- The app should be available on https://<globally_unique_web_app_name>.azurewebsites.net/
  - e.g. https://kristinatodoapp.azurewebsites.net/

# Restart the app
- Find the webhook URL for your app
  - On Azure portal - Your app resource -> Deployment -> Deployment Center -> Webhook URL
- Make a POST request to that URL, e.g. `curl -v -X POST <webhook_url>`

## Encryption
CosmosDB data is encrypted at rest and in transit, see [Data encryption in Azure Cosmos DB](https://learn.microsoft.com/en-us/azure/cosmos-db/database-encryption-at-rest) for more details. The deployed application forces HTTPS.