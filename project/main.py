import os
import json
from flask import Flask, request, redirect, url_for, render_template
import heeger_bergen

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB limit

@app.route('/')
def index():
    count, output = counter()    
    heeger_bergen.execute(count)
    return render_template("index.html", 
                           output=output)

# @app.route("/catForm",methods = ['POST'])
# def catForm():
#     #key is the same as in the form :)
#     uploadedfile = request.files['the_file']
#     #save file to uploads folder
    # uploadedfile.save(os.path.join(app.config['UPLOAD_FOLDER'],uploadedfile.filename)) # writes the bytes to disk
#     app.logger.info(uploadedfile.filename)
#     return json.dumps({"filename": uploadedfile.filename})

# Handle past uploaded images
@app.route('/pastUploads')
def pastUploads():
    img_list = os.listdir(app.config['UPLOAD_FOLDER'])
    app.logger.info(img_list)
    return img_list

def counter():
    # Source - https://stackoverflow.com/a/29733650
    # Posted by MikeTGW
    # Retrieved 2026-11-25, License - CC BY-SA 3.0

    with open( "count.txt", "r" ) as f:
        count = f.read()

    output = "The webpage has been accessed {count} times.".format(count=count)

    count = int(count)
    with open( "count.txt", "w" ) as f:
        f.write( str(count+1) )

    return count, output

app.run(debug = True)

