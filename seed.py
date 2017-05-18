from config import * 
import psycopg2
conn = psycopg2.connect("dbname=%s user=%s password=%s"%(database,user,password))
cur = conn.cursor()

sql = """
insert into duenos (nombre, telefono, email) values ('Dagoberto Navarrete', '911', 'thudaghitobienbellako@realg4life.cl') returning 
id, nombre, telefono, email;
"""
# Revisar returning
cur.execute(sql)
conn.commit()
dueno = cur.fetchone()
print dueno

conn.close()