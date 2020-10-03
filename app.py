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

    def __repr__(self):
        return '<Item {self.id} {self.describtion}>'



@app.route('/')
def index():
    return render_template('index.html',data=ToDo.query.all())

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
if __name__ == '__main__':
    app.debug = True
    app.run()        