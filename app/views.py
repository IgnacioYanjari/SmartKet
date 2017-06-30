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
        prod_id = request.form['pid']
        cant = request.form['cant']

        if not prod_id:
             return redirect("/index")

        else:
            sql = """
                SELECT (EXISTS (SELECT 1 FROM productos WHERE id = ('%s')))::bool;
            """%(prod_id)
            cur.execute(sql)
            isOnTable=cur.fetchone()
            if not isOnTable[0]:
                return redirect("/index")

        sql = """
            select stock_producto from stocks where producto_id=('%s');
        """%(prod_id)
        print sql
        cur.execute(sql)
        cant_stock=cur.fetchone()
        cant_stock=int(cant_stock[0])

        if int(cant) > cant_stock:
            print "La cantidad de producto que desea llevar sobrepasa la cantidad en stock"
            return redirect("/index", code=303)

        sql = """
            SELECT (EXISTS (SELECT 1 FROM ventas_detalle WHERE num_venta=0 and producto_id = ('%s')))::bool;
        """%(prod_id)
        cur.execute(sql)
        exist=cur.fetchone()

        nuevo_stock = cant_stock - int(cant)
        sql = """
            update stocks set stock_producto=('%s') where producto_id=('%s');
        """%(nuevo_stock, prod_id)
        cur.execute(sql)
        conn.commit()

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
            print sql

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
    print sql
    cur.execute(sql)
    venta_actual = cur.fetchall()

    sql = """
        select sum(monto*cantidad) as total from ventas_detalle, productos
        where ventas_detalle.producto_id=productos.id and num_venta='0';
    """
    print sql
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
    print sql
    cur.execute(sql)
    ventas = cur.fetchall()

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
        update stocks set stock_producto = (select cantidad + stock_producto from ventas_detalle,
        stocks where num_venta=0 and ventas_detalle.producto_id=('%s')
        and ventas_detalle.producto_id=stocks.producto_id) where producto_id=('%s');
    """%(id,id)
    print sql
    cur.execute(sql)

    sql="""
        delete from ventas_detalle where num_venta=0 and producto_id=('%s');
    """%(id)
    cur.execute(sql)
    conn.commit()
    return  redirect(request.referrer)

@app.route('/vender')
def vender():
    sql="""
        select * from ventas_detalle where num_venta=0;
    """
    print sql
    cur.execute(sql)
    venta = cur.fetchall()

    if not venta:
        print "No se han seleccionado productos para vender, no se ejecuta venta"
        return redirect("/index")

    sql = """
        select max(num_venta) from ventas_detalle;
    """
    print sql
    cur.execute(sql)
    maxNum_venta = cur.fetchone()
    num_ventaActual = maxNum_venta[0]+1
    sql = """
        update ventas_detalle set num_venta = ('%s') where num_venta=0;
    """%(num_ventaActual)
    cur.execute(sql)

    fecha = datetime.now()
    sql = """
        insert into ventas (num_venta,negocio_id,fecha) values(('%s'),1,('%s'));
    """%(num_ventaActual, fecha)
    cur.execute(sql)
    conn.commit()
    return  redirect(request.referrer)

@app.route('/ventas_estadisticas.html')
@app.route('/date', methods = ["POST" , "GET"])
def ventas():
    importantData=[]
    state = "nothing"
    now = datetime.now().date()
    if request.method == 'POST': # falta enviar la cantidad del producto
        sql = """select ventas.num_venta,ventas.fecha from ventas,
        (select negocios.id as id , min(num_venta) as minimo
        from ventas,negocios
        where negocios.id=ventas.negocio_id and negocios.id='1' group by negocios.id) as total
        where total.id=ventas.negocio_id and ventas.num_venta = total.minimo ; """
        cur.execute(sql)
        date_min = cur.fetchone()
        date_min = date_min[1].date()
        date_ini = request.form['date-ini']
        date_fin = request.form['date-fin']
        date_now = datetime.now()
        date_now = date_now.date()
        date_ini = datetime.strptime(date_ini, '%Y-%m-%d')
        date_fin = datetime.strptime(date_fin, '%Y-%m-%d')
        date_ini = date_ini.date()
        date_fin = date_fin.date()
        print "date_ini :",date_ini,"date_fin :",date_fin,"date_now :",date_now,"date_min :",date_min
        if date_ini > date_fin :
            state = "fail2"
        elif date_ini == date_fin :
            if date_ini <= date_now :
                if date_ini >= date_min :
                    state="today"
                else :
                    state = "fail"
            else :
                state = "fail2"
        elif date_ini < date_fin :
            if date_now >= date_fin :
                if date_ini >= date_min :
                    state="interval"
                else :
                    state="fail"
            else :
                state="fail2"
        else :
            state="nothing"

        sql = """
            select sum(x.total) from (select num_venta, sum(monto*cantidad) as total
            from ventas_detalle group by num_venta) as x, ventas, ventas_detalle, negocios
            where negocios.id = '1' and ventas.negocio_id=negocios.id and ventas.num_venta=ventas_detalle.num_venta and DATE(fecha) BETWEEN ('%s') AND ('%s');
        """%(date_ini, date_fin)
        print sql
        cur.execute(sql)
        ganancia = cur.fetchone()

        sql = """
            select nombre from (select producto_id, sum(cantidad) from ventas_detalle, ventas, negocios where negocios.id='1'
            and ventas.negocio_id=negocios.id and
            ventas_detalle.num_venta=ventas.num_venta and DATE(fecha) BETWEEN ('%s') AND ('%s') group by producto_id) as x, productos
            where productos.id = x.producto_id and x.sum=(select max(t.sum) from
            (select producto_id, sum(cantidad) from ventas_detalle, ventas, negocios where negocios.id='1'
            and ventas.negocio_id=negocios.id and ventas_detalle.num_venta=ventas.num_venta
            and DATE(fecha) BETWEEN ('%s') AND ('%s') group by producto_id) as t);
        """%(date_ini, date_fin,date_ini, date_fin)
        print sql
        cur.execute(sql)
        masvendido = cur.fetchone()

        importantData.append(ganancia[0])
        importantData.append(masvendido[0])


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

    return render_template("ventas_estadisticas.html" , ventas = tupla,
        ventas_detalle = ventas_detalle, state = state, now = now, importantData = importantData)

@app.route('/inventario.html', methods = ["POST" , "GET"])
def inventario():
    sql = """
    select stocks.stock_producto , productos.nombre from productos, stocks where stocks.negocio_id = 1
    and productos.id = stocks.producto_id;
    """
    cur.execute(sql)
    todo = cur.fetchall()

    sql = """
    select max(stocks.stock_producto) from productos, stocks where stocks.negocio_id =1
    and productos.id = stocks.producto_id;
    """
    cur.execute(sql)
    maxi = cur.fetchone()
    todo1 = []
    for i in todo:
        todo1.append([i[0],i[1],(float(i[0])/float(maxi[0]))*100])

    if request.method == 'POST':
        prod = request.form['producto']
        sql = """
        select stocks.stock_producto from stocks, productos where stocks.negocio_id = 1
        and stocks.producto_id = productos.id and productos.nombre = ('%s')
        """%(prod)
        cur.execute(sql)
        stock = cur.fetchone()

        return render_template("inventario.html", stock = stock, todo = todo1)

    return render_template("inventario.html", stock = '0', todo = todo1)

@app.route('/anadir_stock', methods = ["POST" , "GET"])
def anadir_stock():
    if request.method == 'POST':
        nombre1 = request.form['nombre1']
        cantidad1 = request.form['cantidad1']
        sql = """
        select stocks.stock_producto , stocks.producto_id from stocks ,
        productos where stocks.negocio_id = '1' and stocks.producto_id = productos.id and productos.nombre = ('%s');
        """%(nombre1)
        cur.execute(sql)
        print sql
        stock1 = cur.fetchone()
        print stock1
        n_stock = stock1[0]+int(cantidad1)
        sql = """
        update stocks set stock_producto = ('%s') where stocks.negocio_id = '1' and stocks.producto_id =('%s');
        """%(n_stock, stock1[1])
        print sql
        cur.execute(sql)
        return  redirect(request.referrer)
@app.route('/anadir_prod', methods = ["POST" , "GET"])
def anadir_prod():
    if request.method == 'POST':
        nombre = request.form['nombre0']
        detalle = request.form['detalle']
        id1 = request.form['id1']
        cant = request.form['cant']
        precio = request.form['precio']
        sql = """
        insert into productos values (('%s'),('%s'),('%s'));
        """%(id1,nombre,detalle)
        cur.execute(sql)
        sql = """
        insert into stocks values('1',(%s),(%s),'0',(%s))
        """%(id1,cant,precio)
        cur.execute(sql)
        return  redirect(request.referrer)

