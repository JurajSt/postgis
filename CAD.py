import arcpy
import glob
import os
from connectionData import pathCad, pathShp, typeCadFile
arcpy.env.overwriteOutput=True

gdb = pathCad +"/dgn.gdb"
arcpy.env.workspace = gdb
arcpy.CreateFileGDB_management(pathCad, "dgn.gdb")
reference_scale = "1500"
#globTxt = "r,"+ pathCad +"/*."+typeCadFile
for file in glob.glob("r"+pathCad+"/.*"+typeCadFile):
    outDS = arcpy.ValidateTableName(os.path.splitext(os.path.basename(file))[0])
    arcpy.CADToGeodatabase_conversion(file, gdb, outDS, reference_scale)

datasetList = arcpy.ListDatasets('*','Feature')
for dataset in datasetList:
    arcpy.env.workspace = dataset
    fcList = arcpy.ListFeatureClasses()
    for fc in fcList:
            #print arcpy.env.workspace, fc
        inFeatures = fc
        outLocation = pathShp
        outFeatureClass = fc
        arcpy.FeatureClassToFeatureClass_conversion(inFeatures, outLocation, outFeatureClass)