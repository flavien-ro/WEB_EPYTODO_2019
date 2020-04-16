from app import app
from flask import render_template, request, jsonify, session
from config import *
from app.views import *
from flask import Flask, render_template, url_for, flash, redirect, request
import traceback
import pymysql as sql
import pymysql.cursors


def conn_model():
    conn = sql.connect(host=DATABASE_HOST,
                        user=DATABASE_USER,
                        unix_socket=DATABASE_SOCK,
                        passwd=DATABASE_PASS,
                        charset='utf8mb4',
                        db=DATABASE_NAME)
    return conn

def signin_model(cursor, connection, username, password):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
    account = cursor.fetchone()
    return account

def register_model(cursor, connection, username):
    cursor = connection.cursor()
    new_value = cursor.execute('SELECT * FROM user WHERE username = %s', (username))
    account = cursor.fetchone()
    return account, new_value

def create_usr(cursor, username, password):
    cursor.execute('INSERT INTO user VALUES (NULL, %s, %s)', (username, password))
    cursor.connection.commit()
    return cursor

def add_task(cursor, connection, title, begin, end, status, usr):
    cursor = connection.cursor()
    my_sql = "INSERT INTO task (title, begin, end, status, creator) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(my_sql, (title, begin, end, status, usr))
    connection.commit()

def update_model(connection, title, begin, end, status, task_id, cursor):
    cursor = connection.cursor()
    cursor.execute("UPDATE task SET title=%s, begin=%s, end=%s, status=%s WHERE task_id=%s", (title, begin, end, status, task_id))
    connection.commit()

def update_spe_case_begin(connection, title, begin, end, status, task_id, cursor):
    cursor = connection.cursor()
    cursor.execute("UPDATE task SET title=%s, begin=CURRENT_TIMESTAMP, end=%s, status=%s WHERE task_id=%s", (title, end, status, task_id))
    connection.commit()

def update_spe_case_end(connection, title, begin, end, status, task_id, cursor):
    cursor = connection.cursor()
    cursor.execute("UPDATE task SET title=%s, begin=%s, end=%s+INTERVAL 1 DAY, status=%s WHERE task_id=%s", (title, begin, begin, status, task_id))
    connection.commit()

def delete_model(connection, cursor, task_id):
    cursor = connection.cursor()
    cursor.execute("DELETE from task where task_id=%s", (task_id))
    connection.commit()

def user_tasks(connection):
    cursor = connection.cursor()
    cursor.execute("SET @num := 0;")
    cursor.execute("UPDATE task SET task_id = @num := (@num+1)")
    cursor.execute("ALTER TABLE task AUTO_INCREMENT = 1")
    cursor.execute('SELECT * FROM task WHERE creator LIKE %s', [session['username']])
    tasks = cursor.fetchall()
    cursor.close
    return tasks

def add_task_spe_case(cursor, connection, title, begin, end, status, usr):
    cursor = connection.cursor()
    my_sql = "INSERT INTO task (title, begin, end, status, creator) VALUES (%s, CURRENT_TIMESTAMP, NOW()+INTERVAL 1 DAY, %s, %s)"
    cursor.execute(my_sql, (title, status, usr))
    connection.commit()

def add_task_spe_case_begin(cursor, connection, title, begin, end, status, usr):
    cursor = connection.cursor()
    my_sql = "INSERT INTO task (title, begin, end, status, creator) VALUES (%s, CURRENT_TIMESTAMP, %s, %s, %s)"
    cursor.execute(my_sql, (title, end, status, usr))
    connection.commit()

def add_task_spe_case_end(cursor, connection, title, begin, end, status, usr):
    cursor = connection.cursor()
    my_sql = "INSERT INTO task (title, begin, end, status, creator) VALUES (%s, %s, %s+INTERVAL 1 DAY, %s, %s)"
    cursor.execute(my_sql, (title, begin, begin, status, usr))
    connection.commit()