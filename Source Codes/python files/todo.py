from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
import webbrowser
from threading import Timer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_all_todos")
def get_all_todos():
    todos = Todo.query.all()
    return render_template("get_all_todos.html", todos = todos)

@app.route("/update_and_save/<string:uuid>", methods = ["GET", "POST"])
def update_and_save(uuid):
    todo = Todo.query.filter_by(uuid=uuid).first()
    name = request.form.get("name")
    description = request.form.get("description")
    date_str = request.form.get("date")
    try :
        date_value = datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        date_str = date_str.replace("/", "-")
        date_value = datetime.strptime(date_str, '%m-%d-%Y').date()

    status = str(request.form.get("status"))
    todo.name = name
    todo.description = description
    todo.date = date_value
    todo.status = status

    db.session.commit()

    return redirect(url_for("get_all_todos"))

@app.route("/update/<string:uuid>")
def update_todo(uuid):
    todo = Todo.query.filter_by(uuid=uuid).first()
    return render_template("update_page.html", todo = todo)

@app.route("/create_todos", methods = ["POST"])
def create_todos():
    name = request.form.get("name")
    description = request.form.get("description")
    date_str = request.form.get("date")
    date_str = date_str.replace("/", "-")
    date_value = datetime.strptime(date_str, '%m-%d-%Y').date()
    status = str(request.form.get("status"))
    new_todo = Todo(name=name, description=description, date=date_value, status=status)
    db.session.add(new_todo)
    db.session.commit()

    return redirect(url_for("get_all_todos"))

@app.route("/delete/<string:uuid>")
def delete_todo(uuid):
    todo = Todo.query.filter_by(uuid=uuid).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("get_all_todos"))

@app.route("/get_todos_by_state/<string:status>")
def get_todos_by_state(status):
    todos = Todo.query.filter_by(status=status)

    return render_template("get_all_todos.html", todos = todos)


@app.route("/todo/api/v1.0/get_all_todos", methods=['GET'])
def get_all_todos_api():
    todos = Todo.query.all()
    dict_list = []
    for todo in todos:
        dict = {
            'uuid' : str(todo.uuid),
            'name' : str(todo.name),
            'description' : str(todo.description),
            'status' : str(todo.status),
            'date' : str(todo.date)
        }
        dict_list.append(dict)
    return jsonify(json.dumps(dict_list))

@app.route("/todo/api/v1.0/get_todos_by_state/<string:status>", methods=['GET'])
def get_todos_by_state_api(status):
    todos = Todo.query.filter_by(status=status)
    dict_list = []
    for todo in todos:
        dict = {
            'uuid' : str(todo.uuid),
            'name' : str(todo.name),
            'description' : str(todo.description),
            'status' : str(todo.status),
            'date' : str(todo.date)
        }
        dict_list.append(dict)
    return jsonify(json.dumps(dict_list))

@app.route("/todo/api/v1.0/create_todos", methods=["POST"])
def create_todos_api():
    date_str = request.json['date']
    try :
        date_value = datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        date_value = datetime.strptime(date_str, '%m-%d-%Y').date()

    task = {
            'name' : request.json['name'],
            'description' : request.json['description'],
            'status' : str(request.json['status']),
            'date' : date_value
        }

    new_todo = Todo(name=task['name'], description=task['description'], date=date_value, status=task['status'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'new_todo': task})

@app.route("/todo/api/v1.0/update/<string:uuid>", methods=["PUT"])
def update_todo_api(uuid):
    date_str = request.json['date']
    try :
        date_value = datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        date_value = datetime.strptime(date_str, '%m-%d-%Y').date()

    todo = Todo.query.filter_by(uuid=uuid).first()
    todo.name = str(request.json['name'])
    todo.description = str(request.json['description'])
    todo.date = date_value
    todo.status = str(request.json['status'])
    db.session.commit()
    task = {
            'name' : todo.name,
            'description' : todo.description,
            'status' : todo.status,
            'date' : todo.date
        }
    return jsonify({'updated_todo': task})


@app.route("/todo/api/v1.0/delete/<string:uuid>", methods=["DELETE"])
def delete_todo_api(uuid):
    todo = Todo.query.filter_by(uuid=uuid).first()
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'delete action result': True})

@app.route("/api_documentation")
def api_doc():
    return render_template("api_documentation.html")

class Todo(db.Model):
    uuid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    status = db.Column(db.String(80))

def open_browser():
    webbrowser.open_new('http://127.0.0.27:80/')

if __name__ == "__main__":
    from waitress import serve
    Timer(1, open_browser).start();
    #app.run(host="127.0.0.27", port=80, debug=True)
    serve(app, host="127.0.0.27", port=80)
