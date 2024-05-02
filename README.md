# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## Running with Docker

First do the steps in [Configuration](#configuration) to configure your environment variables

### Development

Run `docker build --target development --tag to-do-app:dev .` from the root to build the container and then `docker run -p 5000:5000 --env-file .env --mount "type=bind,source=$(pwd),target=/usr/src/app" to-do-app:dev` to run it. The code should change without you needing to re-run the container.

The app should be accessible in the browser via http://localhost:5000/

### Prod

`docker build --target production --tag to-do-app:prod .`

`docker run -p 5000:5000 --env-file .env to-do-app:prod `


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

You need to populate the `TRELLO_API_KEY`,`TRELLO_API_TOKEN`, `TRELLO_BOARD_ID`, `TRELLO_TO_DO_LIST_ID` and `TRELLO_DONE_LIST_ID` variables in the `.env` file. 

First create a [Trello](https://trello.com/) account and make a test board (e.g. To-Do App - test) with `To Do` and `Done` columns.

Create a new power-up for the app here https://trello.com/power-ups/admin, then generate an API key and after that a token for it (there should be a link on the right of the API key) - these are the values for `TRELLO_API_KEY` and `TRELLO_API_TOKEN` respectively.

To get your test board ID, make this GET request (don't forget to substitute the values)

```
https://api.trello.com/1/members/me/boards?key={TRELLO_API_KEY}&token={TRELLO_API_TOKEN}
```
find your test board object (the name of it should be displayed), copy the ID and put it as your `TRELLO_BOARD_ID` value.

To get `TRELLO_TO_DO_LIST_ID` and `TRELLO_DONE_LIST_ID`, make this request
```
https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/lists?key={TRELLO_API_KEY}&token={TRELLO_API_TOKEN}
```
and copy the IDs from the response into the variables.

## Running the App

Once the all dependencies have been installed and secret values added, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

If you get an error saying 

> Recreating virtualenv todo-app in \<your working directory\>\\.venv

> 'flask' is not recognized as an internal or external command,
operable program or batch file." 

(especially if you tried running the dev Docker container) you might need to run `poetry install` and try again

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

# Running the tests 

To run all tests, simply run `poetry run pytest` from the terminal in the root folder. (`poetry run pytest <path\to\file>` to run tests in that file, `poetry run pytest <path\to\file> -k '<test_name>'` to run 1 specific test)

To run tests in VSCode, press the "Testing" item on the left (beaker icon) or Ctrl+Shift+P -> `View: Show Testing` and select `pytest`, then `todo_app` when running the configuration. The tests should appear on the side panel and you should be able to run them through the UI, including adding breakpoints and debugging. 

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
  trello_api_key: <TRELLO_API_KEY>
  trello_api_token: <TRELLO_API_TOKEN>
  trello_board_id: <TRELLO_BOARD_ID>
  trello_to_do_list_id: <TRELLO_TO_DO_LIST_ID> 
  trello_done_list_id: <TRELLO_DONE_LIST_ID>
  ```
  - Save the vault

### Setup without a vault (NOT RECOMMENDED)
Instead of creating a vault you can also just make a file `vars\webservers` and paste the same data as you'd do in the vault into it

## Running

Run `ansible-playbook playbook.yml -i inventory.ini --ask-vault-pass` and enter your vault password (or just `ansible-playbook playbook.yml -i inventory.ini` if you didn't create a vault). 

The configuration should be applied to all managed nodes and you should be able to connect to them using `<node_ip>:5000` from the browser.

 