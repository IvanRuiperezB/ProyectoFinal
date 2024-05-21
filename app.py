from flask import Flask, render_template, abort, request
import os
import requests
app = Flask(__name__)
key=os.environ["key"]
@app.route('/')
def inicio():
    return render_template("inicio.html")

@app.route('/players')
def jugadores():
    return render_template("players.html")

def jugador():
    URL_jugador="https://api.brawlstars.com/v1/players/%23"
    headers={'Authorization': f'Bearer {key}'}
    tag=request.form.get("player")
    r=requests.get(URL_jugador+tag,headers=headers)
    if r.status_code == 200:
        jugador=r.json()        
        return render_template("player.html")
    else:
        jugador=0
        return render_template("player.html",jugador=jugador)
app.run("0.0.0.0",5000,debug=True)