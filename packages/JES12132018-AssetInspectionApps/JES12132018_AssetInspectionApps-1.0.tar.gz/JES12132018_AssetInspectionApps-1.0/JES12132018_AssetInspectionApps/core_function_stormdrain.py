import arcpy

def createStormdrainFeatureLayer(stormdrainFC): # Select stormdrains
    # Delete existing feature layer
    arcpy.Delete_management("stormdrainSelection")
    # Make feature layer for stormdrains
    arcpy.MakeFeatureLayer_management(stormdrainFC, "stormdrainSelection")
    
def createInspectionArea(areaFC): # Select inspection area
    # Delete existing feature layer
    arcpy.Delete_management("areaSelection")
    #Make feature Layer for stormwater drainage basin
    arcpy.MakeFeatureLayer_management(areaFC, "areaSelection")
    
def createShapefile(area, path, name):    #Output selected manholes
    # Select specifc stormwater drainage basin from user input
    areaQuery = '"SUBBASIN" =' + "'"+ area + "'"
    arcpy.SelectLayerByAttribute_management("areaSelection",'NEW_SELECTION', areaQuery)
    # Select all active county maintained catch basins, junction boxes, headwalls, yard inlets, and trench drains
    stormdrainQuery = stormdrainQuery = '"WATERTYPE" = ' + "'Storm'" + 'AND'+ '"SUBTYPE" IN' + '(1, 2, 3, 4, 5)' + 'AND'+ '"COUNTY_MAI" IN' + "('Y', 'Y1')"
    # Select inspection area
    arcpy.SelectLayerByLocation_management("stormdrainSelection", "WITHIN", "areaSelection")
    # Create a subselection of all selected stormdrains in selected stormwater drainage basin
    arcpy.SelectLayerByAttribute_management("stormdrainSelection",'SUBSET_SELECTION', stormdrainQuery)
    # Create output name for feature class
    outputFC = path + "\\"+ name + ".shp"
    # Delete exisitng file if it exists
    if arcpy.Exists(outputFC):
        arcpy.Delete_management(outputFC)
        arcpy.CopyFeatures_management ("stormdrainSelection", outputFC)
    else:
        arcpy.CopyFeatures_management ("stormdrainSelection", outputFC)

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
