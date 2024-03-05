# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

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

## Configuration
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

To run all tests, simply run `pytest` from the terminal in the root folder. (`pytest <path\to\file>` to run tests in that file, `pytest <path\to\file> -k '<test_name>'` to run 1 specific test)

To run tests in VSCode, press the "Testing" item on the left (beaker icon) or Ctrl+Shift+P -> `View: Show Testing` and select `pytest`, then `todo_app` when running the configuration. The tests should appear on the side panel and you should be able to run them through the UI, including adding breakpoints and debugging. 