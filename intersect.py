import psycopg2
import xlsxwriter

from connectionData import *
from calculateArea import columnArea

connection = psycopg2.connect(DB)  # pripoenie k db
connection.autocommit = True
cursor = connection.cursor()




def intersect(parcela, objekt):
    cursor.execute('''select p.parcela
                        from ''' + parcela + ''' as p, 
                        ''' + objekt + ''' as o
                        where st_intersects(o.geom,p.geom) 
                        group by p.parcela;''')
    rows = cursor.fetchall()
    return rows, objekt

