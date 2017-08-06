from connectionData import *
import db
import DXFtoPostgis
import calculateArea
import postgisIntersection
import CreateOutput


importShpToPostgres = db.ImportShpToPostgres(DB, pathKm, field, field1, field2)       #import vstupnej vrstvy (kladpar, linie a polygony)
importDxfToPostgres = DXFtoPostgis.dxfToPostgis('vzory.dxf')
intersection = postgisIntersection.intersection()
calcArea2 = calculateArea.columnArea(tableName)     # vypocet plochy pre objekty
output = CreateOutput.CreateOutput(pathOutputXLS)