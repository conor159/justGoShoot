#!/usr/bin/python3
import yagmail
import mysql.connector
from flask import Flask, render_template, request , url_for , redirect ,session ,g  , flash , send_from_directory  ,send_file
from werkzeug.utils import secure_filename
from functools import wraps
import psutil
import pieMaker
import os
from os import  listdir
import pathlib
import time
import bcrypt
import random
import json
import string

#mysql login 
mydb = mysql.connector.connect(
    host='localhost',
    user='admin',
    password='ThisIsMysqlLogin2020!',
    database='justGoShootDB'
)
cursor = mydb.cursor(buffered=True)

#app = Flask(__name__)
app = Flask(__name__, instance_path='/home/conor/justGoShoot/justGoShoot/uploaded_images')
app.secret_key="7:b]&E3K~8?_UK[2"
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config["UPLOAD_PATH"] = "uploaded_images" #where finshed clinet photos go for a while



@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/gallary")
def gallery():
    if session.get("admin"):
        request.args.get("folder_name")
        return render_template('gallary_admin.html')

    return render_template('gallary.html')


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

    contactEmail(name,email,phone,serviceDropDown,contactText)

    

    return render_template('contact.html')

@app.route("/client_login_page")
def client_login():
    return render_template('client_login_page.html')

@app.route("/admin_login_page")
def admin_login_page():
    if session.get('admin') == "admin":
        return render_template('admin_loged_in_page.html', admin = session.get("admin") , storage = storage() )

    return render_template('admin_login_page.html')

@app.route("/admin_login_post", methods=['POST'])
def admin_login():
    email = request.form['email']
    userPassword = request.form['password']

    #lookup password user name in db
    #'admin'@'localhost' identified by 'ThisIsMysqlLogin2020!';
    #use justGoShootDB
    #create table users ( userName varchar(35), name varchar(35), password varchar(64) , admin varchar(1) )
    #niamh20399 | Niamh Meredith | password | 1

    mycursor = mydb.cursor()
    query = """select * from users where email=%s  and password=%s and admin = 1 """
    mycursor.execute( query , (email, userPassword))
    records = mycursor.fetchall()

    if len(records) == 1:
        session["admin"] = "admin"
        return render_template("admin_loged_in_page.html", admin= session["admin"], storage = storage() )
    
    flash("Incorect email or password")
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
    folder_name = request.form['folder_name']
    email = request.form['email']
    images = request.files.getlist("images")

    if email  == "" or folder_name == "" :
        #implement later
        flash("missing parameter(s)")
        return render_template('admin_loged_in_page.html', admin = session.get("admin") , storage = storage() )

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

    addEnteryToFinProjects(folder_name,email)
    return render_template('admin_loged_in_page.html', admin = session.get("admin") , storage = storage() )


@app.route("/uploaded_images/<folderName>/<fileName>" )
def uploaded_images(folderName, fileName):
    if session.get("admin") == "admin":
        return send_from_directory( os.path.join(app.instance_path, folderName), fileName )

    else:
        return ""



@app.route("/fin_projects_json",  methods=["GET"])
def fin_projects_json():
    folderName = request.args.get('folder_name')

    #return a list of files in folder 
    if session.get("admin") == "admin" and folderName:
        filesList = listdir( os.path.join(app.config['UPLOAD_PATH'] , folderName ))
        fileListJson = json.dumps(filesList)
        return fileListJson


    # return all users info and thumbnail
    if session.get("admin") == "admin":
        users = []
        #table stuff

        finCursor = mydb.cursor()
        query = """  select u.name, u.phone, fin.pubDate, fin.folder_name, fin.published from users as u , finshedProjects as fin where u.userId = fin.userId """
        finCursor.execute( query )
        records = finCursor.fetchall()

        for record in records:  
            filesList = listdir( os.path.join(app.config['UPLOAD_PATH'] , record[3] ))
            user = {
                "userName" : record[0],
                "phone" : record[1],
                "pubDate" : record[2],
                "folderName" : record[3],
                "published" : record[4],
                "files" :  filesList[0]
            }
            users.append(user)

        userJson = json.dumps(users)
        finCursor.close()
        return userJson
    # where will later return user photos if published and pin is correct
    return "auth error"


@app.route("/publish", methods=['POST'])
def publish():
    #need to pass text on here
    emailText = ""
    if session.get("admin") == "admin":
        folderName = request.form['folder_name']
        mycursor = mydb.cursor()
        val = ( folderName,) #grrr tupple with only one item needs a , mysql excute requires tups
        query = " update finshedProjects set published = 1 where folder_name = %s "
        mycursor.execute( query , val)
        mydb.commit()


        query = """ select email from users where userID = (     select   userID from finshedProjects where folder_name = %s limit 1 ) """
        mycursor.execute( query , val)
        userEmail = mycursor.fetchone()
        userEmail = userEmail[0]

        mydb.free_result()
        publishEmail(userEmail, folderName )

        
    return ""




def publishEmail( userEmail, folderName):
    #createGalLink()
    emailText = ""
    try:
        yag = yagmail.SMTP(user="conornugent96@gmail.com" , password="putInLater")
        yag.send( to=userEmail, subject="Just Go Shoot" ,   contents=emailText  )
    except:
        print("error in sending email yell at Conor")



@app.route("/create_user", methods=['POST'])
def createUser():
    userEmail = request.form['new_user_email']
    userName = request.form['new_user_name']
    userPhone = request.form['new_user_phone']
    if userEmail =="" or userName == "" :
        return "enter email and name "

    letters = string.ascii_letters
    userID =  ( ''.join(random.choice(letters) for i in range(32)) )
    tempPassword =  ( ''.join(random.choice(letters) for i in range(12)) )
    tmpPassword = genPassword(tempPassword)

    mycursor = mydb.cursor()
    query = """ insert into  users  (email , name,  password,  admin,   userID, phone) values   ( %s, %s, %s ,%s, %s, %s )"""
    mycursor.execute( query , (userEmail, userName, tempPassword, 0,  userID , userPhone))
    mydb.commit()
    mycursor.close() 
    flash(" Created New User: " + userEmail)
    return redirect(url_for("admin_login_page"))








@app.route("/get_users", methods=['GET'])
def getUsers():
    if session["admin"] == "admin":
        #return json with all user detales
        mycursor = mydb.cursor()
        query = """ select users.email , users.name, users.phone from users """
        mycursor.execute( query )
        records = mycursor.fetchall()
        users = []
        for record in records:  
            user = {
                "email" : record[0],
                "name" : record[1],
                "phone" : record[2]
            }
            users.append(user)

        userJson = json.dumps(users)
        mycursor.close()
        return  userJson
    return "auth error"





def storage():
    hdd = psutil.disk_usage('/')
    pieMaker.createLogoPie()
    return {"diskSpaceRemainingGB" : ( hdd.free // 2**30) }


def contactEmail(name,email,phone,serviceDropDown,contactText):
    try:
        yag = yagmail.SMTP(user="conornugent96@gmail.com" , password="putInLater")
        yag.send(to=email, subject=name + " , " + serviceDropDown, contents=contactText + "\n" + "\n Phone: " +  phone)
    except:
        print("error in sending email yell at Conor")


def addEnteryToFinProjects( folder_name, email):
    mycursor = mydb.cursor()
    pubDate = time.time()
    #rand here

    query = """select users.userID  from users where email  =  %s  """
    mycursor.execute( query , (email,) ) 
    userID = mycursor.fetchone()
    userID = userID[0]

    query = """insert into finshedProjects ( userID,  pubDate , published,  folder_name)  values  (%s, %s, %s, %s )"""
    vals = (   userID , pubDate ,"0",  folder_name)
    mycursor.execute( query , vals ) 
    mydb.commit()
    mycursor.close()

    #print("added "+ folder_name  +" to finshed projects")
    

def genPassword(password):
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt(12))

def checkPassword(providedPassword, hashedPassword):
    return bcrypt.checkpw(proviedPassword, hashedPassword )

if __name__ == 'main':
        app.run(debug=True)