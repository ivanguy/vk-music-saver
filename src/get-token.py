#!/usr/bin/python3
import webbrowser
from flask import Flask
from time import sleep


app=Flask(__name__)
token=""
file_id="../auth/user_id"
file_token="../auth/token"
client_id="5164793"
get_token_uri="https://oauth.vk.com/authorize?client_id="+client_id+"&redirect_uri=http://localhost:6767/&display=page&scope=audio+offline&response_type=token&revoke=1"
server_addr=("",6767)

@app.route('/shutdown', methods=['POST'])
def shutdown_server():
    func=request.environ.get("werkzeug.server.shutdown")
    func()

@app.route("/", methods=["GET"])
def my_handle(access_token,expires_in,user_id):
    print(access_token)
    return "Now copy access_token value from address bar to console"

def valid_token():
    if not os.path.exists(file_id):
        os.makedirs(file_id)
    if not os.path.exists(file_token):
        os.makedirs(file_token)
    with open(file_token, 'r') as token_file:
        return token_file.readline()

def update_token():
    webbrowser.open(get_token_uri)
    sleep(1)
    token=input("copy access_token from browser address bar:")
    with open(file_token,'w') as token_file:
        token_file.write(token)
    with open(file_id, 'w') as id_file:
        id_file.write(input("copy user_id from browser:"))
    return

if __name__=="__main__":
    if not valid_token():
        update_token()
