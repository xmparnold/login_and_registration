from flask import Flask

app = Flask(__name__)
app.secret_key = 'secret'
DATABASE = 'login_and_registration_assignment'