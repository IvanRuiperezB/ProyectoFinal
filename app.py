from flask import Flask, render_template, abort, request
import os
import requests
app = Flask(__name__)
key=os.environ["key"]
@app.route('/')
def inicio():
    return render_template("inicio.html")

app.run("0.0.0.0",5000,debug=True)