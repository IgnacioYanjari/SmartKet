from app import app
from datetime import datetime
from flask import render_template,request,redirect
from config import *
import psycopg2

conn = psycopg2.connect("dbname=%s host=%s user=%s password=%s"%(database,host,user,password))
cur = conn.cursor()

@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST': # falta enviar la cantidad del producto
        print request.form
        prod_id = request.form['pid']
        cant = request.form['cant']

        sql = """
            SELECT (EXISTS (SELECT 1 FROM ventas_detalle WHERE num_venta=0 and producto_id = ('%s')))::bool;
        """%(prod_id)
        cur.execute(sql)
        exist=cur.fetchone()
        print "here:",exist
        if exist[0]:
             sql = """
                 update ventas_detalle set cantidad = (select cantidad from ventas_detalle where
                 producto_id=('%s') and num_venta=0)+('%s')
                 where num_venta=0 and producto_id=('%s')
             """%(prod_id, cant, prod_id)
             cur.execute(sql)
             conn.commit()
        else:
            sql = """
                select productos.nombre, stocks.precio from productos, stocks where
                productos.id=stocks.producto_id and stocks.negocio_id=1 and productos.id=('%s');
            """%(prod_id)
            cur.execute(sql)
            p_info=cur.fetchone()
            print p_info

    	    sql = """
                insert into ventas_detalle (num_venta, producto_id, monto, cantidad) values(0,%s,%s,%s);
            """%(prod_id,p_info[1],cant)
            cur.execute(sql)
            conn.commit()

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
        select nombre, cantidad, monto*cantidad as total, producto_id from ventas_detalle, productos
        where ventas_detalle.producto_id=productos.id and num_venta='0';
    """
    cur.execute(sql)
    venta_actual = cur.fetchall()

    sql = """
        select sum(monto*cantidad) as total from ventas_detalle, productos
        where ventas_detalle.producto_id=productos.id and num_venta='0';
    """
    cur.execute(sql)
    total_venta = cur.fetchone()
    if not total_venta[0]:
        total_venta = [0]

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
    return render_template("index.html",duenos=duenos , datos = datos ,
    ventas = ventas, venta_actual = venta_actual, total_venta = total_venta)

@app.route('/delete/<id>')
def delete(id):
    sql="""
        delete from ventas_detalle where num_venta=0 and producto_id=('%s');
    """%(id)
    cur.execute(sql)
    conn.commit()
    return  redirect(request.referrer)

@app.route('/ventas_estadisticas.html')
@app.route('/date', methods = ["POST" , "GET"])
def ventas():
    if request.method == 'POST': # falta enviar la cantidad del producto
        date_ini = request.form['date-ini']
        date_fin = request.form['date-fin']
        date_now = datetime.now()
        print date_ini
        print date_fin
        print date_now.date()
    sql = """ select t2.num_venta , t1.suma , t2.fecha from (select num_venta ,sum( monto * cantidad) as suma
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
