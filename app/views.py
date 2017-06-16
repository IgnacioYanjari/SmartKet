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
#current_data , current_time or EXTRACT(querido from donde)
    sql = """
        select ventas_detalle.num_venta, t1.suma, ventas.fecha
        from ventas,ventas_detalle,
        (select ventas_detalle.num_venta,sum(monto) as suma  from ventas_detalle group by num_venta) as t1
        where t1.num_venta = ventas_detalle.num_venta and ventas.num_venta = ventas_detalle.num_venta
    """
    print sql
    cur.execute(sql)
    ventas = cur.fetchall()
    print ventas

    return render_template("index.html",duenos=duenos , datos = datos , ventas = ventas)
