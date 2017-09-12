from connectionData import *
import db
import DXFtoPostgis
import calculateArea
import postgisIntersection
import CreateOutput
import os
import sklad


tablesKm = db.ImportShpToPostgres(DB, pathKm, field, field1, field2)       #import kat. map; dostanem zoznam importovanych Km

files = ([name for name in os.listdir(pathCad)])
count = 0
targets = []
for file in files:
    if file.endswith('.dxf'):
        count = count + 1
        targets.append(file)
        #print(file)
    #print "Total number of files = " + str(count)
    tables = []
    for file in targets:
        fileName = file.split(".")[0]   # nazov dxf suboru
        importDxfToPostgres = DXFtoPostgis.dxfToPostgis(fileName)
        dxfPoly = sklad.dxfToPoly(importDxfToPostgres)
intersection = postgisIntersection.intersection()
calcArea2 = calculateArea.columnArea(tableName)     # vypocet plochy pre objekty
output = CreateOutput.CreateOutput(pathOutputXLS)