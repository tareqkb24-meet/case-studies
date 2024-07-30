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

app.config['SECRET_KEY'] = 'super-secret-key'
firebase = pyrebase.initialize_app(firebaseConfig) 
auth = firebase.auth()
db = firebase.database()

@app.route('/home', methods=['GET', 'POST'])
def index():
  if request.method == "POST":
    print('lala')
    if "change_mode" in request.form:
      print(login_session['mode'])
      if login_session['mode'] == "signup":
        login_session['mode'] = "login"
      elif login_session['mode'] == "login":
        login_session['mode'] = "signup"
      print(login_session['mode'])

    else:
      if login_session['mode'] == "signup":
        email = request.form["email"]
        username = request.form['username']
        password = request.form['password']
        pair = "None" 
        choice = request.form['choice']
        login_session["user"] = auth.create_user_with_email_and_password(email, password)
        user = {'username': username, 'email':email, 'password':password, "pair": pair, "choice": choice}
        UID = login_session["user"]['localId']
        login_session["user"]["choice"] = choice
        db.child("user").child(UID).set(user)
        for i in db.child("user").get().val():  
            if db.child("user").child(i).child("pair").get().val() == "None" and db.child("user").child(i).child("choice").get().val() != login_session["user"]["choice"]:
              db.child("user").child(UID).update({'pair':i})
              db.child("user").child(i) .update({'pair':UID})
              return redirect(url_for("chat"))
        return('not pair')
      if mode == "signin":
        #signin
        pass
    return render_template("index.html", mode=login_session['mode'])
  login_session['mode'] = "signup"
  return render_template("index.html", mode=login_session['mode'])


@app.route ('/chat', methods = ['GET', 'POST']) 
def chat ():
  if request.method == 'POST':
    studentInput = request.form['student']
    UID = login_session["user"]['localId']
    msg = {"user": UID, "input" : studentInput}
    db.child("user").child(UID).child("chat").push(msg)

    return render_template('chat.html')

  return render_template('chat.html') 
 






if __name__ == "__main__":  
  app.run(debug=True)