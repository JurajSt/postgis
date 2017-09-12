import xlsxwriter
import psycopg2
from connectionData import *

def Output(rows, name):
    workbook = xlsxwriter.Workbook(pathOutputXLS+name+".xlsx")
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "Parcela")
    r=1
    for row in rows:
        row = row[0].split()[0]
        print row
        worksheet.write(r, 0, row)
        r= r+1
    workbook.close()
    return 0