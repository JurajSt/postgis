import psycopg2
from connectionData import *
import xlsxwriter

connection = psycopg2.connect(DB)  # pripoenie k db
connection.autocommit = True
cursor = connection.cursor()

cursor.execute('''SELECT parcelne_cislo As pc, objekt, area FROM ''' + tableName)
rows = cursor.fetchall()

def CreateOutput(pathOutputXLS):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(pathOutputXLS)
    worksheet = workbook.add_worksheet()

    worksheet.write(0,0, "Parcela")
    worksheet.write(0,1, "Plocha")
    worksheet.write(0,2, "Objekt")
    r = 1
    c = 0
    for row in rows:
        cp = row[0].split()[0]
        area = row[2]
        objekt = row[1].split()[0]
        worksheet.write(r,c,cp)
        worksheet.write(r, c+1, area)
        worksheet.write(r, c+2, objekt)
        r=r+1

    workbook.close()
    cursor.close()
    return 0