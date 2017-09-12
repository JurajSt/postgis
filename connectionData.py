# pripojenie k db
hostname = 'localhost'
username = 'postgres'
password = 'sql'
database = 'postgis_23_sample'
DB = "host=" + hostname + " user=" + username + " password=" + password + " dbname=" + database

# cesty k vstupom a vystupom
pathKm = 'data/test_data/km'    # ceta ku katastralnej mape
pathCad = 'data/test_data/dxf'  # cesta k dxf suborom
pathOutputXLS = 'data/output/'    # cesta k xsl suboru
typeCadFile = 'dgn'

# polia ktore sa importuju z shp vrstvy kat. mapy
field = 'Vrstva'
field1 = 'Parcela'
field2 = 'KU'

tableName = 'inters'

# kod suradnicoveho systemu
epsg = 5514

#dxfFile = 'SO_47-33-13_170309_finalny_model_V8i.dxf'            #SO_47-33-13_170309_finalny_model_V8i

