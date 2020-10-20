#!/usr/bin/python3
import yagmail
import mysql.connector
from flask import Flask, render_template, request , url_for , redirect ,session ,g 
from werkzeug.utils import secure_filename
from functools import wraps
import psutil
import pieMaker
import os
import pathlib

#mysql login 
mydb = mysql.connector.connect(
    host='localhost',
    user='admin',
    password='ThisIsMysqlLogin2020!',
    database='justGoShootDB'
)

app = Flask(__name__)
app.secret_key="7:b]&E3K~8?_UK[2"
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config["UPLOAD_PATH"] = "uploaded_images" #where finshed clinet photos go for a while



@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/gallery")
def gallery():
    return render_template('gallery.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/contactForm", methods=['POST'])
def contactForm():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    serviceDropDown = request.form['serviceDropDown']
    contactText = request.form['contactText']

    createEmail(name,email,phone,serviceDropDown,contactText)
    return render_template('contact.html')

@app.route("/client_login_page")
def client_login():
    return render_template('client_login_page.html')

@app.route("/admin_login_page")
def admin_login_page():
    return render_template('admin_login_page.html')

@app.route("/admin_login_post", methods=['POST'])
def admin_login():
    userName = request.form['user_name']
    userPassword = request.form['password']


    #lookup password user name in db
    #'admin'@'localhost' identified by 'ThisIsMysqlLogin2020!';
    #use justGoShootDB
    #create table users ( userName varchar(35), name varchar(35), password varchar(64) , admin varchar(1) )
    #niamh20399 | Niamh Meredith | password | 1

    mycursor = mydb.cursor()
    query = """select * from users where userName=%s  and password=%s and admin = 1 """
    mycursor.execute( query , (userName, userPassword))
    records = mycursor.fetchall()

    if len(records) == 1:
        session["admin"] = "admin"

        return render_template("admin_loged_in_page.html", admin= session["admin"], storage = storage() )
    
    return redirect(url_for('admin_login_page'))


@app.route("/admin_loged_in_page")
def loged_in_admin():
    if session.get("admin") == "admin":
        return render_template('admin_loged_in_page.html', admin = session.get("admin") , storage = storage() )
    return render_template('admin_login_page.html')

@app.route("/client_page")
def client_page():
    return render_template('client_page.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/photo_upload", methods=["POST"])
def photo_upload():
    name = request.form['user_name']
    folder_name = request.form['folder_name']
    email = request.form['email']
    images = request.files.getlist("images")
    print(name, folder_name, email)
    print(images)

    for image in images:
        #create dir on dec then add photos to it 
        imageName = secure_filename(image.filename)
        pathlib.Path(app.config['UPLOAD_PATH'], folder_name).mkdir(exist_ok=True)
        if imageName != "":
            imageExt = os.path.splitext(imageName)[1] 
            if imageExt not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            else:
                print(image)
                image.save(os.path.join(app.config['UPLOAD_PATH'] ,  folder_name , imageName))
    
    #decription is going to be folder name if same dec then goes into same folder


    return render_template('admin_loged_in_page.html', admin = session.get("admin") , storage = storage() )

def storage():
    hdd = psutil.disk_usage('/')
    pieMaker.createLogoPie()
    return {"diskSpaceRemainingGB" : ( hdd.free // 2**30) }


def createEmail(name,email,phone,serviceDropDown,contactText):
    try:
        yag = yagmail.SMTP(user="conornugent96@gmail.com" , password="putInLater")
        yag.send(to=email, subject=name + " , " + serviceDropDown, contents=contactText + "\n" + "\n Phone: " +  phone)
    except:
        print("error in sending email yell at Conor")


    


if __name__ == 'main':
        app.run(debug=True)