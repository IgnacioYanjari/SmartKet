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
        from negocios  where  negocios.id='1';
    """
    # print sql
    cur.execute(sql)
    datos = cur.fetchone()

    sql = """
        select t2.num_venta , t1.suma , t2.fecha from (select num_venta ,sum(monto*cantidad) as suma
        from ventas_detalle group by num_venta) as t1 ,
        (select num_venta , fecha from ventas group by num_venta) as t2
        where t1.num_venta = t2.num_venta order by t2.num_venta desc limit 10;

    """
    # print sql
    cur.execute(sql)
    ventas = cur.fetchall()
    #print ventas

    tupla =[]
    for subventa in ventas:
        tupla2 = list(subventa)
        tupla.append(tupla2)

    #print (tupla)

    for subventa in tupla:

        day = str(subventa[2].day)
        if int(day) < 10 :
            day = "0" + day
        month = str(subventa[2].month)
        if int(month) < 10 :
            month = "0" + month
        year = str(subventa[2].year)
        if int(year) < 10 :
            year = "0" + year
        fechas = day +"/"+ month+"/"+ year

        hour = str(subventa[2].hour)
        if int(hour) < 10 :
            hour = "0" + hour
        minute = str(subventa[2].minute)
        if int(minute) < 10 :
            minute = "0" + minute
        second = str(subventa[2].second)
        if int(second) < 10 :
            second = "0" + second

        horas = hour+":"+minute+":"+second

        subventa.append(fechas)
        subventa.append(horas)

    ventas = tuple(tupla)
    #print ventas
    return render_template("index.html",duenos=duenos , datos = datos , ventas = ventas)

@app.route('/ventas_estadisticas.html')
def ventas():

    sql = """ select t2.num_venta , t1.suma , t2.fecha from (select num_venta ,sum(monto*cantidad) as suma
            from ventas_detalle group by num_venta) as t1 ,
            (select num_venta , fecha from ventas group by num_venta) as t2
            where t1.num_venta = t2.num_venta order by t2.num_venta
        """

    cur.execute(sql)
    ventas = cur.fetchall()
    #print sql
    #print ventas
    tupla =[]
    for subventa in ventas:
        tupla2 = list(subventa)
        tupla.append(tupla2)

    #print (tupla)

    for subventa in tupla:

        day = str(subventa[2].day)
        if int(day) < 10 :
            day = "0" + day
        month = str(subventa[2].month)
        if int(month) < 10 :
            month = "0" + month
        year = str(subventa[2].year)
        if int(year) < 10 :
            year = "0" + year
        fechas = day +"/"+ month+"/"+ year

        hour = str(subventa[2].hour)
        if int(hour) < 10 :
            hour = "0" + hour
        minute = str(subventa[2].minute)
        if int(minute) < 10 :
            minute = "0" + minute
        second = str(subventa[2].second)
        if int(second) < 10 :
            second = "0" + second

        horas = hour+":"+minute+":"+second

        subventa.pop(2)
        subventa.append(fechas)
        subventa.append(horas)

    #print tupla

    sql = """ select ventas_detalle.num_venta,productos.nombre,ventas_detalle.cantidad,ventas_detalle.monto
              from productos,ventas_detalle where productos.id = ventas_detalle.producto_id"""
    cur.execute(sql)
    ventas_detalle = cur.fetchall()
    

    return render_template("ventas_estadisticas.html" , ventas = tupla, ventas_detalle = ventas_detalle)
