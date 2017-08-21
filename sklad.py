import psycopg2
from connectionData import *
import DXFtoPostgis
import ogr

connection = psycopg2.connect(DB)
connection.autocommit = True
cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS polyg')
cursor.execute('CREATE TABLE polyg (ID INT NOT NULL, typ CHAR(50),geom GEOMETRY, PRIMARY KEY (ID))')


buff = []
dxf_line = DXFtoPostgis.dxfToPostgis(dxfFile)
for line in dxf_line:                           # vytvorenie buffru okolo lini
    pt = ogr.CreateGeometryFromWkt(line)
    bufferDistance = 0.01
    polyBuff = pt.Buffer(bufferDistance).ExportToWkt()
    buff.append(polyBuff)

b = 1
a = 1
id = 1
print len(buff)
multi = []
geometry = []
poly1 = ogr.CreateGeometryFromWkt(buff[0])
#multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)
while b < len(buff):
    poly2 = ogr.CreateGeometryFromWkt(buff[b])
    multipolygon = poly1.Union(poly2)
    try:
        mWkt = multipolygon.ExportToWkt()
        geometry = [multipolygon.ExportToWkt()]
    except AttributeError as e:
        poly1 = ogr.CreateGeometryFromWkt(buff[b])
        continue
    poly1 = ogr.CreateGeometryFromWkt(mWkt)
    print b
    b = b + 1
geometry.append(multipolygon.ExportToWkt())
print geometry
"""
    if b == 300*a:
        multi.append(multipolygon)
        multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)
        a =a+1
        b = b+1
        print a
        continue
    b =b+1
multipolygon2 = ogr.Geometry(ogr.wkbMultiPolygon)
i = 0
for m in multi:
    multipolygon2 = multipolygon2.Union(m)
    print i
    i = i+1
    """

i = 0
ListWkt = []
for geo in geometry:
    sp = geo.split("),")
    while i <len(sp):
        if i == 0:
            wkt = sp[i].replace("MULTI", "").replace("(((", "((").replace(")", "")+"))"
            ListWkt.append(wkt)
        else:
            re = sp[i].replace("((", "").replace("(", "").replace(")", "")
            wkt = "POLYGON ((" + re + "))"
            ListWkt.append(wkt)
#print wkt
        i = i+1

print ListWkt
w = 0
print len(ListWkt)
multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)
while w < len(ListWkt):
    poly1 = ogr.CreateGeometryFromWkt(ListWkt[w])
    union = multipolygon.Union(poly1)
    uWkt = union.ExportToWkt()
    w = w+1
    obj = "polygon"
    wkt = union.ExportToWkt()
    cursor.execute("INSERT INTO polyg (ID, typ, geom)" + "VALUES (%s, %s, ST_GeometryFromText(%s, %s))",
                           (id, obj, wkt, epsg))
    id = id+1
cursor.execute("DROP INDEX IF EXISTS polyg_index")
cursor.execute("CREATE INDEX polyg_index ON polyg USING GIST(geom)")
