#!/usr/bin/python3
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


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


def createEmail(name,email,phone,serviceDropDown,contactText)
    


if __name__ == 'main':
        app.run(debug=True)