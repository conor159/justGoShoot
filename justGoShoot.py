#!/usr/bin/python3
import yagmail
#import mysql.connector
from flask import Flask, render_template, request , url_for , redirect ,session ,g  , flash , send_from_directory  ,send_file, make_response , Response
from werkzeug.utils import secure_filename
from functools import wraps
import pieMaker
import os
from os import  listdir
import pathlib
import time
import bcrypt
import random
import json
import string
import psutil
from  flask_mysqldb import  MySQL


#app = Flask(__name__)
app = Flask(__name__, instance_path='/home/conor/justGoShoot/justGoShoot/uploaded_images')
app.secret_key="7:b]&E3K~8?_UK[2"
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config["UPLOAD_PATH"] = "uploaded_images" #where finshed clinet photos go for a while

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'ThisIsMysqlLogin2020!'
app.config['MYSQL_DB'] = 'justGoShootDB'
mydb = MySQL(app)

adminEmail = "conornugent96@gmail.com"
emailPassword = "put back in in prod "
justGoShootLink  = "http://127.0.0.1:5000"



#todos need to check redirect endpoint things
#need to create a delete function for old projects

#need to do testing 
#need to have some sort of external file thing
#block same folder entery

#current --------------------------
#double photo upload error is a thing
#add bufferd to everthing


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

    contactText  = contactText + "\n" +  "Name: " +  name + "\n Phone: " +  phone + "\n Email:" +  email

    contactEmail(email, name + " " + phone , contactText )
    return render_template('contact.html')

@app.route("/client_login_page")
def client_login():

    return render_template('client_login_page.html')

@app.route("/admin_login_page")
def admin_login_page():
    if userIsAdmin(request.cookies.get("userID")):
        return redirect(url_for('loged_in_admin', storage = storage() ))

    if request.cookies.get("userID"):
        return redirect(url_for('user_gallery'))

    return render_template('admin_login_page.html')

@app.route("/admin_login_post", methods=['POST'])
def admin_login():
    #'admin'@'localhost' identified by 'ThisIsMysqlLogin2020!';
    #use justGoShootDB
    userPassword = ""
    email = request.form['email']
    userPassword = request.form['password']
    userIDCookie = request.cookies.get("userID")
    mycursor = mydb.connect.cursor()

    query = """select email , name , phone , eircode , county , addr3 , addr2 , addr1 , password  , admin , userID from users where email=%s    """
    mycursor.execute( query , (email,))
    record = mycursor.fetchone()
    hashedPasswordMatch = checkPassword(userPassword, record[8])
    

    if record[9] == "1" and hashedPasswordMatch: 
        resp =  make_response( render_template("admin_loged_in_page.html",  storage = storage() ))
        resp.set_cookie("userID", record[10] )
        return resp

    if hashedPasswordMatch:
        resp =  make_response(redirect(url_for("user_gallery")))
        resp.set_cookie("userID", record[10] )
        return resp

    return redirect(url_for("admin_login_page"))





@app.route("/user_gallery")
def user_gallery():
    userID = request.cookies.get("userID")
    if userPubList(userID):
        return render_template("user_gallery.html")
    return redirect(url_for("index"))





@app.route("/admin_loged_in_page")
def loged_in_admin():
    if userIsAdmin(request.cookies.get("userID")):
    #userID is admin
        return render_template('admin_loged_in_page.html',  storage = storage() )
    return render_template('admin_login_page.html')

@app.route("/client_page")
def client_page():
    return render_template('client_page.html')




@app.route("/logout")
def logout():
    response  = make_response(render_template("index.html"))
    response.set_cookie("userID", expires=0)
    return response







@app.route("/photo_upload", methods=["POST"])
def photo_upload():
    folder_name = request.form['folder_name']
    email = request.form['email']
    images = request.files.getlist("images")

    if email  == "" or folder_name == "" :
        #implement later
        flash("missing parameter(s)")
        return render_template('admin_loged_in_page.html',  storage = storage() )

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
    return render_template('admin_loged_in_page.html',  storage = storage() )


@app.route("/uploaded_images/<folderName>/<fileName>" )
def uploaded_images(folderName, fileName):
    #user is authed for folder stop bothering mysql
    if session.get(folderName):
        return send_from_directory( os.path.join(app.instance_path, folderName), fileName )

    #check to see if user is autherised to view this folder if so create session
    userID = request.cookies.get("userID")
    mycursor = mydb.connect.cursor()
    query = """ select userID  from finshedProjects where folder_name = %s  and userID = %s  and published = %s  """
    mycursor.execute(query,(folderName, userID, "1"))
    record = mycursor.fetchone()

    if userID == record[0]:
        session[folderName] = folderName
        print("fileName: ", fileName)
        mycursor.close()
        return send_from_directory( os.path.join(app.instance_path, folderName), fileName )

    elif userIsAdmin(userID):
        #lets admin view non published files put in last 
        mycursor.close()
        return send_from_directory( os.path.join(app.instance_path, folderName), fileName )

    mycursor.close()
    return ""


@app.route("/fin_projects_json",  methods=["GET"])
def fin_projects_json():
    folderName = request.args.get('folder_name')
    #return a list of files in folder  if supliyed a folder name
    admin = userIsAdmin(request.cookies.get("userID")) 
    if admin and folderName:
        filesList = listdir( os.path.join(app.config['UPLOAD_PATH'] , folderName ))
        fileListJson = json.dumps(filesList)
        return fileListJson

    listOfAuthFolders = userPubList(request.cookies.get("userID"))
    # get a list of folders that the user is autherised to view 
    if listOfAuthFolders: 
        folders = []
        #print(listOfAuthFolders)
        for folder in listOfAuthFolders:
            #go though the folders and return json 
            filesList = listdir( os.path.join(app.config['UPLOAD_PATH'] , folder ))
            folderDict = {
                "folderName" : folder,
                "files" :  filesList
            }
            folders.append(folderDict)
        fileListJson = json.dumps(folders)
        return fileListJson

    # return all users info and thumbnail
    if admin:
        users = []
        #table stuff

        mycursor = mydb.connect.cursor()
        query = """  select u.name, u.phone, fin.pubDate, fin.folder_name, fin.published , u.email from users as u , finshedProjects as fin where u.userId = fin.userId """
        mycursor.execute( query )
        records = mycursor.fetchall()
        for record in records:  
            filesList = listdir( os.path.join(app.config['UPLOAD_PATH'] , record[3] ))
            user = {
                "userName" : record[0],
                "phone" : record[1],
                "pubDate" : record[2],
                "folderName" : record[3],
                "email" :  record[5],
                "published" : record[4],
                "files" :  filesList[0]
            }
            users.append(user)

        userJson = json.dumps(users)
        mycursor.close()
        return userJson
    # where will later return user photos if published and pin is correct
    return "auth error"


@app.route("/publish", methods=['POST'])
def publish():
    #need to pass text on here
    emailText = ""
    if userIsAdmin(request.cookies.get("userID")):
        folderName = request.form['folder_name']
        mycursor = mydb.connect.cursor()
        val = ( folderName,) #grrr tupple with only one item needs a , mysql excute requires tups
        query = " update finshedProjects set published = 1 where folder_name = %s "
        mycursor.execute( query , val)
        mydb.commit()


        query = """ select email   from users where userID = (     select   userID from finshedProjects where folder_name = %s limit 1 ) """
        mycursor.execute( query , val)
        userEmail = mycursor.fetchone()
        userEmail = userEmail[0]
        
    return ""




def publishEmail( userEmail, userName):
    nemailText = "Hi there " + userName + "your photos are avalable on Just Go Shoot where you can \n view and download them here once you create an account"
    try:
        yag = yagmail.SMTP(user= adminEmail , password=emailPassword)
        yag.send( to=userEmail, subject="Just Go Shoot" ,   contents=emailText  )
    except:
        print("error in sending email yell at Conor")
    return





@app.route("/create_user", methods=['POST'])
def createUser():
    if userIsAdmin(request.cookies.get("admin")):
        userEmail = request.form['new_user_email']
        if userEmail == "":
            return "enter user email"

        token = randString()
        createSetupToken( userEmail, token)
        #creates a link and entery in db that will be deleteed once user creates first login 

        #need to setup firstLogin endpoint
        setupLink =' <a href =' + "'" + justGoShootLink + "/first_login?token=" + token  + "'"  + '> here</a>.'
        subjectText = "Setup for Just Go Shoot"
        content = "Click the link below to create an account so you can access your photos once they are published " + setupLink
        sendToUserEmail( userEmail, subjectText, content)

        return redirect(url_for("admin_login_page"))
    return redirect(render_template('index.html'))



def getUserRecordByID(userID):
        mycursor = mydb.connect.cursor()()
        query = """select email , name , phone , eircode , county, addr3 , addr2 , addr1, password , admin , userID  from users where userID=%s    """
        mycursor.execute(query, (userID,) )
        record = mycursor.fetchone()
        mycursor.close()
        return record


def userIsAdmin(userID):
    query = """select admin from users where userID=%s    """
    mycursor = mydb.connect.cursor()
    mycursor.execute(query, (userID,) )
    record = mycursor.fetchone()
    #userRecord =  getUserRecordByID(userID)
    #fix without row index later 
    if not record:
        return False
    if record[0] == '1':
        return True
    return False


def userPubList(userID):
        mycursor = mydb.connect.cursor()
        query = """ select  folder_name from finshedProjects where userID = %s and published = %s """
        mycursor.execute(query, (userID, "1"))
        record = mycursor.fetchall()
        folders = [ x[0] for x in record]
        mycursor.close()
        return folders


def randString():
    letters = string.ascii_letters
    numbers = string.hexdigits

    alfaNum = (letters , numbers)
    longRandString =  ( ''.join(random.choice(letters) for i in range(128)) )
    return longRandString



def createSetupToken(email , token):
    mycursor = mydb.connect.cursor()
    query = """insert into setupTokens ( email , token ) values (  %s , %s)"""
    mycursor.execute( query , (email, token))
    mydb.commit()



@app.route("/first_login", methods=["GET"])
def firstLogin():
    #lookup db to see if link they clicked in email has a matching email
    token  = request.args.get("token")
    mycursor = mydb.connect.cursor()()
    query = """select email, token from setupTokens where token = %s """
    mycursor.execute( query , (token,))
    tokenResult = mycursor.fetchone()

    if  tokenResult  == None :
        return redirect(url_for('index'))

    if tokenResult[1] == token:
        #right if the token matches send the user over to create a account
        session["createAccount"] = token
        return redirect( url_for("createAccount"))

    #otherwide send them off to homepage
    return redirect( url_for("index"))

@app.route("/create_account")
def createAccount():
    if session.get('createAccount'):
        return render_template("create_account.html")
    return redirect(url_for("index"))

       


'''
@app.route("/get_users", methods=['GET'])
def getUsers():
    if userIsAdmin(request.cookies.get("userID")):
        mycursor = mydb.connect.cursor()(buffered=True)
        query = "select email, name , phone from users"
        mycursor.execute(query)
        records = mycursor.fetchall()
        #might be a good idea to put address in here
        users = []
        for record in records:  
            user = {
                "email" : record[0],
                "name" : record[1],
                "phone" : record[2]
            }
            users.append(user)

        userJson = json.dumps(users)
        return  userJson

    return "auth error"
'''



def storage():
    hdd = psutil.disk_usage('/')
    pieMaker.createLogoPie()
    return {"diskSpaceRemainingGB" : ( hdd.free // 2**30) }


def sendToUserEmail(toEmail,  subjectText , content):
    yag = yagmail.SMTP(user=adminEmail , password=emailPassword)
    yag.send(to=toEmail, subject="Login for Just Go Shoot ",  contents=content)

@app.route('/account_form', methods=["POST"])
def accountForm():
    if session.get("createAccount"):
        email = request.form['email']
        name = request.form['name']
        phone = request.form['phone']
        addr1 = request.form['addr1']
        addr2 = request.form['addr2']
        addr3 = request.form['addr3']
        county = request.form['addr4']
        eircode = request.form['addr5']
        password = request.form['password']
        password1 = request.form['password1']

        if password != password1 or  len(password) < 9:
            #flash 
            return redirect( url_for("createAccount") )

        #finaly adding user to db
        userID = randString()
        mycursor = mydb.connect.cursor()
        query = """ insert into  users  (email , name,  phone,  eircode,   county ,addr3, addr2,  addr1 , password, admin , userID) values   ( %s, %s ,%s, %s, %s, %s, %s, %s,%s,%s, %s  )"""
        mycursor.execute( query , ( email , name , phone ,eircode , county, addr3, addr2, addr1, genPassword(password) , "0" ,  userID))

        query = """ delete from setupTokens where email = %s """
        mycursor.execute( query , (email, ))
        mydb.commit()
        mycursor.close() 
        
        session.clear()
        session[userID] = userID
        flash(" Created New User: " + email)

        return redirect(url_for("gallery")) 
    return redirect(url_for("index"))



def contactEmail(toEmail,subjectText, content):
    try:
        yag = yagmail.SMTP(user=adminEmail , password=emailPassword)
        yag.send(to=adminEmail, subject=name + " , " + serviceDropDown, contents=contactText + "\n" + "\n Phone: " +  phone)
    except:
        print("error in sending contentEmail yell at Conor")


def addEnteryToFinProjects( folder_name, email):
    mycursor = mydb.connect.cursor()
    pubDate = time.time()

    query = """select users.userID  from users where email  =  %s  """
    mycursor.execute( query , (email,) ) 
    userID = mycursor.fetchone()
    userID = userID[0]

    query = """insert into finshedProjects ( userID,  pubDate , published,  folder_name)  values  (%s, %s, %s, %s )"""
    vals = (   userID , pubDate ,"0",  folder_name)
    mycursor.execute( query , vals ) 
    mydb.commit()
    mycursor.close()

    

def genPassword(password):
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt(12))

def checkPassword(providedPassword, hashedPassword):
    providedPassword = providedPassword.encode('utf-8')
    hashedPassword = hashedPassword.encode('utf-8')
    return bcrypt.checkpw(providedPassword, hashedPassword )



if __name__ == 'main':
        app.run(debug=True)