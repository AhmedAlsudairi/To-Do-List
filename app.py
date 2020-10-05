from flask import Flask, render_template,request,redirect,url_for,jsonify, abort
from  flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:admin@localhost:5432/todoapp'
db = SQLAlchemy(app)

migrate = Migrate(app,db)
class ToDo(db.Model):
    __tablename__ = 'todos'
    id= db.Column(db.Integer,primary_key=True)
    describtion=db.Column(db.String(),nullable=False)
    completed=db.Column(db.Boolean,nullable=False,default=False)
    list_id= db.Column(db.Integer,db.ForeignKey('todolists.id'),nullable=False)

    def __repr__(self):
        return '<Item {self.id} {self.describtion}>'

class ToDoList(db.Model):
    __tablename__ = 'todolists'
    id= db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(),nullable=False)
    children= db.relationship('ToDo',backref='list',lazy=True)

@app.route('/')
def index():
    return render_template('index.html',data=ToDo.query.order_by('id').all())

@app.route('/todos/create', methods=['POST'])
def create_todo():
    body={}
    try:
        describtion= request.get_json()['describtion']
        toDoItem=ToDo(describtion=describtion)
        db.session.add(toDoItem)
        db.session.commit()
        body=toDoItem.describtion
    except:
        db.session.rollback()
        print(sys.exe_info())
    finally:
        db.session.close()    
        return jsonify({
            'describtion': body
        })

@app.route('/todos/<todo_id>/set-completed',methods=['POST'])
def setCompleted(todo_id):
    try:
        completed = request.get_json()['completed']
        todo_item = ToDo.query.get(todo_id)
        todo_item.completed = completed
        db.session.commit()        
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))        

@app.route('/todos/<todo_id>/delete',methods=['DELETE'])
def deleteItem(todo_id):
    try:
        todo_item = ToDo.query.get(todo_id)
        db.session.delete(todo_item)
        db.session.commit()        
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))            
if __name__ == '__main__':
    app.debug = True
    app.run()        