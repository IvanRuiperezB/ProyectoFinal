from flask import Flask, render_template, abort, request
import os
import requests
app = Flask(__name__)
key=os.environ["key"]
@app.route('/')
def inicio():
    return render_template("inicio.html")

@app.route('/players')
def players():
    URL_jugador="https://api.brawlstars.com/v1/players/%23"
    headers={'Authorization': f'Bearer {key}'}
    return render_template("players.html")
app.run("0.0.0.0",5000,debug=True)