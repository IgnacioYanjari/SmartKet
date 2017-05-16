from configuraciones import *
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))

cur = conn.cursor()
sql ="""select 'drop table "' || tablename || '" cascade;' from pg_tables;""" #
cur.execute(sql)

sql = """
CREATE TABLE Negocios( id serial PRIMARY KEY , Dueno_id integer , Ubicacion varchar , Comuna varchar , Gastos integer);
CREATE TABLE Stocks(id serial PRIMARY KEY , Negocio_id integer , Producto_id integer , Stock_producto integer , Proveedor_id integer , Precio integer );
CREATE TABLE Dueños(id serial PRIMARY KEY , Nombre varchar , Telefono integer , Email varchar );
CREATE TABLE Proveedores(id serial PRIMARY KEY , Stock_id integer , Telefono integer , Comuna varchar,Ubicacion varchar ,Precio integer);
CREATE TABLE Productos(id serial PRIMARY KEY , Nombre varchar , Detalle varchar);
CREATE TABLE Ventas(num_venta serial PRIMARY KEY , Negocio_id integer, Fecha datetime);
CREATE TABLE Ventas_detalle(num_venta integer , Producto_id integer , Monto integer , Cantidad integer);
"""
#queda con 255 el varchar
cur.execute(sql)
conn.commit()
cur.close()
conn.close()
