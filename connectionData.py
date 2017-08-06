hostname = 'localhost'
username = 'postgres'
password = 'sql'
database = 'postgis_23_sample'
pathKm = 'data/test_data/km'   #ceta ku katastralnej mape
pathCad = 'data/test_data/dxf'
typeCadFile = 'dgn'
field = 'Vrstva'    # nazov atributu ktory sa nahra do db
field1 = 'Parcela'    # nazov atributu ktory sa nahra do db
field2 = 'KU'
tableName = 'inters'    # nazov tabulky ktora bude vytvorena intersectom
epsg = 5514
pathOutputXLS = 'test.xlsx'

DB = "host=" + hostname + " user=" + username + " password=" + password + " dbname=" + database
