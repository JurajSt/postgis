import ogr
import math as m
import dxfgrabber
import psycopg2
from ClassPoint import Point
from connectionData import *

#dxf = dxfgrabber('KN848832_3_2_I.dxf') # katastralna mapa
dxf = dxfgrabber.readfile("UCS_45_MaSk_170511_konfrontacny_vykres_nesahat.dxf") # vykres
#entities = dxf.modelspace()
layers = dxf.layers         # zoznam pouzitych vrstiev vo vykrese
entities = dxf.entities     # zoznam prvkov vo vykrese
print("DXF version: {}".format(dxf.dxfversion))  # dxf version
header_var_count = len(dxf.header)  # dict of dxf header vars
layer_count = len(dxf.layers)  # collection of layer definitions
block_definition_count = len(dxf.blocks)  # dict like collection of block definitions
entity_count = len(dxf.entities)  # list like collection of entities

connection = psycopg2.connect(DB)  # pripoenie k db
connection.autocommit = True
cursor = connection.cursor()

for layer in layers:
    layerName = (layer.name).replace("-", "_")
    if layerName == '0':
        continue
    print layerName
    cursor.execute('DROP TABLE IF EXISTS ' + layerName)
    cursor.execute('CREATE TABLE ' + layerName + ' (ID INT NOT NULL, typ CHAR(50),geom GEOMETRY, PRIMARY KEY (ID))')

    id = 1
    # pocitadla entit
    line_count, polyline_count, pw_polyline_count, arc_count, ellipse_count, circle_count, point_count, dsolid, dface_count, k = 0,0, 0, 0, 0, 0, 0, 0, 0, 0

    for entity in entities:  # vyber entit podla typu
        k=k+1
        if entity.dxftype == "POINT":
            point_count = point_count + 1
            point = ogr.Geometry(ogr.wkbPoint)
            point.AddPoint(entity.point[0], entity.point[1])
            wkt = point.ExportToWkt()
            cursor.execute("INSERT INTO " + layerName + " (ID, typ, geom)" + "VALUES (%s, %s, ST_GeometryFromText(%s, %s))", (
                id, entity.dxftype, wkt, epsg))
            id = id+1

        elif entity.dxftype == "LINE":
            line_count = line_count+1
            line = ogr.Geometry(ogr.wkbLineString)
            start = entity.start
            end = entity.end
            line.AddPoint(start[0], start[1], start[2])
            line.AddPoint(end[0], end[1], end[2])
            wkt = line.ExportToWkt()
            cursor.execute("INSERT INTO " + layerName + " (ID, typ, geom) " + "VALUES(%s, %s, ST_GeometryFromText(%s, %s))", (
                id, entity.dxftype, wkt, epsg))
            id = id + 1

        elif entity.dxftype == "POLYLINE":
            polyline_count = polyline_count+1
            vertices = entity.points
            vertices_count = len(vertices)
            line = ogr.Geometry(ogr.wkbLineString)
            for i in range(vertices_count):
                line.AddPoint(vertices[i][0],vertices[i][1],vertices[i][2])
            wkt = line.ExportToWkt()
            cursor.execute("INSERT INTO " + layerName + " (ID, typ, geom) " + "VALUES(%s, %s, ST_GeometryFromText(%s, %s))", (
                id, entity.dxftype, wkt, epsg))
            id = id + 1

        elif entity.dxftype == "LWPOLYLINE":
            pw_polyline_count = pw_polyline_count+1
            vertices = entity.points
            vertices_count = len(vertices)
            line = ogr.Geometry(ogr.wkbLineString)
            for i in range(vertices_count):
                line.AddPoint(vertices[i][0],vertices[i][1])
            wkt = line.ExportToWkt()
            cursor.execute("INSERT INTO " + layerName + " (ID, typ, geom) " + "VALUES(%s, %s, ST_GeometryFromText(%s, %s))", (
                id, entity.dxftype, wkt, epsg))
            id = id + 1

        elif entity.dxftype == "ARC":
            arc_count = arc_count+1
            centerPoint = Point(entity.center[0], entity.center[1], entity.center[2])
            radius = entity.radius
            start_angle = m.radians(entity.start_angle)
            end_angle = m.radians(entity.end_angle)
            endPoint = Point(radius * m.cos(end_angle), m.sin(end_angle), entity.center[2])
            line = ogr.Geometry(ogr.wkbLineString)
            while start_angle < end_angle:
                p = Point(radius * m.cos(start_angle), radius * m.sin(start_angle), entity.center[2])
                line.AddPoint(p.getX(), p.getY())
                start_angle = start_angle + m.radians(1)
            line.AddPoint(endPoint.getX(), endPoint.getY())
            wkt = line.ExportToWkt()
            cursor.execute("INSERT INTO " + layerName + " (ID, typ, geom)" + "VALUES(%s, %s, ST_GeometryFromText(%s, %s))", (
                id, entity.dxftype, wkt, epsg))
            id = id + 1

        '''elif entity.dxftype == "ELLIPSE":
            ellipse_count = ellipse_count+1
            centerPoint = Point(entity.center[0], entity.center[1], entity.center[2])
            majorAxisPoint = Point(entity.major_axis[0], entity.major_axis[1], entity.major_axis[2])
            start_param = entity.start_param
            end_param = entity.end_param
            #print start_param, end_param
            print "ellipse center point x = {0}, y = {1}, z = {2}".format(centerPoint.getX(), centerPoint.getY(), centerPoint.getZ())
            #print majorAxisPoint.getX(), majorAxisPoint.getY(), majorAxisPoint.getZ()

        elif entity.dxftype == "CIRCLE":
            circle_count = circle_count+1
            centerPoint = Point(entity.center[0], entity.center[1], entity.center[2])
            print centerPoint.getX(), centerPoint.getY(), centerPoint.getZ()

        elif entity.dxftype == "3DSOLID":
            dsolid_count = dsolid+1
        elif entity.dxftype == "3DFACE":
            dface_count = dface_count+1'''

    cursor.execute("CREATE INDEX " + layerName + "_index ON " + layerName + " USING GIST(geom)")

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

print line_count+polyline_count+pw_polyline_count+arc_count+ellipse_count