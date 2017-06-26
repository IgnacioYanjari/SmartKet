from app import app
from flask import render_template,request
from config import *
import psycopg2

conn = psycopg2.connect("dbname=%s host=%s user=%s password=%s"%(database,host,user,password))
cur = conn.cursor()

@app.route('/')
@app.route('/index', methods=['POST'])
def index():
    if request.method == 'POST': # falta enviar la cantidad del producto
        print request.form
        prod_id = request.form['pid']
        cant = request.form['cant']

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
        select nombre, cantidad, monto*cantidad as total from ventas_detalle, productos
        where ventas_detalle.producto_id=productos.id and num_venta=0;
    """
    print sql
    cur.execute(sql)
    venta_actual=cur.fetchall()

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
    return render_template("index.html",duenos=duenos , datos = datos , ventas = ventas, venta_actual = venta_actual)
