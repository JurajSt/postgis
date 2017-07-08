import psycopg2
from connectionData import DB
from connectionData import pathShp
from connectionData import pathCad
from connectionData import field
from connectionData import typeCadFile
import db, CAD

convertCad = CAD.CadToShp(pathCad, pathShp, typeCadFile)
importToPostgres = db.ImportShpToPostgres(DB, pathShp, field)
