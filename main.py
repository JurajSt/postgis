import psycopg2
from connectionData import DB
from connectionData import pathShp
from connectionData import pathCad
from connectionData import field
from connectionData import typeCadFile
import db, calculateArea


importToPostgres = db.ImportShpToPostgres(DB, pathShp, field)       #import vstupnej vrstvy (kladpar, linie a polygony)
importToPostgres2 = db.ImportShpToPostgres(DB, pathCad, 'Layer')    # import converotvane cad subory
importToPostgres3 = db.ImportShpToPostgres(DB, 'data/parcely_body', 'TEXT')    #import bodovej vrstvy z cislami parcely
calcArea = calculateArea.columnArea(importToPostgres)       # vypocet plochy pre parcely
calcArea2 = calculateArea.columnArea(importToPostgres2)     # vypocet plochy pre objekty