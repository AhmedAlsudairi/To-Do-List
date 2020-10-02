from flask import Flask, render_template,request,redirect,url_for,jsonify
from  flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:admin@localhost:5432/todoapp'
db = SQLAlchemy(app)

class ToDo(db.Model):
    __tablename__ = 'todos'
    id= db.Column(db.Integer,primary_key=True)
    describtion=db.Column(db.String(),nullable=False)

    def __repr__(self):
        return '<Item {self.id} {self.describtion}>'

db.create_all()

@app.route('/')
def index():
    return render_template('index.html',data=ToDo.query.all())

@app.route('/todos/create', methods=['POST'])
def create_todo():
    describtion= request.get_json()['describtion']
    toDoItem=ToDo(describtion=describtion)
    db.session.add(toDoItem)
    db.session.commit()
    return jsonify({
        'describtion': toDoItem.describtion
    })
if __name__ == '__main__':
    app.debug = True
    app.run()        