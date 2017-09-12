import os
import DXFtoPostgis
from connectionData import *
import db
import intersect, Output


tablesKm = db.ImportShpToPostgres(DB, pathKm, field, field1, field2)       #import kat. map; dostanem zoznam importovanych Km  >> bude len jedna
print tablesKm
files = ([name for name in os.listdir(pathCad)])
count = 0
cadTables = []
for file in files:
    if file.endswith('.dxf'):
        count = count + 1
        fileName = file   # nazov dxf suboru
        name = fileName.split(".")[0]
        cadTables.append(name)
        importDxfToPostgres = DXFtoPostgis.dxfToPostgis(name, fileName)
print cadTables

for tab in tablesKm:
    for tab2 in cadTables:
        intersect = intersect.intersect(tab, tab2)
        rows = intersect[0]
        nam = intersect[1]
        output = Output.Output(rows, nam)
