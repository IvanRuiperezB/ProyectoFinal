from flask import Flask, render_template, abort, request
import os
app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template("inicio.html")
