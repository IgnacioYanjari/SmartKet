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

    sql = """
        select ventas_detalle.num_venta, t1.suma, ventas.fecha
        from ventas,ventas_detalle,
        (select ventas_detalle.num_venta,sum(monto) as suma  from ventas_detalle group by num_venta) as t1
        where t1.num_venta = ventas_detalle.num_venta and ventas.num_venta = ventas_detalle.num_venta
    """
    print sql
    cur.execute(sql)
    ventas = cur.fetchall()
    for subventa in ventas

        fecha = str(ventas[2].day)+"/"+str(ventas[2].month)+"/"+str(ventas[2].year)
        hora = str(ventas[2].hour)+":"+str(ventas[2].minute)+":"str(ventas[2].second)
        ventas[2] = fecha
        ventas.append(hora)

    print ventas

    return render_template("index.html",duenos=duenos , datos = datos , ventas = ventas)
