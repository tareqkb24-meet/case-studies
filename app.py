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
    # for student in db.child("user").get().val():  
      # if db.child("user").child(student).child("pair").get().val() == "None" and db.child("user").child(student).child("choice").get().val() != login_session["user"]["choice"]:
      #   db.child("user").child(UID).update()
        

  if request.method == "POST":
    if "change_mode" in request.form:
      print(login_session['mode'])
      if login_session['mode'] == "signup":
        login_session['mode'] = "login"
      elif login_session['mode'] == "login":
        login_session['mode'] = "signup"
      print(login_session['mode'])


    else:
       if login_session['mode'] == "signup":
        try:
          email = request.form["email"]
          username = request.form['username']
          password = request.form['password']
          pair = "None" 
          choice = request.form['choice']
          login_session["user"] = auth.create_user_with_email_and_password(email, password)
        except:
          return render_template("index.html")
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
        if login_session['mode'] == "login":
          try:
            email = request.form["email"]
            password = request.form['password']
            login_session["user"] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for("chat"))
          except:
            return render_template("index.html")
    if login_session['mode'] == 'signup':
      not_mode = 'login'
    else:
      not_mode = 'signup'
    return render_template("index.html", mode=login_session['mode'], not_mode=not_mode)
  login_session['mode'] = "signup"
  not_mode = "login"
  return render_template("index.html", mode=login_session['mode'], not_mode=not_mode)


@app.route ('/chat', methods = ['GET', 'POST']) 
def chat():
  UID = login_session["user"]['localId']

  if request.method == 'POST':
    studentInput = request.form['student']
    msg = {"user": UID, "input" : studentInput}
    db.child("user").child(UID).child("chat").push(msg)

    pair = db.child("user").child(UID).child('pair').get().val()

    db.child("user").child(pair).child("chat").push(msg)

  conversation = db.child("user").child(UID).child("chat").get().val()
  print(conversation)
  return render_template('chat.html', conversation = conversation) 
 

if __name__ == "__main__":  
  app.run(debug=True)