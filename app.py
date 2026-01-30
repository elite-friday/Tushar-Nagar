import os
import requests
from flask import Flask, redirect, request, url_for, render_template, session
from google_auth_oauthlib.flow import Flow
import sqlite3

app = Flask(__name__, static_folder='static', template_folder='templates')



# Secret key is required for Flask sessions (used by google oauth flow)
# In production, set the `FLASK_SECRET_KEY` environment variable to a strong value.
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')


#creating the database function
def init_db():
    conn=sqlite3.connect('login_user.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            playername TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    return conn

#route for login page
@app.route('/')
def login_page():
    return render_template('create_account.html')






#when click on login button this function will be called (email/password login)
@app.route('/login_email' ,methods=['GET', 'POST'])
def login_email():
    if request.method == 'GET':
        return render_template('login.html')
    
    email = request.form['email']
    password = request.form['password']
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? ", (email,))
    user = cursor.fetchone()
    conn.close()
    if user and user[3] == password:  # Assuming password is at index 3
        return render_template('index.html')  # Assuming playername is at index 1
    else:
        return render_template('login.html', error="Invalid credentials")

#route for home page
# @app.route('/home')
# def home():
#     return render_template('index.html')



#route for create account page
@app.route('/create_account_page', methods=['GET', 'POST'])
def create_account_page():
    return render_template('create_account.html')

#function for create account page / register user page
@app.route('/create_account', methods=['POST'])
def create_account():
    player_name = request.form.get('playername')
    email = request.form.get('email')
    password = request.form.get('password')
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (playername, email, password) VALUES (?, ?, ?)", (player_name, email, password))
    conn.commit()
    conn.close()
    return render_template('index.html', message="Account created successfully")


   #showing the table data
@app.route('/table_data', methods=['GET', 'POST'])
def table_data():
    conn = init_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template('table_data.html', data=users)  



#......................................................................................
#google se mili hui details yahan ayngi
#google se mili hui details yahan ayngi
google_client_id = "528397678148-72cmo157m7hdbrdd9oj0hkp54lnd3ico.apps.googleusercontent.com"
google_client_secret = "testing_code/google_auth_system/static/client_secret_528397678148-72cmo157m7hdbrdd9oj0hkp54lnd3ico.apps.googleusercontent.com.json"

#flow setup:google se baat karne k liye
flow=Flow.from_client_secrets_file(
    client_secrets_file=google_client_secret,
    scopes=["https://www.googleapis.com/auth/userinfo.profile","https://www.googleapis.com/auth/userinfo.email","openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)
#home route
@app.route('/')
def home():
    return render_template('index.html')

#route for login page
@app.route('/login')
def login_google():
    #user ko google ke login page pr bhejna
    authorization_url,state=flow.authorization_url()
    session['state']=state
    return redirect(authorization_url)

#callback route:google se response milne k baad
@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    #user ki informtion nikalna
    credentials=flow.credentials
    user_info_service=requests.get(
        'https://www.googleapis.com/userinfo/v2/me',
        headers={'Authorization':f'Bearer {credentials.token}'}
    ).json()
    #user ka data session m save krna
    session['google_id']=user_info_service.get('id')
    session["name"]=user_info_service.get("name")
    return render_template('index.html', name=session["name"])
 
# ...........................................................................................
if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(debug=True)
