import ogr
import math as m
import dxfgrabber
import psycopg2
from ClassPoint import Point
from connectionData import *
from geomet import wkt
import json
pi = m.pi

def fCalculateAzimuth(xf,yf, xl, yl):
    dX = xl - xf
    dY = yl - yf
    Azimuth = 0  # Default case, dX = 0 and dY >= 0
    if dX > 0:
        Azimuth = 90 - m.atan(dY / dX) * 180 / pi
    elif dX < 0:
        Azimuth = 270 - m.atan(dY / dX) * 180 / pi
    elif dY < 0:
        Azimuth = 180

    return Azimuth

#dxf = dxfgrabber('KN848832_3_2_I.dxf') # katastralna mapa
dxf = dxfgrabber.readfile("vzory.dxf") # vykres
#entities = dxf.modelspace()
layers = dxf.layers         # zoznam pouzitych vrstiev vo vykrese
entities = dxf.entities     # zoznam prvkov vo vykrese
#print("DXF version: {}".format(dxf.dxfversion))  # dxf version
header_var_count = len(dxf.header)  # dict of dxf header vars
layer_count = len(dxf.layers)  # collection of layer definitions
block_definition_count = len(dxf.blocks)  # dict like collection of block definitions
entity_count = len(dxf.entities)  # list like collection of entities

connection = psycopg2.connect(DB)  # pripoenie k db
connection.autocommit = True
cursor = connection.cursor()
'''
for layer in layers:
    layerName = (layer.name).replace("-", "_")
    if layerName == '0':
        continue
    print layerName
'''
cursor.execute('DROP TABLE IF EXISTS test')
cursor.execute('CREATE TABLE test (ID INT NOT NULL, typ CHAR(50),geom GEOMETRY, PRIMARY KEY (ID))')

id = 1
# pocitadla entit
line_count, polyline_count, pw_polyline_count, arc_count, ellipse_count, circle_count, point_count, dsolid, dface_count, k = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
geometry = []
for entity in entities:  # vyber entit podla typu
    k=k+1
    '''
    if entity.dxftype == "POINT":
        point_count = point_count + 1
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(entity.point[0], entity.point[1])
        wkt = point.ExportToWkt()
        cursor.execute("INSERT INTO test (ID, typ, geom)" + "VALUES (%s, %s, ST_GeometryFromText(%s, %s))",
                       (id, entity.dxftype, wkt, epsg))
        id = id+1
        '''
    if entity.dxftype == "LINE":
        line_count = line_count+1
        line = ogr.Geometry(ogr.wkbLineString)
        start = entity.start
        end = entity.end
        #print start, end
        line.AddPoint(start[0], start[1], start[2])
        line.AddPoint(end[0], end[1], end[2])
        wkt = line.ExportToWkt()
        cursor.execute("INSERT INTO test (ID, typ, geom) " + "VALUES(%s, %s, ST_GeometryFromText(%s, %s))",
                       (id, entity.dxftype, wkt, epsg))
        id = id + 1
        geometry.append(wkt)

    elif entity.dxftype == "POLYLINE":
        polyline_count = polyline_count+1
        vertices = entity.points
        vertices_count = len(vertices)
        line = ogr.Geometry(ogr.wkbLineString)
        for i in range(vertices_count):
            line.AddPoint(vertices[i][0],vertices[i][1],vertices[i][2])
            wkt = line.ExportToWkt()
        cursor.execute("INSERT INTO test (ID, typ, geom) " + "VALUES(%s, %s, ST_GeometryFromText(%s, %s))",
                       (id, entity.dxftype, wkt, epsg))
        id = id + 1
        geometry.append(wkt)

    elif entity.dxftype == "LWPOLYLINE":
        pw_polyline_count = pw_polyline_count+1
        vertices = entity.points
        vertices_count = len(vertices)
        line = ogr.Geometry(ogr.wkbLineString)
        for i in range(vertices_count):
            line.AddPoint(vertices[i][0],vertices[i][1])
            wkt = line.ExportToWkt()
        cursor.execute("INSERT INTO test (ID, typ, geom) " + "VALUES(%s, %s, ST_GeometryFromText(%s, %s))",
                       (id, entity.dxftype, wkt, epsg))
        id = id + 1
        geometry.append(wkt)

    elif entity.dxftype == "ARC":
        arc_count = arc_count+1
        centerPoint = Point(entity.center[0], entity.center[1], entity.center[2])
        #print"arc", centerPoint.getX(), centerPoint.getY(), centerPoint.getZ()
        radius = entity.radius
        start_angle = entity.start_angle             #entity.start_angle
        end_angle = entity.end_angle                 #entity.end_angle
        #endPoint = Point(centerPoint.getX()+(radius * m.cos(end_angle)), centerPoint.getY() + (radius * m.sin(end_angle)), entity.center[2])
        line = ogr.Geometry(ogr.wkbLineString)
        range_angle = end_angle-start_angle
        if range_angle < 0:
            range_angle = range_angle+(360)
        while start_angle < (entity.start_angle+range_angle):
            p = Point(centerPoint.getX()+(radius * m.cos(m.radians(start_angle))), centerPoint.getY()+(radius * m.sin(m.radians(start_angle))), entity.center[2])
            line.AddPoint(p.getX(), p.getY())
            start_angle = start_angle + m.radians(1)
        wkt = line.ExportToWkt()
        #print wkt
        cursor.execute("INSERT INTO test (ID, typ, geom)" + "VALUES(%s, %s, ST_GeometryFromText(%s, %s))",
                       (id, entity.dxftype, wkt, epsg))
        id = id + 1
        geometry.append(wkt)

    elif entity.dxftype == "ELLIPSE":
        ellipse_count = ellipse_count+1
        centerPoint = Point(entity.center[0], entity.center[1], entity.center[2])
        majorAxisPoint = Point(entity.major_axis[0], entity.major_axis[1], entity.major_axis[2])
        start_param = entity.start_param
        end_param = entity.end_param
        line = ogr.Geometry(ogr.wkbLineString)
        #print "start_par: ", start_param, "end_param: ", end_param
        #print "ellipse center point x = {0}, y = {1}, z = {2}".format(centerPoint.getX(), centerPoint.getY(), centerPoint.getZ())
        #print "major axis: ", majorAxisPoint.getX(), majorAxisPoint.getY()
        endPointMajorAxis = Point(centerPoint.getX() + majorAxisPoint.getX(), centerPoint.getY() + majorAxisPoint.getY())
        #print "end Point Major axis:",endPointMajorAxis.getX(), endPointMajorAxis.getY()
        #print "ratio:", entity.ratio
        ratio = entity.ratio
        a = m.sqrt(majorAxisPoint.getX()*majorAxisPoint.getX() + majorAxisPoint.getY()*majorAxisPoint.getY())
        b = a*ratio
        azimut = fCalculateAzimuth(centerPoint.getX(), centerPoint.getY(), endPointMajorAxis.getX(), endPointMajorAxis.getY())

        if round(end_param,5) == round(2*pi,5) and round(start_param,5) <> round(0.0,5):   # ak by nebolo -pi elipsa je o pi otocena dovod - zatial neznami
            end_param = start_param - pi
            start_param = 0

        while start_param <= end_param:
            xi = a * m.cos(start_param)
            yi = b * m.sin(start_param)
            xe = m.sin(m.radians(azimut))*xi - m.cos(m.radians(azimut))*yi
            ye = m.sin(m.radians(azimut))*yi + m.cos(m.radians(azimut))*xi
            start_param = start_param+m.radians(1)
            p = Point(centerPoint.getX() + xe, centerPoint.getY() + ye)
            line.AddPoint(p.getX(), p.getY())
            #print p.getX(), p.getY()
        wkt = line.ExportToWkt()
        cursor.execute("INSERT INTO test (ID, typ, geom)" + "VALUES(%s, %s, ST_GeometryFromText(%s, %s))",
                       (id, entity.dxftype, wkt, epsg))
        id = id + 1
        geometry.append(wkt)

    elif entity.dxftype == "CIRCLE":
        circle_count = circle_count+1
        radius = entity.radius
        centerPoint = Point(entity.center[0], entity.center[1], entity.center[2])
        line = ogr.Geometry(ogr.wkbLineString)
        i = 0
        while i <= 2*pi:
            p = Point(centerPoint.getX()+(radius * m.cos(i)), centerPoint.getY()+(radius * m.sin(i)), entity.center[2])
            line.AddPoint(p.getX(), p.getY())
            i = i + m.radians(1)
        wkt = line.ExportToWkt()
        cursor.execute("INSERT INTO test (ID, typ, geom)" + "VALUES(%s, %s, ST_GeometryFromText(%s, %s))",
                       (id, entity.dxftype, wkt, epsg))
        id = id + 1
        geometry.append(wkt)

cursor.execute("DROP INDEX IF EXISTS test_index")
cursor.execute("CREATE INDEX test_index ON test USING GIST(geom)")

        #else:
        #    print k, entity.dxftype

print "count line %i" % line_count
print "count polyline %i" % polyline_count
print "count pwpolyline %i" % pw_polyline_count
print "count arc %i" % arc_count
print "count ellipse %i" % ellipse_count
#print "count 3Dsolid %i" % dsolid_count
#print "count 3Dface %i" % dface_count
print "count circle %i" % circle_count
print "count point %i" % point_count
print line_count+polyline_count+pw_polyline_count+arc_count+ellipse_count+circle_count
print len(geometry)


