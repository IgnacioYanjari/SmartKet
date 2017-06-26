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
    # print sql
    cur.execute(sql)
    duenos = cur.fetchone()

    sql = """

        select negocios.telefono , negocios.calle
        from negocios  where  negocios.id='0';
    """
    # print sql
    cur.execute(sql)
    datos = cur.fetchone()

    sql = """
        select ventas_detalle.num_venta, t1.suma, ventas.fecha from ventas, ventas_detalle,
        (select ventas_detalle.num_venta, sum(monto*cantidad) as suma from ventas_detalle group by num_venta) as t1
        where t1.num_venta = ventas_detalle.num_venta and ventas.num_venta = ventas_detalle.num_venta
        order by ventas_detalle.num_venta desc limit 10;
    """
    # print sql
    cur.execute(sql)
    ventas = cur.fetchall()
    print ventas

    tupla =[]
    for subventa in ventas:
        tupla2 = list(subventa)
        tupla.append(tupla2)

    print (tupla)

    for subventa in tupla:
        fechas = str(subventa[2].day)+"/"+str(subventa[2].month)+"/"+str(subventa[2].year)
        horas = str(subventa[2].hour)+":"+str(subventa[2].minute)+":"+str(subventa[2].second)
        subventa.append(fechas)
        subventa.append(horas)

    ventas = tuple(tupla)
    print ventas
    return render_template("index.html",duenos=duenos , datos = datos , ventas = ventas)
