# pip 3 install flask opencv-python This step requires a long time 15-20 minutes
import os
import cv2
import numpy as np
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads/'
PROCESSED_FOLDER = 'static/processed/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tif', 'tiff'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def processImage(filename, operation):
    print(f"the operation is {operation} and filename is {filename}")
    img = cv2.imread(f"static/uploads/{filename}")
    match operation :
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/processed/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename

        case "gaussian":
            imgProcessed = cv2.GaussianBlur(img, (5, 5), cv2.BORDER_DEFAULT)
            newFilename = f"static/processed/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename

    pass


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/itib1")
def itib1():
    return render_template("itib1.html")

@app.route("/itib2")
def itib2():
    return render_template("itib2.html")

@app.route("/itib3")
def itib3():
    return render_template("itib3.html")

@app.route("/itib4")
def itib4():
    return render_template("itib4.html")

@app.route("/itib5")
def itib5():
    return render_template("itib5.html")

@app.route("/taib1")
def taib1():
    return render_template("taib1.html")

@app.route("/taib2")
def taib2():
    return render_template("taib2.html")

@app.route("/taib3")
def taib3():
    return render_template("taib3.html")

@app.route("/taib4")
def taib4():
    return render_template("taib4.html")

@app.route("/taib5")
def taib5():
    return render_template("taib5.html")

@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


@app.route("/documents")
def documents():
    return render_template("documents.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template("index.html")
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return render_template("index.html")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            #file.save(os.path.join(app.config['/'], new))
            flash(f"Your image has been processed and is available <a href='/{new}' target='_blank' ></a>")
            # return redirect(url_for('uploaded_file',filename=filename))
            return render_template('index.html', filename=filename)
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            #return redirect(request.url)
            return render_template("index.html")


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/display2/<filename>')
def display_processed_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='processed/' + filename), code=301)

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'],
                               filename, as_attachment=True)


app.run(debug=True, port=5001)
