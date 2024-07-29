from flask import Flask
from flask import Flask, render_template, request, url_for, redirect
from flask import session as login_session
import random
import pyrebase

app = Flask( __name__ , template_folder='templates',  static_folder='static'  )

firebaseConfig = {
  "apiKey": "AIzaSyAAL4ipnYtGe8RGsmH4VUgs5RYwgP64X_Y",
  "authDomain": "giftapp-ad937.firebaseapp.com",
  "databaseURL": "https://giftapp-ad937-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "giftapp-ad937",
  "storageBucket": "giftapp-ad937.appspot.com",
  "messagingSenderId": "904198728084",
  "appId": "1:904198728084:web:3bcf00efde3e24626fc781",
  'measurementId': "G-BF70XBJ7YD"
};

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

app.config['SECRET_KEY'] = 'super-secret-key'
firebase = pyrebase.initialize_app(firebaseConfig) 
auth = firebase.auth()
db = firebase.database()

@app.route("/home")
def home():
  return render_template("index.html")

if __name__ == "__main__":  
  app.run(debug=True)