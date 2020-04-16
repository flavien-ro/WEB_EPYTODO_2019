from app import app
import pymysql as sql
from app import controller
from app import models
from app.models import *
from app.controller import *
from config import *
from flask import Flask, render_template, url_for, flash, redirect, request, session, json, jsonify
from datetime import datetime
import traceback

app.config['SECRET_KEY'] = 'd707323ffd8c5c2299fc6bf3776a25a9'

@app.route('/', methods =['GET'])
def route_home():
    if "username" in session:
        return render_template ('user_home.html')
    return render_template ('home.html')

@app.route('/register', methods=['POST', 'GET'])
def route_register():
    return controller.register_control()

@app.route('/signin', methods=['POST', 'GET'])
def route_signin():
    return controller.signin_control()

@app.route('/signout', methods=['POST', 'GET'])
def logout():
    return controller.control_signout()

@app.route('/user/task/add', methods=['POST'])
def route_add_task():
    return controller.control_add_task()

@app.route('/user/task/id', methods=['GET', 'POST'])
def update():
   return controller.control_update()

@app.route('/user/task/delete/<string:task_id>', methods=['GET', 'POST'])
def delete(task_id):
    return controller.control_delete(task_id)

@app.route('/user', methods=['GET'])
def user():
    return controller.control_user_home()

@app.route("/user/task", methods=["GET", "POST"])
def user_task_info():
    return controller.control_user_space()