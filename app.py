from flask import Flask, render_template, abort, request, redirect, url_for
import os
import requests
import datetime

def convertir_fecha(fecha_str):
    return datetime.datetime.fromisoformat(fecha_str[:-5])
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
        miembros=len(clubinfo["members"])
        return render_template("club.html",clubinfo=clubinfo,miembros=miembros)

@app.route('/brawlers', methods=["POST","GET"])
def brawlers():
    if request.method=="GET":
        brawlers=1
        return render_template("brawlers.html",brawlers=brawlers)
    else:
        URL="https://api.brawlstars.com/v1/brawlers/"
        busqueda=request.form.get("busqueda")
        busq=busqueda.lower()
        r=requests.get(URL,headers=headers)
        if r.status_code == 200:
            resultado=r.json()
            brawlers=[]
            for brawler in resultado["items"]:
                nombre=brawler["name"].lower()
                if nombre.startswith(busq):
                    brawlers.append(brawler)
            if len(brawlers) == 0:
                brawlers=0
            return render_template("brawlers.html",brawlers=brawlers,busqueda=busqueda)

@app.route('/games')
def games():
    URL="https://api.brawlstars.com/v1/events/rotation"
    fecha_actual = datetime.datetime.utcnow()
    r=requests.get(URL,headers=headers)
    if r.status_code == 200:
        eventos=r.json()
        actuales=[]
        proximos=[]
        for evento in eventos:
            inicio=convertir_fecha(evento["startTime"])
            fin=convertir_fecha(evento["endTime"])
            if inicio <= fecha_actual <= fin:
                actuales.append(evento)
            elif inicio > fecha_actual:
                proximos.append(evento)
        return render_template("games.html",proximos=proximos,actuales=actuales)


port=os.environ["PORT"]
app.run("0.0.0.0",int(port),debug=False)