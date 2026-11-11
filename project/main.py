import os
import json
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

# a route
@app.route('/')
def index():
    return render_template("index.html")

@app.route("/thank_form_two")
def thank_you_two():

    return render_template("thankyou_form_rev.html", 
                           imgPath = "../synthesized.png")

app.run(debug = True)