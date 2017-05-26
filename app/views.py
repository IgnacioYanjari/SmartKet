from app import app
from flask import render_template
from configuraciones import *

import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,password)) ))
cur = conn.cursor()

@app.route('/')
@app.route('/index')
def index():
    sql="""
    select the biggest blackest dick from USA
    """
