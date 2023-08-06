import arcpy

def createManholeFeatureLayer(manholeFC): # Select manholes
    # Delete existing feature layer
    arcpy.Delete_management("manholeSelection")
    # Make feature layer for manholes
    arcpy.MakeFeatureLayer_management(manholeFC, "manholeSelection")

def createInspectionArea(areaFC): # Select inspection area
    # Delete existing feature layer
    arcpy.Delete_management("areaSelection")
    #Make feature Layer for inspecion area
    arcpy.MakeFeatureLayer_management(areaFC, "areaSelection")
    
def createShapefile(area, path, name):    #Output selected manholes
    # Select specifc sewer service area from user input
    areaQuery = '"MajorServi" =' + "'"+ area + "'"
    arcpy.SelectLayerByAttribute_management("areaSelection",'NEW_SELECTION', areaQuery)
    # Select all manholes in the specified sewer service area
    arcpy.SelectLayerByLocation_management("manholeSelection", "WITHIN", "areaSelection")
    # Create a subselection of all active manholes in specified sewer service area 
    manholeQuery = '"WATERTYPE" = ' + "'Sewage'"
    arcpy.SelectLayerByAttribute_management("manholeSelection",'SUBSET_SELECTION', manholeQuery)
    # Create output name for feature class
    outputFC = path + "\\"+ name + ".shp"
    # Delete exisitng file if it exists
    if arcpy.Exists(outputFC):
        arcpy.Delete_management(outputFC)
        arcpy.CopyFeatures_management ("manholeSelection", outputFC)
    else:
        arcpy.CopyFeatures_management ("manholeSelection", outputFC)

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
