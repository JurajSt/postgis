import os.path
import psycopg2
import osgeo.ogr


def ImportShpToPostgres(DB, pathShp, field, field1, field2):
    connection = psycopg2.connect(DB)
    connection.autocommit = True
    cursor = connection.cursor()

    files = ([name for name in os.listdir(pathShp)])
    count = 0
    targets = []
    for file in files:
        if file.endswith('.shp'):
            count = count + 1
            targets.append(file)
            #print(file)
    print "Total number of files = " + str(count)
    tables = []
    for file in targets:
        fileName = file.split(".")[0]
        tables.append(fileName)
        print fileName
        srcFile = os.path.join(pathShp, file)
        shapefile = osgeo.ogr.Open(srcFile)
        layer = shapefile.GetLayer(0)
        cursor.execute('DROP TABLE IF EXISTS '+fileName)
        cursor.execute('CREATE TABLE '+ fileName+' (ID INT NOT NULL, '+field+' CHAR(255), '+field1+' CHAR(255), '+field2+' CHAR(255),geom GEOMETRY, PRIMARY KEY (ID))')
        for i in range(layer.GetFeatureCount()):
            feature = layer.GetFeature(i)
            fieldValue = feature.GetField(field).decode("Latin-1")
            fieldValue1 = feature.GetField(field1).decode("Latin-1")
            fieldValue2 = feature.GetField(field2).decode("Latin-1")
            try:
                wkt = feature.GetGeometryRef().ExportToWkt()
                print i, wkt
            except AttributeError as e:
                print e
                continue
            cursor.execute("INSERT INTO "+fileName+" (ID,"+field+","+field1+","+field2+",geom) " +"VALUES (%s, %s, %s, %s, ST_GeometryFromText(%s, " +"5514))",
                            (i, fieldValue.encode("utf8"), fieldValue1.encode("utf8"), fieldValue2.encode("utf8"), wkt))
        cursor.execute("CREATE INDEX "+fileName+"_index ON "+fileName+" USING GIST(geom)")
    #connection.commit()
    return tables
