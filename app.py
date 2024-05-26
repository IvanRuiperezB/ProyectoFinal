from flask import Flask, render_template, abort, request, redirect, url_for
import os
import requests
app = Flask(__name__)
key=os.environ["key"]
headers={'Authorization': f'Bearer {key}'}
@app.route('/')
def inicio():
    return render_template("inicio.html")

@app.route('/players')
def players():
    return render_template("players.html")

@app.route('/player',methods=["POST"])
def player():
    player = request.form.get("player")
    return redirect(url_for('perfil', player=player))

@app.route('/player/<player>')
def perfil(player):
    URL_jugador="https://api.brawlstars.com/v1/players/%23"
    r=requests.get(URL_jugador+player,headers=headers)
    if r.status_code == 200:
        jugador=r.json()
        brawlers=len(jugador["brawlers"])
        club=len(jugador["club"])
        victorias=jugador["3vs3Victories"]+jugador["soloVictories"]+jugador["duoVictories"]
        return render_template("player.html",jugador=jugador,brawlers=brawlers,club=club,victorias=victorias)
    else:
        jugador=0
        return render_template("player.html",jugador=jugador)

@app.route('/club/<club>')
def club(club):
    URL_club="https://api.brawlstars.com/v1/clubs/%23"
    request=requests.get(URL_club+club,headers=headers)
    if request.status_code == 200:
        clubinfo=request.json()
        return render_template("club.html",clubinfo=clubinfo)
    else:
        clubinfo=0
        return render_template("club.html",clubinfo=clubinfo)
app.run("0.0.0.0",5000,debug=True)