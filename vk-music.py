#!/usr/bin/python3
import os,requests,json
import tkinter as tk
from tkinter import filedialog
from time import sleep
from selenium import webdriver
from threading import Lock

token=""
user_id=""
auth_dir="auth/"
id_path=os.path.abspath(auth_dir+'user_id')
token_path=os.path.abspath(auth_dir+'token')
get_token_uri = "https://oauth.vk.com/authorize" \
    "?client_id=5164793" \
    "&redirect_uri=http://oauth.vk.com/blank.html" \
    "&display=page&" \
    "scope=audio+offline" \
    "&response_type=token" \
    "&revoke=1"
proxies = {"http":"http://proxy.ifmo.ru:3128",
           "https":"https://proxy.ifmo.ru:3128"}

def valid_token():
    """Check if files with tokens exist
    """
    global token, user_id
    if not os.path.exists(auth_dir):
        os.makedirs(auth_dir)
    if os.path.exists(token_path):
        with open(token_path, 'r') as token_file:
            token=token_file.readline()
        with open(id_path, 'r') as id_file:
            user_id=id_file.readline()
        return token
    return False

def update_token():
    """Get new access token and rewrite to disk
    and global vars
    """
    global token, user_id
    wdriver = webdriver.Firefox()
    wdriver.get(get_token_uri)
    while True:
        input("Give access, then press any key...")
        redirect_uri = wdriver.current_url
        if "access_token" in redirect_uri:
            break
    if args.debug:
        print(redirect_uri)
    wdriver.close()
    
    token, _, user_id = redirect_uri.split('#')[1].split('&')
    token, user_id= [x.split('=')[1] for x in (token,user_id)]
    if args.debug:
        print(token, user_id)

    with open(token_path, 'w') as token_file:
        token_file.write(token)
    with open(id_path, 'w') as id_file:
        id_file.write(user_id)
    return 1

def is_valid_dir(parser, arg):
    """Check if arg is a valid directory that already exists on the file
       system. Raises proper parser error.
    """
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The folder {} does not exist!".format(arg))
    else:
        return arg

def make_parser():
    """Wrap parser configuration if func for readability.
    """
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Save audio from vk.com\n" \
            "To get token authorize on promt.")
    parser.add_argument('path', action='store',
            type=lambda x: is_valid_dir(parser, x),
            help='directory for songs')
    parser.add_argument('songs', help='how many song to download')
    parser.add_argument('-s','--skip', default=0,
            help='skip that many from beginning of your playlist')
    parser.add_argument('-n', '--new', default=False, action='store_true',
            help='get new access token')
    parser.add_argument('-p', '--proxy', default=False, action='store_true',
            help='use proxy.ifmo.ru')
    parser.add_argument('-d', '--debug', default=False, action='store_true')
    return parser



if __name__=="__main__":
    args=make_parser().parse_args()
    if valid_token():
        if args.new:
            update_token()
    else:
        update_token()
    if args.debug:
        print("token:\t",token)
        print("id:\t",user_id)

    url = "https://api.vk.com/method/audio.get?owner_id={}&count={}&offset={}" \
          "&access_token={}".format(user_id, args.songs, args.skip, token)
    if args.proxy:
        response=requests.get(url,proxies=proxies)
    else:
        response=requests.get(url)
    response_dict = json.loads(response.text)
    if args.debug:
        print(response_dict)
    artists_list = []
    titles_list = []
    links_list = []
    number = 0
    for item in response_dict['response'][1:]:
        if args.debug:
            print(item)
        artists_list.append(item["artist"])
        titles_list.append(item["title"])
        links_list.append(item["url"])
        number += 1

    #root = tk.Tk()
    #root.withdraw()
    #path = filedialog.askdirectory()
    print("Saving to {}".format(args.path))
    print("Pending ",number," tracks")
    input("press any key...")

    dwnldd = 0
    skpd = 0
    kbdsig=False
    for i in range(0,number):
        if kbdsig:
            break
        song_name=artists_list[i]+'-'+titles_list[i]+'.mp3'
        song_name=song_name.replace('/','')
        filename=args.path + os.path.sep + song_name
        filename.strip("/")
        if not os.path.exists(filename):
            print("[{}/{}]Downloading:\t{}".format(i+1,number,filename[len(args.path):]))
            try:
                with open(filename, "wb") as out:
                    response = requests.get(links_list[i].split("?")[0])
                    out.write(response.content)
                    print("...done")
                    dwnldd+=1
            except KeyboardInterrupt as e:
                print("Waiting for download...")
                kbdsig=True
                
        else:
            print("Skippin: ", filename[len(args.path):])
            skpd+=1
    print("Downloaded:\t",dwnldd)
    print("Skipped:\t",skpd)
