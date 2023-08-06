import arcpy

def createHydrantFeatureLayer(hydrantFC): # Select potable hydrants
    # Delete existing feature layer
    arcpy.Delete_management("hydrantSelection") 
    # Make feature layer for fire hydrants
    arcpy.MakeFeatureLayer_management(hydrantFC, "hydrantSelection")

def createInspectionArea(areaFC): # Select inspection area
    # Delete existing feature layer
    arcpy.Delete_management("areaSelection")
    #Make feature Layer for inspecion area
    arcpy.MakeFeatureLayer_management(areaFC, "areaSelection")
    
def createShapefile(path, name):    #Output selected fire hydrants
    # Select potable fire hydrants in selected inspection area
    hydrantQuery= '"WATERTYPE" ='+ "'Potable'"
    # Select inspection area
    arcpy.SelectLayerByLocation_management("hydrantSelection", "WITHIN", "areaSelection")
    # Create a subselection of all potav=ble fire hydrants in selected inspection area
    arcpy.SelectLayerByAttribute_management("hydrantSelection",'SUBSET_SELECTION', hydrantQuery)
    # Create output name for feature class
    outputFC = path + "\\"+ name + ".shp"
    # Delete exisitng file if it exists
    if arcpy.Exists(outputFC):
        arcpy.Delete_management(outputFC)
        arcpy.CopyFeatures_management ("hydrantSelection", outputFC)
    else:
        arcpy.CopyFeatures_management ("hydrantSelection", outputFC)

def importArcpyIfAvailable():
    """test whether arcpy is available for import"""
    try: # test whether we can import arcpy
        import arcpy
    except:
        return False
    return True

def runningAsScriptTool():
    """test whether this program is run as a script tool in ArcGIS"""
    try: # test whether we can access an opened ArcGIS project
        import arcpy
        arcpy.mp.ArcGISProject("CURRENT")
    except:
        return False
    return True
