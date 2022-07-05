from flask import Flask, request
import datetime
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String())
    description = db.Column(db.String())
    status = db.Column(db.String())
    created_date = db.Column(db.Date())
    last_edited_date = db.Column(db.Date())
    target_date = db.Column(db.String())
 
    def __init__(self, heading,description,status,created_date,last_edited_date,target_date):
        self.heading = heading
        self.description = description
        self.status = status
        self.created_date = created_date
        self.last_edited_date = last_edited_date
        self.target_date = target_date
 
    def __repr__(self):
        return f"{self.heading}:{self.status}"


class todoSchema(ma.Schema):
    class Meta:
        fields = ("id", "heading", "description", "status", "created_date", "last_edited_date", "target_date")


todo_schema = todoSchema()
todos_schema = todoSchema(many=True)


class getAllTodos(Resource):
    def get(self):
        try:
            todos = todo.query.all()
            return todos_schema.dump(todos)
        except:
            return "Error while getting list of todos"

class getTodoById(Resource):
    def get(self, todo_id):
        try:
            todos = todo.query.get_or_404(todo_id)
            return todo_schema.dump(todos)
        except:
            return "Error while getting todo by ID"

class createTodo(Resource):
    def post(self):
        try:
            new_todo = todo(
                heading=request.json['heading'],
                description=request.json['description'],
                status=request.json['status'],
                created_date=datetime.datetime.now(),
                last_edited_date=datetime.datetime.now(),
                target_date=request.json['target_date'],
            )
            db.session.add(new_todo)
            db.session.commit()
            return todo_schema.dump(new_todo)
        except:
            return "Error while creating a todo"

class updateTodo(Resource):
    def patch(self, todo_id):
        try:
            todos = todo.query.get_or_404(todo_id)
            todos.last_edited_date = datetime.datetime.now()

            if 'heading' in request.json:
                todos.heading = request.json['heading']
            if 'description' in request.json:
                todos.description = request.json['description']
            if 'status' in request.json:
                todos.status = request.json['status']
            if 'created_date' in request.json:
                todos.created_date = request.json['created_date']
            if 'target_date' in request.json:
                todos.target_date = request.json['target_date']

            db.session.commit()
            return todo_schema.dump(todos)
        except:
            return "Error while Updating a todo"

class deleteTodo(Resource):
    def delete(self, todo_id):
        try:
            todos = todo.query.get_or_404(todo_id)
            db.session.delete(todos)
            db.session.commit()
            return 'Data deleted Successfully', 204
        except:
            return "Error while deleting a todo"

api.add_resource(getAllTodos, '/')
api.add_resource(getTodoById, '/<int:todo_id>')
api.add_resource(createTodo, '/create')
api.add_resource(updateTodo, '/update/<int:todo_id>')
api.add_resource(deleteTodo, '/delete/<int:todo_id>')


if __name__ == '__main__':
    app.run(debug=True)
