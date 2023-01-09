import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request,render_template,url_for,flash,jsonify
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import logging
import os
from typing import Union
from google.cloud import storage
import pymysql
from datetime import date
from datetime import datetime
import pytz
from config import config
from validaciones import *

app = Flask(__name__)
app.secret_key = "mysecretkey"

def open_connection():
    conn = pymysql.connect(user='',password='',unix_socket='',db='',cursorclass=pymysql.cursors.DictCursor)
    #conn=  pymysql.connect(host='',user='',password='',database='',port=3306)
    return conn


@app.route('/listar_usuarios', methods=['GET'])
def all_users():
    conn = open_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM Persona')
    data = cur.fetchall()
    return jsonify({'Personas': data, 'mensaje': "Persona listadas.", 'exito': True})
  

@app.route('/agregar_usuario', methods=['POST'])
def add_users():
    conn = open_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    _Rut_Usuario=request.json['Rut_Usuario']
    _Nombre=request.json['Nombre']
    _Apellido=request.json['Apellido']
    _Edad=request.json['Edad']
    _Sexo=request.json['Sexo']
    cur.execute("INSERT INTO Persona (Rut_Usuario, Nombre, Apellido,Edad,Sexo) VALUES (%s, %s,%s,%s,%s)", (_Rut_Usuario,_Nombre,_Apellido,_Edad,_Sexo))
    conn.commit()
    return jsonify({'mensaje': "Persona registrada.", 'exito': True})


@app.route('/eliminar_usuario/<id>', methods=['DELETE'])
def delete_user(id):
    conn = open_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('DELETE FROM Persona WHERE Rut_Usuario = %s', (id))
    conn.commit()
    return jsonify({'mensaje': "Persona eliminada.", 'exito': True})
    

@app.route('/actualizar_usuario/<id>', methods=['POST'])
def update_user(id):
    if request.method == 'POST':
        _Nombre=request.json['Nombre']
        _Apellido=request.json['Apellido']
        _Edad=request.json['Edad']
        _Sexo=request.json['Sexo']
        conn = open_connection()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE Persona
            SET Nombre=%s,
                Apellido=%s,
                Edad=%s,
                Sexo=%s
            WHERE Rut_Usuario = %s
        """, (_Nombre, _Apellido,_Edad,_Sexo,id))
        conn.commit()
        return jsonify({'mensaje': "Persona actualizada.", 'exito': True})
        

@app.route('/editar_usuario/<id>', methods = ['POST', 'GET'])
def get_user(id):
    conn = open_connection()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM Persona WHERE Rut_Usuario = %s', (id))
    data = cur.fetchall()
    cur.close()
    return jsonify({'Persona': data, 'mensaje': "Persona listada.", 'exito': True})
    
       
def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug=True)