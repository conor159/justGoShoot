#!/usr/bin/python3
import yagmail
import mysql.connector
from flask import Flask, render_template, request , url_for , redirect ,session ,g  , flash , send_from_directory  ,send_file
from werkzeug.utils import secure_filename
from functools import wraps
import psutil
import pieMaker
import os
import pathlib
import datetime
import bcrypt
import random

#mysql login 
mydb = mysql.connector.connect(
    host='localhost',
    user='admin',
    password='ThisIsMysqlLogin2020!',
    database='justGoShootDB'
)

#app = Flask(__name__)
app = Flask(__name__, instance_path='/home/conor/justGoShoot/justGoShoot/uploaded_images')
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

    if( name== "" or folder_name == "" or email == "" ):
        #implement later
        flash("missing parameter(s)")
        return render_template('admin_loged_in_page.html', admin = session.get("admin") , storage = storage() )

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
                image.save(os.path.join(app.config['UPLOAD_PATH'] ,  folder_name , imageName))

    addUserToDB(name,folder_name,email)
    return render_template('admin_loged_in_page.html', admin = session.get("admin") , storage = storage() )


@app.route("/uploaded_images/<folderName>/<fileName>" )
def uploaded_images(folderName, fileName):
    return send_from_directory( os.path.join(app.instance_path, folderName), fileName )


















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


def addUserToDB(name, folder_name, email):
    mycursor = mydb.cursor()
    pubDate = datetime.datetime.now() 
    #rand here
    pin = random.randint(1,10000)
    pin = genPassword(str(pin))

    query = """insert into finshedProjects (user_name, user_email,  pubDate , published, pin , folder_name)  values  (%s, %s ,%s, %s, %s, %s )"""
    vals = ( name,  email , pubDate ,"0", pin, folder_name)
    mycursor.execute( query , vals ) 
    mydb.commit()
    print("added "+ folder_name  +" to finshed projects")
    

def genPassword(pin):
    pin = pin.encode('utf-8')
    return bcrypt.hashpw(pin, bcrypt.gensalt(12))

def checkPassword(proviededPin, hashedPassword):
    return bcrypt.checkpw(proviededPin, hashedPassword )

if __name__ == 'main':
        app.run(debug=True)