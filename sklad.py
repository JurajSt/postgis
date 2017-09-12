import psycopg2
from connectionData import *
import DXFtoPostgis
import ogr

def dxfToPoly():
    connection = psycopg2.connect(DB)
    connection.autocommit = True
    cursor = connection.cursor()

    cursor.execute('DROP TABLE IF EXISTS polyg')
    cursor.execute('CREATE TABLE polyg (ID INT NOT NULL, typ CHAR(50),geom GEOMETRY, PRIMARY KEY (ID))')

    buff = []
    dxf_line = DXFtoPostgis.dxfToPostgis(dxfFile)
    for line in dxf_line:                           # vytvorenie buffru okolo lini
        pt = ogr.CreateGeometryFromWkt(line)
        bufferDistance = 0.001
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
            print e
            poly1 = ogr.CreateGeometryFromWkt(buff[b])
            continue
        poly1 = ogr.CreateGeometryFromWkt(mWkt)
        print b
        b = b + 1

    geometry.append(multipolygon.ExportToWkt())
    print "pocet geometryi :", len(geometry)
    obj = "objekt"
    ListWkt = []
    for geo in geometry:
        cursor.execute("INSERT INTO polyg (ID, typ, geom)" + "VALUES (%s, %s, ST_GeometryFromText(%s, %s))",
                       (id, obj, geo, epsg))
        id = id + 1
        '''
        sp = geo.split("),")
        i = 0
        while i < len(sp):
            if i == 0:
                wkt = sp[i].replace("MULTI", "").replace("(((", "((").replace(")", "")+"))"
                ListWkt.append(wkt)
            else:
                re = sp[i].replace("((", "").replace("(", "").replace(")", "")
                wkt = "POLYGON ((" + re + "))"
                ListWkt.append(wkt)
            cursor.execute("INSERT INTO polyg (ID, typ, geom)" + "VALUES (%s, %s, ST_GeometryFromText(%s, %s))",
                               (id, obj, wkt, epsg))
            id = id + 1
    #print wkt
            i = i+1
        obj = "objekt"
        w = 1
        print len(ListWkt)
        
        poly1 = ogr.CreateGeometryFromWkt(ListWkt[0])
        while w < len(ListWkt):
            poly2 = ogr.CreateGeometryFromWkt(ListWkt[w])
            union = poly1.Union(poly2)
            uWkt = union.ExportToWkt()
            poly1 = ogr.CreateGeometryFromWkt(uWkt)
            print w
            w = w+1
        wkt = union.ExportToWkt()
        '''

    cursor.execute("DROP INDEX IF EXISTS polyg_index")
    cursor.execute("CREATE INDEX polyg_index ON polyg USING GIST(geom)")
    return 0

ttt = dxfToPoly()