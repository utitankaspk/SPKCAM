#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2,urllib
import webbrowser
import os
import random
import string
import json
import time
ID_FILENAME="login_session_token"
#URL="http://localhost:8080"
#URL="https://spksandbox.appspot.com"
URL="https://spkcloud.appspot.com"

ID_FILE=os.path.join(os.path.dirname(os.path.abspath(__file__)),ID_FILENAME)

#devuelve el string que se debe mandar al comunicarse con el servidor (con el nombre "spkcam_session_token") o None si no se inicio sesion. Nota: ya no es necesario mandar la variable 'author' al subir productos, el servidor lo saca de aqui.
def get_login_token():
    if not os.path.exists(ID_FILE):
        return None
    with open(ID_FILE,"r") as f: return f.read()
#devuelve el usuario con el cual esta iniciada la sesion, o None
def get_user():
    login_token=get_login_token()
    if login_token:
        url=URL+"/_cam/getuser"
        data=json.loads(urllib2.urlopen(url,urllib.urlencode({"login_token":login_token})).read())
        user= data.get("user",None)
        if user is None:
            os.remove(ID_FILE)
        return user
    return None
#abre una ventana del navegador para iniciar sesion, y devuelve el usuario con el que se inicio, o None si algo salio mal
def login():
    logout()
    url=URL+"/_cam/startlogin"
    data=json.loads(urllib2.urlopen(url,"").read())
    token=data["token"]
    browserpage=URL+"/spkcam/login?token=%s"%token
    webbrowser.open_new(browserpage)
    url=URL+"/_cam/checklogin"
    while True:
        time.sleep(2)
        data=json.loads(urllib2.urlopen(url,urllib.urlencode({"token":token})).read())
        if data["status"]=="invalid_token":
            return None
        elif data["status"]=="allowed":
            login_token=data["login_token"]
            with open(ID_FILE,"w") as f: f.write(login_token)
            return data["user"]
#cierra sesion con el usuario actual
def logout():
    login_token=get_login_token()
    if login_token is not None:
        url=URL+"/_cam/logout"
        urllib2.urlopen(url,urllib.urlencode({"login_token":login_token})).read()
        os.remove(ID_FILE)