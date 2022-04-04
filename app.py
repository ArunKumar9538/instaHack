from flask import Flask,render_template,request
import requests
import json
from datetime import datetime

app = Flask(__name__)
@app.route("/")
@app.route("/home")
def home():
	return render_template("index.html")

@app.route("/result", methods=['POST',"GET"])
def result():
	output = request.form.to_dict()
	username = output["username"]
	password = output["password"]
	return render_template("index.html",error=login(username,password))

def login(username,password):
	link = 'https://www.instagram.com/accounts/login/'
	login_url = 'https://www.instagram.com/accounts/login/ajax/'
	time = int(datetime.now().timestamp())
	response = requests.get(link)
	csrf = response.cookies['csrftoken']
	payload = {
	    'username': username,
	    'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
	    'queryParams': {},
	    'optIntoOneTap': 'false'
	}
	login_header = {
	    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
	    "X-Requested-With": "XMLHttpRequest",
	    "Referer": "https://www.instagram.com/accounts/login/",
	    "x-csrftoken": csrf
	}
	try:
		login_response = requests.post(login_url, data=payload, headers=login_header)
		json_data = json.loads(login_response.text)
		if json_data["authenticated"]:
			return "Login sucessfull"
			# print("login successful : ",password)
			# cookies = login_response.cookies
			# cookie_jar = cookies.get_dict()
			# csrf_token = cookie_jar['csrftoken']
			# print("csrf_token: ", csrf_token)
			# session_id = cookie_jar['sessionid']
			# print("session_id: ", session_id)
			# exit(0)
		else:
			return "Invalid username or password"
	except Exception as e:
		return "Invalid username or password"
if __name__ == '__main__':
	app.run(debug=True,port=5001)