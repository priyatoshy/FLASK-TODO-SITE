#importing flask
from datetime import datetime
import re
from flask import Flask, render_template,request,redirect
#importing databases
from flask_sqlalchemy import SQLAlchemy
#importing datetime
from datetime import datetime
#CREATING APP AN app Object from flask class by giving the __name__ as parameter
app = Flask(__name__)


#setting up database orm with SQLAlchemy class

#CREATING A SQLite3 Databased
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///test.db"

#CHANGING THE TRACK MODIFICATION(SIGNAL EMITING ETC)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#CREATING A DATABASE OBJECT FROM SQLALCHEMY CLASS WITH OUR app AS PARAMETER
db=SQLAlchemy(app)


#CREATING A TODOCLASS with db.model as a parameter(a sublclass within db)
class Todo(db.Model):
   #creating fields
   sno=db.Column(db.Integer,primary_key=True)
   title=db.Column(db.String(200),nullable=False)
   desc=db.Column(db.String(500),nullable=False)
   date_created=db.Column(db.DateTime,default=datetime.utcnow)

   #creating a repr() method for printing object
   def __repr__(self) -> str:
       return f"{self.sno} : {self.title}"


#ROUTING DECORATORS

#THE HOME PAGE AND ADDITION FUNCTION

@app.route('/',methods=['GET','POST'])
def home():
   if request.method =='POST':
      #print("POST")
      title1=request.form['title']
      desc1=request.form['desc']
      todo=Todo(title=title1,desc=desc1)
      db.session.add(todo)
      db.session.commit()
      allTodo=Todo.query.all()
      return render_template('index.html',allTodo=allTodo)
 
   else:
      allTodo=Todo.query.all()
      return render_template('index.html',allTodo=allTodo)
      
      
      
      



   
  
#CREATING THE DELETE FUNCTION
@app.route('/delete/<int:sno>')
def delete(sno):
   todo=Todo.query.filter_by(sno=sno).first()
   db.session.delete(todo)
   db.session.commit()
   #return "deleted"
   return redirect("/")


#CRATE UPDATE FUNCTION
@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
   if request.method =='POST':
      
      title1=request.form['title']
      desc1=request.form['desc']
      todo=Todo.query.filter_by(sno=sno).first()
      todo.title=title1
      todo.desc=desc1
      db.session.add(todo)
      db.session.commit()
      return redirect("/")

   todo=Todo.query.filter_by(sno=sno).first()
   return render_template('update.html',todo=todo)
   

   



if __name__ == '__main__':
   app.run(debug = True,port=8000)