from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class students(db.Model):
   id = db.Column('student_id', db.Integer, primary_key = True)
   #roll_Number = db.Column(db.String(50),primary_key = True)
   email_Id = db.Column(db.String(50),unique=True, nullable=False)
   password = db.Column(db.String(10), nullable=False) 
   
   
   def __init__(self, email_Id,password):
      self.email_Id =email_Id
      #self.password = generate_password_hash(password)
      self.password = password

## Need to add these two lines to craete the table initially 
db.create_all()
db.session.commit()
#### Very dangerous comment as it will drop all the tables from the database ######################
###db.drop_all()
###db.session.commit()
#### Very dangerous comment as it will drop all the tables from the database ######################


@app.route('/register', methods = ['GET', 'POST'])
def register():
   if request.method == 'POST':
      if not request.form['email_Id'] or not request.form['password'] :
         flash('Please enter all the fields', 'error')
      else:
         email_Id = request.form['email_Id']
         password = request.form['password']
         #result = db.session.query((students.email_Id==email_Id)).scalar()
         data = students.query.filter_by(email_Id=email_Id).first()
         if data is None:
            ## It is a strange syntax to initialize the fields
            s1 = students(email_Id=email_Id,password=password)
            db.session.add(s1)
            db.session.commit()
            flash('Record was successfully added')
            return render_template('show_all.html')
         else:
            flash('Email Id already exists!!!!')
            flash('Please use the correct password to log in!!!!')
            render_template('register.html')
   return render_template('register.html')

@app.route('/show_all')
def show_all():
   print(students.query.all())
   return render_template('show_all.html', students = students.query.all() )

@app.route('/delete_One')
def delete_One():
   print(students.query.all())
   return render_template('show_all.html', students = students.query.all() )

@app.route('/edit_One')
def edit_One():
   print(students.query.all())
   return render_template('show_all.html', students = students.query.all() )

@app.route('/delete_all')
def delete_all():
   students.query.delete()
   db.session.commit()
   return render_template('delete_all.html', students = students.query.all() )

if __name__ == '__main__':
#   db.create_all()
   app.run(debug = True)