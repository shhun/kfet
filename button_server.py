from flask import Flask, request, url_for, render_template
from passlib.hash import pbkdf2_sha256
import utils

app = Flask(__name__)

secret_hash = pbkdf2_sha256.hash("nikmosser")

@app.route('/')
def hello():
	return render_template("kfet.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if check_auth(request.form['password']):
			utils.toggle_state()
			return "Toggled state"
		return "Invalid password"

	else:
		return '''
			<form method="post">
            <p><input type=text name=password>
			<p><input type=submit value=Log>
        </form>
    '''

def	check_auth(password):
	return pbkdf2_sha256.verify(password, secret_hash)

