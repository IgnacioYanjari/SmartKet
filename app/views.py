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
    state = "nothing"
    fechas = 0
    if request.method == 'POST': # falta enviar la cantidad del producto

        date_ini = request.form['date-ini']
        date_fin = request.form['date-fin']
        date_now = datetime.now()
        date_now = date_now.date
        date_ini = datetime.strptime(date_ini, '%Y-%m-%d')
        date_fin = datetime.strptime(date_fin, '%Y-%m-%d')
        date_ini = date_ini
        date_fin = date_fin
        print "date_fin :",date_fin,"date_ini :",date_ini
        #year_ini = int(date_ini[0:4])
        #month_ini = int(date_ini[5:7])
        #day_ini = int(date_ini[8:10])
        #year_fin = int(date_fin[0:4])
        #month_fin = int(date_fin[5:7])
        #day_fin = int(date_fin[8:10])
        #year_now = date_now.date().year
        #month_now = date_now.date().month
        #day_now = date_now.date().day
        #print "year_ini :",year_ini
        #print "month_ini :",month_ini
        #print "day_ini :",day_ini
        #print "year_fin :",year_fin
        #print "month_fin :",month_fin
        #print "day_fin :",day_fin
        #print "year_now :",year_now
        #print "month_now :",month_now
        #print "day_now :",day_now

        #if date_ini.year  >  date_fin.year or date_ini.month > date_fin.month or date_ini.day > date_fin.day :
        #    if date_ini.year  >  date_now.year or date_ini.month > date_now.month or date_ini.day > date_now.day :
        #        #print "fail2"
        #        state = "fail2"
        #    else :
                #print "fail"
        #        state ="fail2"
        #elif date_ini.year  ==  date_fin.year and date_ini.month == date_fin.month and date_ini.day == date_fin.day :
        #    if date_ini.year  <=  date_now.year and date_ini.month <= date_now.month and date_ini.day <= date_now.day:
        #        print "today"
        #        state = "today"
        #    else :
                #print "fail2"
        #        state = "fail2"
        #elif date_ini.year  <  date_fin.year or date_ini.month < date_fin.month or date_ini.day < date_fin.day :
        #    if date_now.year  >=  date_fin.year or date_now.month >= date_fin.month or date_now.day >= date_fin.day:
                #print "interval"
        #        state = "interval"
        #    else :
                #print "fail2"
        #        state ="fail2"
        #else :
        #print "nothing"
        #    state ="nothing"

#        if state == "interval" :
#            print "caca"
        # Hacer consulta y mostrar cosas

#        if state == "today" :
#            print "cacu"
        # Hacer consulta y mostrar cosas del dia

    sql = """ select t2.num_venta , t1.suma , t2.fecha
    from (select ventas_detalle.num_venta ,sum( ventas_detalle.monto * ventas_detalle.cantidad) as suma
    from ventas_detalle,ventas,negocios where negocios.id='1' and negocios.id=ventas.negocio_id and ventas_detalle.num_venta = ventas.num_venta group by ventas_detalle.num_venta) as t1 ,
    (select ventas.num_venta , fecha from ventas,negocios where ventas.negocio_id = negocios.id and negocios.id='1' group by ventas.num_venta)as t2
    where t1.num_venta = t2.num_venta order by t2.num_venta;"""
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

    sql = """select ventas_detalle.num_venta,productos.nombre,ventas_detalle.cantidad,ventas_detalle.monto
    from productos,ventas_detalle,ventas,negocios where productos.id = ventas_detalle.producto_id
    and negocios.id = ventas.negocio_id and ventas.num_venta = ventas_detalle.num_venta and negocios.id='1' ;"""
    cur.execute(sql)
    ventas_detalle = cur.fetchall()

    return render_template("ventas_estadisticas.html" , ventas = tupla, ventas_detalle = ventas_detalle, state = state)

@app.route('/inventario.html')
def inventario():
    return render_template("inventario.html")
