import os, shutil, psutil
import json
from flask import Flask, request, redirect, url_for, render_template, jsonify, session
import heeger_bergen
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB limit

app.secret_key = 'BAD_SECRET_KEY' # needed to sign the session cookie ( uses a placeholder like this for testing)

# Adapted from: Skyla 
# build the info session dictionary: this visitor's session values + live system stats
def read():
    info = {
        "clicks": session.get("clicks", 0),
        "tab_leaves": session.get("tab_leaves", 0),
        "first_visit": session.get("first_visit"),
        "city": session.get("city"),
        "region": session.get("region"),
        "org": session.get("org"),
    }

    # live stats are not saved, they are measured fresh each time from js 
    info.update({
        "ram_free_gb": round(psutil.virtual_memory().available / 1e9, 1), # turns into gb and rounds to nearest 10th 
        "ram_total_gb": round(psutil.virtual_memory().total / 1e9, 1), # ''
        "disk_free_gb": round(shutil.disk_usage(os.path.expanduser("~")).free / 1e9, 1),
        "disk_total_gb": round(shutil.disk_usage(os.path.expanduser("~")).total / 1e9, 1),
    })
    return info



@app.route('/')
def index():
    if "first_visit" not in session:  # first visit from this browser, only saved once
        session["first_visit"] = datetime.now().isoformat(timespec="seconds")
    count, output = counter()    
    heeger_bergen.execute(count)
    return render_template("index.html", 
                           output=output,
                           info=read())

# Handle past uploaded images
@app.route('/pastUploads')
def pastUploads():
    img_list = os.listdir(app.config['UPLOAD_FOLDER'])
    app.logger.info(img_list)
    return img_list

def counter():
    # Adapted from: Source - https://stackoverflow.com/a/29733650
    # Posted by MikeTGW
    # Retrieved 2026-11-25, License - CC BY-SA 3.0

    with open( "count.txt", "r" ) as f:
        count = f.read()

    output = "The webpage has been accessed {count} times.".format(count=count)

    count = int(count)
    with open( "count.txt", "w" ) as f:
        f.write( str(count+1) )

    return count, output

# # Add one to an event (clicks or tab_leaves), store in the session, return totals
# @app.route("/log", methods=["POST"])
# def log():
#     event = (request.get_json(silent=True) or {}).get("event")
#     if event in ("clicks", "tab_leaves"):  # ignore anything else
#         session[event] = session.get(event, 0) + 1
#     return jsonify(read())

# @app.route("/log")
# def log():
#     print(request)
#     read()
#     return("returning")

# Read-only route for the buttons (does not count as a click)
@app.route("/info")
def info_route():
    return jsonify(read())


# The page refreshes location and network details on each load and posts them here.
@app.route("/location", methods=["POST"])
def location():
    data = request.get_json(silent=True) or {}
    session["city"] = data.get("city")
    session["region"] = data.get("region")
    session["org"] = data.get("org")

    return jsonify(read())

# app.run(debug = True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port="port")

