import psycopg2
from connectionData import DB
from connectionData import *
from connectionData import pathCad
from connectionData import field
from connectionData import typeCadFile
import db


importToPostgres = db.ImportShpToPostgres(DB, pathKm, field, field1, field2)       #import vstupnej vrstvy (kladpar, linie a polygony)
#importToPostgres2 = db.ImportShpToPostgres(DB, pathCad, 'Layer')    # import converotvane cad subory
#importToPostgres3 = db.ImportShpToPostgres(DB, 'data/parcely_body', 'TEXT')    #import bodovej vrstvy z cislami parcely
#calcArea = calculateArea.columnArea(importToPostgres)       # vypocet plochy pre parcely
#calcArea2 = calculateArea.columnArea(importToPostgres2)     # vypocet plochy pre objekty