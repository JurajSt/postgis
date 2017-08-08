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

def dxfToPostgis(dxfFile):
    #dxf = dxfgrabber('KN848832_3_2_I.dxf') # katastralna mapa
    dxf = dxfgrabber.readfile(dxfFile) # vykres sa musi nachadzat pri skripte
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
        print entity.dxftype
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
    '''
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
    '''

    cursor.execute('DROP TABLE IF EXISTS test_polygon')
    cursor.execute('CREATE TABLE test_polygon (ID INT NOT NULL, objekt CHAR(50),geom GEOMETRY, PRIMARY KEY (ID))')



    vertices = []
    for geo in geometry:
        re = geo.replace(")","")
        sp = re.split("(")
        sp = sp[1].split(",")
        vertices.append(sp)

    polygon_geometry = []
    id = 1
    indexes = []
    for vertex in vertices:     # vytvrenie polygonov z uzavretych linii (kruh, elipsa...)
        firstVertex = vertex[0]
        lastVertex = vertex[-1]
        indInList = vertices.index(vertex)
        #print firstVertex, lastVertex
        if firstVertex == lastVertex:
            obj = "ring"
            ring = ogr.Geometry(ogr.wkbLinearRing)  # Create ring
            poly = ogr.Geometry(ogr.wkbPolygon)  # Create polygon
            for value in vertex:
                val = value.split()
                ring.AddPoint(float(val[0]), float(val[1]))
            poly.AddGeometry(ring)
            wkt = poly.ExportToWkt()
            polygon_geometry.append(wkt)
            cursor.execute("INSERT INTO test_polygon (ID, objekt, geom)" + "VALUES(%s, %s, ST_GeometryFromText(%s, %s))",
                           (id, obj, wkt, epsg))
            id = id+1

        else:
            i = 0
            index = []
            while i < len(vertices):
                if i == indInList:
                    index.append(i)
                    i = i + 1
                    continue
                #print vertices[i]
                nextFirstVertex = vertices[i][0]
                nextLastVertex = vertices[i][-1]
                #print "last", lastVertex
                if lastVertex == nextFirstVertex:
                    lastVertex = nextLastVertex
                    index.append(i)
                    #print "=", firstVertex, nextLastVertex
                    if firstVertex == nextLastVertex:
                        indexes.append(index)
                        break
                i= i+1
    # kontrola
    polygon = []
    for ind in indexes:
        lineToPoly = []
        a = vertices[ind[0]][0]
        b = vertices[ind[-1]][-1]
        if a==b:
            for i in ind:
                lineToPoly.append(vertices[i])
            polygon.append(lineToPoly)
    obj = "ring"
    i = 0
    while i < len(polygon):
        ring = ogr.Geometry(ogr.wkbLinearRing)  # Create ring
        j = 0
        while j <len(polygon[i]):
            if j == 0:
                for value in polygon[i][j]:
                    sp = value.split()
                    ring.AddPoint(float(sp[0]), float(sp[1]))
            elif j > 0:
                k = 1
                while k < len(polygon[i][j]):
                    sp = polygon[i][j][k].split()
                    ring.AddPoint(float(sp[0]), float(sp[1]))
                    k = k + 1
            j = j+1
        poly = ogr.Geometry(ogr.wkbPolygon)  # Create polygon
        poly.AddGeometry(ring)
        wkt = poly.ExportToWkt()
        cursor.execute(
            "INSERT INTO test_polygon (ID, objekt, geom)" + "VALUES(%s, %s, ST_GeometryFromText(%s, %s))",
            (id, obj, wkt, epsg))
        id = id + 1
        i = i + 1


    cursor.execute("DROP INDEX IF EXISTS test_pol_index")
    cursor.execute("CREATE INDEX test_pol_index ON test_polygon USING GIST(geom)")
    return 0

