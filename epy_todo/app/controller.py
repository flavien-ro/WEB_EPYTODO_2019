from app import app
from flask import render_template, request, jsonify, session
from app import models
from app.models import *
from config import *
from flask import Flask, render_template, url_for, flash, redirect, request, json, jsonify
import traceback
import pymysql as sql

def signin_control():
    try:
        connection = models.conn_model()
        with connection.cursor() as cursor:
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                account = models.signin_model(cursor, connection, username, password)
                if account:
                    session['username'] = username
                    result = json.dumps("Signin successful")
                    flash(json.loads(result))
                    return redirect(url_for('user'))
                else:
                    result = json.dumps("error : login  or  password  does  not  match")
                    flash(json.loads(result))
                    return redirect(url_for('route_signin'))
    except:
        traceback.print_exc()
    finally:
        connection.close()
    return render_template('login.html')

def register_control():
    try:
        connection = models.conn_model()
        with connection.cursor() as cursor:
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                if (len(username) < 1 or len(password) < 1):
                    result = json.dumps("Please enter a username and a password")
                    flash(json.loads(result))
                    return redirect(url_for('route_register'))
                elif len(username) > 20:
                    result = json.dumps("username must be less than 20 characters")
                    flash(json.loads(result))
                    return redirect(url_for('route_register'))
                elif len(username) < 3:
                    result = json.dumps("username must be more than 3 characters")
                    flash(json.loads(result))
                    return redirect(url_for('route_register'))
                account = models.register_model(cursor, connection, username)
                if account[0]:
                    result = json.dumps("Account already exists!")
                    flash(json.loads(result))
                    return redirect(url_for('route_register'))
                elif account[1] > 0:
                    result = json.dumps("Account already exists!")
                    flash(json.loads(result))
                    return redirect(url_for('route_register'))
                else:
                    cursor = models.create_usr(cursor, username, password)
                    result = json.dumps("Account  created")
                    flash(json.loads(result))
                    return redirect(url_for('route_home'))
    except:
        traceback.print_exc()
    finally:
        connection.close()
    return render_template('register.html')

def control_signout():
    if "username" in session:
        session.pop('username', None)
        result = json.dumps("signout  successful")
        flash(json.loads(result))
        return redirect(url_for('route_home'))
    return redirect(url_for('route_home'))

def control_add_task():
    try:
        connection = models.conn_model()
        with connection.cursor() as cursor:
            if request.method == "POST":
                title = request.form['title']
                status = request.form['status']
                begin = request.form['begin']
                end = request.form['end']
                usr = session['username']            
                if len(title) > 20:
                    result = json.dumps("Your task name must be less than 20 characters")
                    flash(json.loads(result))
                    return redirect(url_for('user_task_info'))
                if (len(begin) < 2 and len(end) < 2):
                    models.add_task_spe_case(cursor, connection, title, begin, end, status, usr)
                    result = json.dumps("New task added")
                    flash(json.loads(result))
                elif(len(begin) < 2):
                    models.add_task_spe_case_begin(cursor, connection, title, begin, end, status, usr)
                    result = json.dumps("New task added")
                    flash(json.loads(result))
                elif (len(end) < 2):
                    models.add_task_spe_case_end(cursor, connection, title, begin, end, status, usr)
                    result = json.dumps("New task added")
                    flash(json.loads(result))
                else:
                    models.add_task(cursor, connection, title, begin, end, status, usr)
                    result = json.dumps("New task added")
                    flash(json.loads(result))
    except:
        traceback.print_exc()
    finally:
        connection.close()
    return redirect(url_for('user_task_info'))

def control_update():
    try:
        connection = models.conn_model()
        with connection.cursor() as cursor:
            if request.method == "POST":
                task_id = request.form['task_id']
                status = request.form.get('status')
                if status == None:
                    status = request.form['save_status']
                title = request.form['title_edit']
                begin = request.form['edit_begin']
                end = request.form['edit_end']
                if len(title) > 20:
                    result = json.dumps("Cannot update : Your task name must be less than 20 characters")
                    flash(json.loads(result))
                    return redirect(url_for('user_task_info'))
                if (len(begin) < 2):
                    models.update_spe_case_begin(connection, title, begin, end, status, task_id, cursor)
                    result = json.dumps("Update  done")
                    flash(json.loads(result))
                if (len(end) < 2):
                    models.update_spe_case_end(connection, title, begin, end, status, task_id, cursor)
                    result = json.dumps("Update  done")
                    flash(json.loads(result))
                else: 
                    models.update_model(connection, title, begin, end, status, task_id, cursor)
                    result = json.dumps("Update  done")
                    flash(json.loads(result))
    except:
        traceback.print_exc()
    finally:
        connection.close()
    return redirect(url_for('user_task_info'))

def control_delete(task_id):
    try:
        connection = models.conn_model()
        with connection.cursor() as cursor:
            models.delete_model(connection, cursor, task_id)
            result = json.dumps("Task  deleted")
            flash(json.loads(result))
    except:
        traceback.print_exc()
    finally:
        connection.close()
    return redirect(url_for('user_task_info'))

def control_user_home():
    if "username" not in session:
        result = json.dumps("error you  must be  logged  in")
        flash(json.loads(result))
        return redirect (url_for('route_home'))
    connection = models.conn_model()
    tasks = models.user_tasks(connection)
    if "username" in session:
        return render_template ('user_home.html', task=tasks)
    return redirect (url_for('route_home'))

def control_user_space():
    if "username" not in session:
        result = json.dumps("error you  must be  logged  in")
        flash(json.loads(result))
        return redirect (url_for('route_home'))
    connection = models.conn_model()
    tasks = models.user_tasks(connection)
    if "username" in session:
        return render_template ('user.html', task=tasks)
    return redirect (url_for('route_home'))