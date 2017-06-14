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
insert into negocios (dueno_id, calle, comuna, ciudad, region, telefono) values
('0','calle_test','comuna_test','ciudad_test','region_test','1')
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
('0','0', '10','0','1000')
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
insert into productos (nombre, detalle) values ('nombre_test','detalle_test')
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
insert into ventas (num_venta, negocio_id, fecha) values ('0','0', ('%s'))
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
values ('0','0', '1000', '3')
returning
num_venta, producto_id, monto, cantidad;
"""
cur.execute(sql)
conn.commit()
ventas_detalle = cur.fetchone()
print ("Insertamos en  Ventas_Detalle : ")
print (ventas_detalle)



conn.close()
