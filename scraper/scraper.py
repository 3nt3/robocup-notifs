import requests
import toml
import sys
import time
import os

try:
    config = toml.load(open('config.toml'))
except Exception as e:
    print(e)
    exit(1)

login_body = {}
token = ''

username, password, url = config['username'], config['password'], config['url']

if len(sys.argv) > 1 and sys.argv[1] == '--get-token':

    login_r = requests.post(f"{url}/login/token.php?service=moodle_mobile_app",
                            {"username": username, "password": password})

    login_body = login_r.json()
    if login_body.get('error'):
        print(
            f"login failed with error, status code {login_r.status_code}. \n{login_body}")
        exit(1)
    token = login_body['token']
    print(token)
    exit()

else:
    try:
        token = config['token']
    except KeyError:
        print('add token to config.toml or username/password with --get-token flag')
        exit(1)

# print(f"login successful! token: {token}, privatetoken: {privatetoken}")

last_n = -2
while True:
    course_data = {
        "wstoken": token,
        "wsfunction": "core_course_get_contents",
        "moodlewsrestformat": "json",
        "courseid": 380
    }

    course_r = requests.get(f"{url}/webservice/rest/server.php", course_data)

    soccer_dict = list(
        filter(lambda x: x['name'] == 'Soccer', course_r.json()))[0]
    open_international_contents = list(
        filter(lambda x: x['name'] == 'Open International', soccer_dict['modules']))[0]['contents']

    n = len(open_international_contents)
    if n > last_n and last_n != -1:
        print("NEW STUFF JUST DROPPED!!")
        os.system("notify-send 'NEW STUFF JUST DROPPED'")
        print(open_international_contents[n-1])

    last_n = n
    time.sleep(300)
