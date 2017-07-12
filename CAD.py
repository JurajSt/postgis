import arcpy
import glob
import os
import ogr
from connectionData import pathCad, pathShp, typeCadFile, field
arcpy.env.overwriteOutput=True
gdb = pathCad +"/dgn.gdb"
arcpy.env.workspace = gdb
arcpy.CreateFileGDB_management(pathCad, "dgn.gdb")
reference_scale = "1500"
#globTxt = "r,"+ pathCad +"/*."+typeCadFile
for file in glob.glob(r"data/dgn_dxf/*.dgn"):
    outDS = arcpy.ValidateTableName(os.path.splitext(os.path.basename(file))[0])
    arcpy.CADToGeodatabase_conversion(file, gdb, outDS, reference_scale)

datasetList = arcpy.ListDatasets('*','Feature')
for dataset in datasetList:
    arcpy.env.workspace = dataset
    fcList = arcpy.ListFeatureClasses()
    for fc in fcList:
        #if fc == "Point" or fc == "Polyline" or fc == "Polygon":
        print fc
        inFeatures = fc
        outLocation = pathCad
        outFeatureClass = fc
        arcpy.FeatureClassToFeatureClass_conversion(inFeatures, outLocation, outFeatureClass)