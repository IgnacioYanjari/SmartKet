from app import app
from flask import render_template
from config import *
import psycopg2

conn = psycopg2.connect("dbname=%s host=%s user=%s password=%s"%(database,host,user,password))
cur = conn.cursor()

@app.route('/')
@app.route('/index')
def index():
    sql = """
        select nombre from duenos where id = '1';
    """
    print sql
    cur.execute(sql)
    duenos = cur.fetchone()

    sql = """

        select negocios.telefono , negocios.calle
        from negocios  where  negocios.id='1';
    """
    print sql
    cur.execute(sql)
    datos = cur.fetchone()
    print datos
    return render_template("index.html",duenos=duenos , datos = datos)
