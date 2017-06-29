from config import *
from datetime import datetime
import psycopg2

conn = psycopg2.connect("dbname=%s host=%s user=%s password=%s"%(database,host,user,password))
cur = conn.cursor()

sql = """
insert into duenos (nombre, telefono, email) values ('dueno_test', '0', 'mail_test@test.cl')
returning
id, nombre, telefono, email;
"""

cur.execute(sql)
conn.commit()
dueno = cur.fetchone()
print ("Insertamos en Duenos :" )
print(dueno)

sql="""
insert into negocios (dueno_id, calle, nombre, comuna, ciudad, region, telefono) values
('0','calle_test','nombre_test','comuna_test','ciudad_test','region_test','1')
returning
id, dueno_id, calle, comuna, ciudad, region, telefono;
"""

cur.execute(sql)
conn.commit()
negocio = cur.fetchone()
print ("Insertamos en  Negocio :" )
print(negocio)

sql="""
insert into negocios (dueno_id, calle, nombre, comuna, ciudad, region, telefono) values
('1','calle_test','nombre_test','comuna_test','ciudad_test','region_test','1')
returning
id, dueno_id, calle, comuna, ciudad, region, telefono;
"""

cur.execute(sql)
conn.commit()
negocio = cur.fetchone()
print ("Insertamos en  Negocio :" )
print(negocio)

sql="""
insert into stocks (negocio_id, producto_id, stock_producto, proveedor_id, precio) values
('1','0', '10','0','1000')
returning negocio_id,producto_id, stock_producto, proveedor_id, precio;
"""

cur.execute(sql)
conn.commit()
stocks = cur.fetchone()
print ("Insertamos en  Stocks :" )
print(stocks)

sql="""
insert into stocks (negocio_id, producto_id, stock_producto, proveedor_id, precio) values
('1','7806500403722', '100','0','2000')
returning negocio_id,producto_id, stock_producto, proveedor_id, precio;
"""

cur.execute(sql)
conn.commit()
stocks = cur.fetchone()
print ("Insertamos en  Stocks :" )
print(stocks)

sql="""
insert into stocks (negocio_id, producto_id, stock_producto, proveedor_id, precio) values
('1','7801610323236', '200','0','1890')
returning negocio_id,producto_id, stock_producto, proveedor_id, precio;
"""

cur.execute(sql)
conn.commit()
stocks = cur.fetchone()
print ("Insertamos en  Stocks :" )
print(stocks)

sql="""
insert into stocks (negocio_id, producto_id, stock_producto, proveedor_id, precio) values
('1','7804646000058', '200','0','1790')
returning negocio_id,producto_id, stock_producto, proveedor_id, precio;
"""

cur.execute(sql)
conn.commit()
stocks = cur.fetchone()
print ("Insertamos en  Stocks :" )
print(stocks)

sql="""
insert into stocks (negocio_id, producto_id, stock_producto, proveedor_id, precio) values
('1','7802420127113', '200','0','10000')
returning negocio_id,producto_id, stock_producto, proveedor_id, precio;
"""

cur.execute(sql)
conn.commit()
stocks = cur.fetchone()
print ("Insertamos en  Stocks :" )
print(stocks)

sql="""
insert into stocks (negocio_id, producto_id, stock_producto, proveedor_id, precio) values
('1','7802000002564', '200','0','1990')
returning negocio_id,producto_id, stock_producto, proveedor_id, precio;
"""

cur.execute(sql)
conn.commit()
stocks = cur.fetchone()
print ("Insertamos en  Stocks :" )
print(stocks)

sql="""
insert into stocks (negocio_id, producto_id, stock_producto, proveedor_id, precio) values
('1','7802110002263', '200','0','1790')
returning negocio_id,producto_id, stock_producto, proveedor_id, precio;
"""

cur.execute(sql)
conn.commit()
stocks = cur.fetchone()
print ("Insertamos en  Stocks :" )
print(stocks)

sql="""
insert into stocks (negocio_id, producto_id, stock_producto, proveedor_id, precio) values
('1','7806540000950', '200','0','2000')
returning negocio_id,producto_id, stock_producto, proveedor_id, precio;
"""

cur.execute(sql)
conn.commit()
stocks = cur.fetchone()
print ("Insertamos en  Stocks :" )
print(stocks)

sql="""
insert into stocks (negocio_id, producto_id, stock_producto, proveedor_id, precio) values
('1','7801930010854', '200','0','2290')
returning negocio_id,producto_id, stock_producto, proveedor_id, precio;
"""

cur.execute(sql)
conn.commit()
stocks = cur.fetchone()
print ("Insertamos en  Stocks :" )
print(stocks)

sql="""
insert into stocks (negocio_id, producto_id, stock_producto, proveedor_id, precio) values
('1','7801620005283', '200','0','1000')
returning negocio_id,producto_id, stock_producto, proveedor_id, precio;
"""

cur.execute(sql)
conn.commit()
stocks = cur.fetchone()
print ("Insertamos en  Stocks :" )
print(stocks)


sql="""
insert into proveedores (telefono, comuna, ciudad, region, calle, precio, nombre)
values ('2', 'comuna_test', 'ciudad_test','region_test','calle_test','800','nombre_test')
returning
id,telefono, comuna, ciudad, region, calle, precio, nombre;
"""


cur.execute(sql)
conn.commit()
proveedor = cur.fetchone()
print ("Insertamos en  Proveedor : ")
print (proveedor)

sql= """
insert into productos (id,nombre, detalle) values ('0','nombre_test','detalle_test')
returning
id,nombre, detalle;
"""

cur. execute(sql)
conn.commit()
productos = cur.fetchone()

sql= """
insert into productos (id,nombre, detalle) values ('7806500403722' ,'Toalla Nova','Elite Deco')
returning
id,nombre, detalle;
"""

cur. execute(sql)
conn.commit()
productos = cur.fetchone()

sql= """
insert into productos (id,nombre, detalle) values ('7801610323236' ,'Coca-Cola','Bebida Gaseosa 3LT')
returning
id,nombre, detalle;
"""

cur. execute(sql)
conn.commit()
productos = cur.fetchone()

sql= """
insert into productos (id,nombre, detalle) values ( '7804646000058','MR Big','Bebida energetica.')
returning
id,nombre, detalle;
"""

cur. execute(sql)
conn.commit()
productos = cur.fetchone()

sql= """
insert into productos (id,nombre, detalle) values ( '7802420127113','Mani salado con miel','Marco Polo')
returning
id,nombre, detalle;
"""

cur. execute(sql)
conn.commit()
productos = cur.fetchone()

sql= """
insert into productos (id,nombre, detalle) values ('7802000002564' ,'Papas Fritas','Lay`s')
returning
id,nombre, detalle;
"""

cur. execute(sql)
conn.commit()
productos = cur.fetchone()

sql= """
insert into productos (id,nombre, detalle) values ('7802110002263' ,'Pisco Capel','40 destilados')
returning
id,nombre, detalle;
"""

cur. execute(sql)
conn.commit()
productos = cur.fetchone()

sql= """
insert into productos (id,nombre, detalle) values ('7806540000950' ,'Servilletas','Favorita pack 40')
returning
id,nombre, detalle;
"""

cur. execute(sql)
conn.commit()
productos = cur.fetchone()

sql= """
insert into productos (id,nombre, detalle) values ('7801930010854' ,'Pizza PF','Jamon Queso')
returning
id,nombre, detalle;
"""

cur. execute(sql)
conn.commit()
productos = cur.fetchone()

sql= """
insert into productos (id,nombre, detalle) values ('7801620005283' ,'Jugo Frugo','3LT sabor pina')
returning
id,nombre, detalle;
"""

cur. execute(sql)
conn.commit()
productos = cur.fetchone()
print (" Insertamos en Productos : ")
print (productos)

fecha=datetime.now()
sql ="""
insert into ventas (negocio_id, fecha) values ('1', ('%s'))
returning
num_venta, negocio_id, fecha;
"""%(fecha)

cur.execute(sql)
conn.commit()
ventas = cur.fetchone()
print ("Insertamos en  Ventas : ")
print (ventas)

fecha=datetime.now()
sql ="""
insert into ventas (negocio_id, fecha) values ('1', ('%s'))
returning
num_venta, negocio_id, fecha;
"""%(fecha)

cur.execute(sql)
conn.commit()
ventas = cur.fetchone()
print ("Insertamos en  Ventas : ")
print (ventas)

fecha=datetime.now()
sql ="""
insert into ventas (negocio_id, fecha) values ('1', ('%s'))
returning
num_venta, negocio_id, fecha;
"""%(fecha)

cur.execute(sql)
conn.commit()
ventas = cur.fetchone()
print ("Insertamos en  Ventas : ")
print (ventas)

sql="""
insert into ventas_detalle (num_venta, producto_id, monto, cantidad)
values ('1','7801620005283', '1000', '3')
returning
num_venta, producto_id, monto, cantidad;
"""
cur.execute(sql)
conn.commit()
ventas_detalle = cur.fetchone()
print ("Insertamos en  Ventas_Detalle : ")
print (ventas_detalle)

sql="""
insert into ventas_detalle (num_venta, producto_id, monto, cantidad)
values ('1','7801610323236', '1890', '1')
returning
num_venta, producto_id, monto, cantidad;
"""
cur.execute(sql)
conn.commit()
ventas_detalle = cur.fetchone()
print ("Insertamos en  Ventas_Detalle : ")
print (ventas_detalle)

sql="""
insert into ventas_detalle (num_venta, producto_id, monto, cantidad)
values ('1','7802110002263', '7990', '2')
returning
num_venta, producto_id, monto, cantidad;
"""
cur.execute(sql)
conn.commit()
ventas_detalle = cur.fetchone()
print ("Insertamos en  Ventas_Detalle : ")
print (ventas_detalle)

sql="""
insert into ventas_detalle (num_venta, producto_id, monto, cantidad)
values ('1','7802000002564', '1870', '1')
returning
num_venta, producto_id, monto, cantidad;
"""
cur.execute(sql)
conn.commit()
ventas_detalle = cur.fetchone()
print ("Insertamos en  Ventas_Detalle : ")
print (ventas_detalle)



sql="""
insert into ventas_detalle (num_venta, producto_id, monto, cantidad)
values ('2','7802420127113', '10000', '1')
returning
num_venta, producto_id, monto, cantidad;
"""
cur.execute(sql)
conn.commit()
ventas_detalle = cur.fetchone()
print ("Insertamos en  Ventas_Detalle : ")
print (ventas_detalle)

sql="""
insert into ventas_detalle (num_venta, producto_id, monto, cantidad)
values ('2','7804646000058', '3400', '1')
returning
num_venta, producto_id, monto, cantidad;
"""
cur.execute(sql)
conn.commit()
ventas_detalle = cur.fetchone()
print ("Insertamos en  Ventas_Detalle : ")
print (ventas_detalle)

sql="""
insert into ventas_detalle (num_venta, producto_id, monto, cantidad)
values ('2','7806500403722', '2000', '2')
returning
num_venta, producto_id, monto, cantidad;
"""
cur.execute(sql)
conn.commit()
ventas_detalle = cur.fetchone()
print ("Insertamos en  Ventas_Detalle : ")
print (ventas_detalle)

sql="""
insert into ventas_detalle (num_venta, producto_id, monto, cantidad)
values ('3','7802000002564', '1890', '2')
returning
num_venta, producto_id, monto, cantidad;
"""
cur.execute(sql)
conn.commit()
ventas_detalle = cur.fetchone()
print ("Insertamos en  Ventas_Detalle : ")
print (ventas_detalle)

sql="""
insert into ventas_detalle (num_venta, producto_id, monto, cantidad)
values ('3','7804646000058', '3400', '1')
returning
num_venta, producto_id, monto, cantidad;
"""
cur.execute(sql)
conn.commit()
ventas_detalle = cur.fetchone()
print ("Insertamos en  Ventas_Detalle : ")
print (ventas_detalle)

conn.close()
