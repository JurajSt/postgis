import os.path
import psycopg2
import osgeo.ogr
import arcpy
import glob

def ImportShpToPostgres(DB, path, field):
    connection = psycopg2.connect(DB)
    connection.autocommit = True
    cursor = connection.cursor()

    files = ([name for name in os.listdir(path)])
    count = 0
    targets = []
    for file in files:
        if file.endswith('.shp'):
            count = count + 1
            targets.append(file)
            #print(file)
    print "Total number of files = " + str(count)

    for file in targets:
        fileName = file.split(".")[0]
        print fileName
        srcFile = os.path.join(path, file)
        shapefile = osgeo.ogr.Open(srcFile)
        layer = shapefile.GetLayer(0)
        cursor.execute('DROP TABLE IF EXISTS '+fileName)
        cursor.execute('CREATE TABLE '+ fileName+' ('+field+' CHAR(255),geom GEOMETRY)')
        for i in range(layer.GetFeatureCount()):
            feature = layer.GetFeature(i)
            fieldName = feature.GetField(field).decode("Latin-1")
            wkt = feature.GetGeometryRef().ExportToWkt()
            cursor.execute("INSERT INTO "+fileName+" ("+field+",geom) " +"VALUES (%s, ST_GeometryFromText(%s, " +"5514))", (fieldName.encode("utf8"), wkt))

    connection.commit()
    return 0
