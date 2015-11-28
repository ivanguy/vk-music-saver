#!/usr/bin/python3
import requests,json
from time import sleep
import os
import tkinter as tk
from tkinter import filedialog
from sys import argv
proxies = {
        "http":"http://proxy.ifmo.ru:3128",
        "https":"https://proxy.ifmo.ru:3128"
        }
token=open("../auth/token","r").read()
user_id=open("../auth/user_id","r").read()
debug =False
if 'd' in argv:
    debug=True

if __name__=="__main__":
    count=int(input("How many songs:\t"))
    offset=int(input("Skip that much:\t"))
    url = "https://api.vk.com/method/audio.get?owner_id={}&count={}&offset={}&access_token={}".format(user_id,count,offset,token)
    if input("Under ifmo proxy?(y,[n]):") in ('n','N','','NO','no','No'):
        response=requests.get(url)
    else:
        response=requests.get(url,proxies=proxies)
    response_dict = json.loads(response.text)
    if debug:
        print(response_dict)
    artists_list = []
    titles_list = []
    links_list = []
    number = 0
    for item in response_dict['response'][1:]:
        if debug:
            print(item)
        artists_list.append(item["artist"])
        titles_list.append(item["title"])
        links_list.append(item["url"])
        number += 1

    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    print("Saving to {}".format(path))
    print("Pending ",number," tracks")
    input("press any key...")


    #path = os.a"~/Music/vk/"
    if not os.path.exists(path):
        os.makedirs(path)

    for i in range(0,number):
        filename=path+os.path.sep+artists_list[i]+" - "+titles_list[i]+".mp3"
        if not os.path.exists(filename):
            print("Downloading: ",filename[len(path):])
            with open(filename, "wb") as out:
                response = requests.get(links_list[i].split("?")[0])
                out.write(response.content)
                print("...done")
        else:
            print("Skippin: ", filename[len(path):])
