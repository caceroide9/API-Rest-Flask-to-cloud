import os
import pymysql
from flask import jsonify

#db_user = os.environ.get('CLOUD_SQL_USERNAME')
#db_password = os.environ.get('CLOUD_SQL_PASSWORD')
#db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
#db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    #conn = pymysql.connect(user='',password='',unix_socket='t',db='',cursorclass=pymysql.cursors.DictCursor)
    conn=  pymysql.connect(host='',user='',password='',database='',port=3306)
    return conn

