from configuraciones import *
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,passwd))

cur = conn.cursor()
sql ="""select 'drop table "' || tablename || '" cascade;' from pg_tables;""" #
cur.execute(sql)

sql = """
CREATE TABLE Negocios( id serial PRIMARY KEY , Dueno_id integer , Calle varchar , Comuna varchar, Ciudad varchar, Ragion varchar, Telefono integer);
CREATE TABLE Stocks(Negocio_id serial PRIMARY KEY ,  Producto_id integer , Stock_producto integer , Proveedor_id integer , Precio integer );
CREATE TABLE Duenos(id serial PRIMARY KEY , Nombre varchar , Telefono integer , Email varchar );
CREATE TABLE Proveedores(id serial PRIMARY KEY , Telefono integer ,Comuna varchar,Ciudad varchar ,Region varchar ,Calle varchar ,Precio integer,Nombre varchar ,Prod_detalle varchar );
CREATE TABLE Productos(id serial PRIMARY KEY , Nombre varchar , Detalle varchar);
CREATE TABLE Ventas(Num_venta serial PRIMARY KEY , Negocio_id integer, Fecha datetime, Total integer);
CREATE TABLE Ventas_detalle(Num_venta serial PRIMARY KEY , Producto_id integer , Monto integer , Cantidad integer);
"""
#queda con 255 el varchar
cur.execute(sql)
conn.commit()
cur.close()
conn.close()
