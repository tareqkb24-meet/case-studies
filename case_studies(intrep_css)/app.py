from flask import Flask, render_template, url_for, redirect, request
from flask import session  
import pyrebase 

app = Flask( __name__ , template_folder='templates',  static_folder='static'  )
app.config['SECRET_KEY'] = 'super-secret-key'
firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db =firebase.database()


if __name__ == "__main__":  
  app.run(debug=True)