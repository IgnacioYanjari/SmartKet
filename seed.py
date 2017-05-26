from config import * 
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,password))
cur = conn.cursor()

sql = """
insert into duenos (id,nombre, telefono, email) values ('0','dueno_test', '0', 'mail_test') 
returning 
id, nombre, telefono, email;

insert into Negocios (id, dueno_id, calle, comuna, ciudad, region, telefono) values 
('0','0','calle_test','comuna_test','ciudad_test','region_test','0') returning 
id, dueno_id, calle, comuna, ciudad, region, telefono;

insert into stocks (negocio_id,producto_id, stock_producto, proveedor_id, precio) values 
('0','0', '0','0','0') 
returning 
negocio_id,producto_id, stock_producto, proveedor_id, precio;

insert into proveedor (id,telefono, comuna, ciudad, region, calle, precio, nombre) values ('0','0', 'comuna_test', 'ciudad_test','region_test','calle_test','0','nombre_test') 
returning 
id,telefono, comuna, ciudad, region, calle, precio, nombre;

insert into productos (id,nombre, detalle) values ('0','nombre_test','detalle_test') 
returning 
id,nombre, detalle;

insert into ventas (num_venta, negocio_id, fecha) values ('0','0', '0/0/0') 
returning 
num_venta, negocio_id, fecha;

insert into ventas_detalle (num_venta, producto_id, monto, cantidad) values ('0','0', '0', '0') 
returning 
num_venta, producto_id, monto, cantidad;
"""
# Revisar returning
cur.execute(sql)
conn.commit()
dueno = cur.fetchone()
print dueno

conn.close()
