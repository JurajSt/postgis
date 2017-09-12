import psycopg2
from connectionData import *
from calculateArea import columnArea

connection = psycopg2.connect(DB)  # pripoenie k db
connection.autocommit = True
cursor = connection.cursor()


def intersection():
    cursor.execute('''DROP TABLE IF EXISTS ''' + tableName + ''';''')
    cursor.execute('''CREATE TABLE ''' + tableName + ''' AS 
        (SELECT p.parcela As parcelne_cislo, b.objekt As objekt, 
        ST_Intersection(b.geom, p.geom) As intersect_geom
        FROM test_polygon b, uo848832c p
        WHERE ST_Overlaps(b.geom, p.geom));''')
    return 0



