import psycopg2
from connectionData import DB

connection = psycopg2.connect(DB)
connection.autocommit = True
cursor = connection.cursor()


def columnArea(tableName):
    cursor.execute("ALTER TABLE " + tableName + " DROP COLUMN IF EXISTS area")
    cursor.execute("ALTER TABLE " + tableName + " ADD COLUMN area double precision")
    cursor.execute("UPDATE " + tableName + " SET area=ST_AREA(intersect_geom)")

    return 0
