from flask import Flask
from flask import Flask, render_template, request, url_for, redirect 
from flask import session as login_session
import random
import pyrebase

app = Flask( __name__ , template_folder='templates',  static_folder='static'  )

firebaseConfig = {
  "apiKey": "AIzaSyCqhRweG6kJZPEdkymGcVJrO_aB_pGeUtU",
  "authDomain": "givat-haviva-69b54.firebaseapp.com",
  "databaseURL": "https://givat-haviva-69b54-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "givat-haviva-69b54",
  "storageBucket": "givat-haviva-69b54.appspot.com",
  "messagingSenderId": "633279220900",
  "appId": "1:633279220900:web:020c8bdd6d774df229aa31",
  "measurementId": "G-B9VJSMDJR4",
  "databaseURL":"https://givat-haviva-69b54-default-rtdb.europe-west1.firebasedatabase.app/"
}



@app.route('/home', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

app.config['SECRET_KEY'] = 'super-secret-key'
firebase = pyrebase.initialize_app(firebaseConfig) 
auth = firebase.auth()
db = firebase.database()


@app.route ('/chat', methods = ['GET', 'POST']) 
def chat (): 
  if request.method == "POST": 
    email = request.form["email"]
    username = request.form['username']
    password = request.form['password']
    login_session["user"] = auth.create_user_with_email_and_password(email, password)
    user = {'username': username, 'email':email, 'password':password }
    UID = login_session["user"]['localId']
    db.child("user").child(UID).set(user)
    return render_template("chat.html") 
  else : 
    return render_template("index.html") 
 

if __name__ == "__main__":  
  app.run(debug=True)