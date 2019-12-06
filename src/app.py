# src/app.py
import logging
from logging.handlers import RotatingFileHandler
import sys
import json
import pyfiglet
from flask import Flask, Blueprint, render_template, request
from flask_cors import CORS

from .config import app_config
from .models import bcrypt
from .models.LoggerModel import LoggerModel


def create_app(env_name):
    """
        Create app
    """
    # app initialization
    app = Flask('BIONS')
    CORS(app)
    app.config.from_object(app_config[env_name])
    bcrypt.init_app(app)

    # initialize the log handler
    logHandler = RotatingFileHandler('info.log', maxBytes=1000, backupCount=1)
    # set the log handler level
    logHandler.setLevel(logging.INFO)
    # set the app logger level
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(logHandler)

    print(pyfiglet.figlet_format("BIONS Device logging"))

    @app.route('/', methods=['GET'])
    def index():
        user = {'username': 'Miguel'}
        posts = [
            {
                'author': {'username': 'John'},
                'body': 'Beautiful day in Portland!'
            },
            {
                'author': {'username': 'Susan'},
                'body': 'The Avengers movie was so cool!'
            }
        ]
        return render_template('index.html', title='Home', user=user, posts=posts)

    @app.route('/saveLogDetails', methods=['POST'])
    def saveLogDetails():
        device_id = request.form['device_id']
        room_no = request.form['room_no']
        ts = request.form['ts']
        if device_id != "" and room_no != "":
            LoggerModel.createLogDetails(device_id, room_no, ts)
        return json.dumps({'status': 'OK', 'device_id': device_id, 'room_no': room_no})

    @app.route('/getBionsLogFile')
    def downloadBionsLogFile():
        print('downloadLogFile')
        log_file = LoggerModel.DownloadLogFileFromLocal()
        return log_file

    return app
