import psycopg2

from connectionData import DB

connection = psycopg2.connect(DB)
connection.autocommit = True
cursor = connection.cursor()


def columnArea(tables):
    for tableName in tables:
        cursor.execute("ALTER TABLE " + tableName + " ADD COLUMN area double precision")
        cursor.execute("UPDATE " + tableName + " SET area=ST_AREA(geom)")
   # connection.commit()
    return 0
