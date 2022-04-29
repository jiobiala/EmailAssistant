import smtplib
from flask import Flask, render_template, request, flash, redirect, session, url_for, jsonify
import os
from Transciption import *
from pydub import AudioSegment

app = Flask(__name__)
app.secret_key = 'supersecretkey12345'

@app.route('/', methods = ['GET', 'POST'])
def home():
    text = 'click anywhere to start'
    gender = 'Male'
    text_to_speech(text, gender)
    return render_template('Home.html')

@app.route('/login_email', methods = ['GET', 'POST'])
def login_email():
    if request.method == 'POST':
        file = request.files['file']
        raw = "raw.wav"
        audio_file = "audio.mp3"
        file.save(raw)
        AudioSegment.from_file(raw).export(audio_file, format='mp3')
        command = query('audio.mp3')
        os.remove(raw)
        os.remove(audio_file)

        if command == 'next':
            session.pop('user', None)
            email = str(request.form['email'])

            if check(email):
                session['email'] = email
                return jsonify(dict(loc='/login_password'))
            else:
                text = 'invalid email format'
                gender = 'Male'
                text_to_speech(text,gender)
        else:
            e = reformat_email(command)
            text = 'you said ' + e
            gender = 'Male'
            text_to_speech(text, gender)
            return jsonify('', render_template('login_email_update.html', email=e))
    return render_template('login_email.html')
###################################################################################
@app.route('/login_password', methods = ['GET', 'POST'])
def login_password():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    if request.method == 'POST':
        file = request.files['file']
        raw = "raw.wav"
        audio_file = "audio.mp3"
        file.save(raw)
        AudioSegment.from_file(raw).export(audio_file, format='mp3')
        command = query('audio.mp3')
        os.remove(raw)
        os.remove(audio_file)

        if command == 'next':
            session.pop('user', None)
            password = str(request.form['password'])
            session['password'] = password
            try:
                email = session.get('email')
                password = session.get('password')
                if (server.login(email, password)):
                    text = 'Welcome user'
                    gender = 'Male'
                    text_to_speech(text, gender)
                    return jsonify({'loc': '/menu'})
            except:
                text = 'invalid email or password, please try again'
                gender = 'Male'
                text_to_speech(text, gender)
                return jsonify(dict(loc='/login_email'))
        else:
            p = command.replace(' ','')
            return jsonify('', render_template('login_password_update.html', password=p))
    return render_template('login_password.html')


if __name__ == '__main__':
    app.run(debug=True)
