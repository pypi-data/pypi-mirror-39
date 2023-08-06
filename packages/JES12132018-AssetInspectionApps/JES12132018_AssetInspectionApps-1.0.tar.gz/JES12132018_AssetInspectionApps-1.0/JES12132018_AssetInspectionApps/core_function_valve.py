import arcpy

def createValveFeatureLayer(valveFC): # Select valves: 6"-16" gate and butterfly valves only
    # Delete existing feature layer
    arcpy.Delete_management("valveSelection")
    # Make feature layer for valves
    arcpy.MakeFeatureLayer_management(valveFC, "valveSelection")

def createInspectionArea(areaFC): # Select inspection area
    # Delete existing feature layer
    arcpy.Delete_management("areaSelection")
    #Make feature Layer for inspecion area
    arcpy.MakeFeatureLayer_management(areaFC, "areaSelection")
    
def createShapefile(path, name):    #Output selected fire hydrants
    # Select all active gate and butterfly valves between 6 and 16 incehs in diameter
    valveQuery = '("VALVE_SIZE" >= 6 AND "VALVE_SIZE" <= 16)' + 'AND'+ '"WATERTYPE" ='+ "'Potable'" + 'AND' +  '"SUBTYPE" IN' + '( 1, 3)'
    # Select inspection area
    arcpy.SelectLayerByLocation_management("valveSelection", "WITHIN", "areaSelection")
    # Create a subselection of all selected valves in selected inspection area
    arcpy.SelectLayerByAttribute_management("valveSelection",'SUBSET_SELECTION', valveQuery)
    # Create output name for feature class
    outputFC = path + "\\"+ name + ".shp"
    # Delete exisitng file if it exists
    if arcpy.Exists(outputFC):
        arcpy.Delete_management(outputFC)
        arcpy.CopyFeatures_management ("valveSelection", outputFC)
    else:
        arcpy.CopyFeatures_management ("valveSelection", outputFC)

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
