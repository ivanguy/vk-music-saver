#!/usr/bin/python3
import os
import requests
from selenium import webdriver
import json
from pathlib import Path

token=""
user_id=""
file_id=Path("../auth/user_id")
file_token=Path("../auth/token")
client_id="5164793"
get_token_uri = "https://oauth.vk.com/authorize" \
                "?client_id="+client_id+ \
                "&redirect_uri=http://localhost:6767/" \
                "&display=page&" \
                "scope=audio+offline" \
                "&response_type=token" \
                "&revoke=1"

wdriver=webdriver.Firefox()
wdriver.get(get_token_uri)
email=input("Email:\t")
password=input("Pswrd:\t")
wbriver.find_element_by_name("email").send_keys(email)
wbriver.find_element_by_name("pass").send_keys(password)
wbriver.find_element_by_id("install_allow").click()
redirect_uri=wdriver.current_url
print(redirect_uri)
exit()



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
