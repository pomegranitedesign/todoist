# Created by Dmitriy Shin on June 23, 2020
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy as sa
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = sa(app)


# Model(s)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"TODO {self.id}: {self.task}; done: {self.done}"


@ app.route('/')
def home():
    return render_template('home.html')


@ app.route('/todos')
def todos():
    todos = Todo.query.all()
    return render_template('todos.html', todos=todos)


@app.route('/add-todo', methods=['GET', 'POST'])
def add_todo():
    if request.method == 'POST':
        task = request.form['task']
        new_todo = Todo(task=task)
        db.session.add(new_todo)
        db.session.commit()
        return redirect('/todos')
    else:
        return render_template('add_todo.html')


@app.route('/remove-todo/<int:todo_id>', methods=['GET', 'POST'])
def remove_todo(todo_id: int):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return redirect('/todos')
    else:
        return render_template('404.html')


@app.route('/check_todo/<int:todo_id>', methods=['POST'])
def check_todo(todo_id: int):
    todo = Todo.query.get(todo_id)
    todo.done = True if not todo.done else False
    db.session.commit()
    return redirect('/todos')


if __name__ == '__main__':
    app.run(debug=True)
