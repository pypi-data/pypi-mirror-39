import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication

import gui_Project_stormdrain, core_function_stormdrain
# =======================================
# GUI event handler and related functions OpenManholeShapefileLE
# =======================================
#
# query and direct input functions
       
def selectStormdrainShapefile():    
    """open file dialog to select exising shapefile and if accepted, update GUI accordingly"""
    fileName, _ = QFileDialog.getOpenFileName(mainWindow,"Select shapefile", "","Shapefile (*.shp)")
    if fileName:
        ui.OpenStormdrainShapefileLE.setText(fileName)

def selectInspectionAreaShapefile():    
    """open file dialog to select exising shapefile and if accepted, update GUI accordingly"""
    fileName, _ = QFileDialog.getOpenFileName(mainWindow,"Select shapefile", "","Shapefile (*.shp)")
    if fileName:
        ui.OpenStormBasinShapefileLE.setText(fileName)

def makeAreaList(): 
    """update sewer area combo box with sewer basin names"""
    ui.PickStormBasinCB.clear()
    areas = ['ALCOVY', 'APALACHEE', 'BEAVER RUIN', 'BIG HAYNES', 'BROMOLOW', 'BRUSHY FORK', 'CAMP CREEK', 'CEDAR CREEK', 
             'CROOKED CREEK', 'HOPKINS CREEK', 'JACKS CREEK', 'JACKSON CREEK', 'LEVEL CREEK', 'LITTLE SUWANEE', 
             'LOWER CHATTAHOOCHEE', 'LOWER YELLOW', 'MULBERRY', 'NO BUSINESS', 'NORTH FORK', 'PEW CREEK', 'POUND CREEK',
             'RICHLAND', 'SHETLEY', 'SHOAL', 'SUWANEE', 'SWEETWATER', 'TURKEY', 'UPPER CHATTAHOOCHEE 1', 'UPPER CHATTAHOOCHEE 2',
             'UPPER CHATTAHOOCHEE 3', 'UPPER YELLOW', 'WATSON CREEK'] 
    
    for basin in areas:
        ui.PickStormBasinCB.addItem(str(basin))
    
    
def createNewShapefile():
    try:
        ui.statusbar.clearMessage()
        ui.statusbar.showMessage('Creating shapefile... please wait!')
        stormdrainFC = ui.OpenStormdrainShapefileLE.text()
        areaFC = ui.OpenStormBasinShapefileLE.text()
        path = ui.outputPathLE.text()
        name = ui.fileNameLE.text()
        area = ui.PickStormBasinCB.currentText()
        core_function_stormdrain.createStormdrainFeatureLayer(stormdrainFC)
        core_function_stormdrain.createInspectionArea(areaFC)
        core_function_stormdrain.createShapefile(area, path, name)
        ui.statusbar.showMessage('New shapefile has been created. You may now close the form.')
           
    except Exception as e:
        QMessageBox.information(mainWindow, 'Operation failed', 'Creating new shapefile failed with '+ str(e.__class__) + ': ' + str(e), QMessageBox.Ok )
        ui.statusbar.clearMessage()

def selectFileLocation():    
    """open file dialog to select exising file directrory where the shapefile will be saved"""
    pathName = QFileDialog.getExistingDirectory(mainWindow, "Select Output Folder")
    if pathName:
        ui.outputPathLE.setText(pathName)


           
#==========================================
# create app and main window + dialog GUI
# =========================================

app = QCoreApplication.instance()
if app is None:
    app= QApplication(sys.argv)

app.aboutToQuit.connect(app.deleteLater)

# set up main window 

mainWindow = QMainWindow()
ui = gui_Project_stormdrain.Ui_MainWindow()
ui.setupUi(mainWindow)


#==========================================
# connect signals
#==========================================
makeAreaList()
ui.OpenStormdrainShapefileTB.clicked.connect(selectStormdrainShapefile)
ui.OpenStormBasinShapefileTB.clicked.connect(selectInspectionAreaShapefile)
ui.outputPathTB.clicked.connect(selectFileLocation)
ui.shapefileCreateNewPB.clicked.connect(createNewShapefile)

#============================================
# test availability and if run as script tool
#============================================

arcpyAvailable = core_function_stormdrain.importArcpyIfAvailable()
if not arcpyAvailable:
    ui.statusbar.showMessage('arcpy not available. Adding to shapefiles and layers has been disabled.')

else:
    import arcpy
    if core_function_stormdrain.runningAsScriptTool():
        runningAsScriptTool = True
        createNewShapefile()
    else:
        ui.statusbar.showMessage(ui.statusbar.currentMessage() + 'Not running as a script tool in ArcMap. Shapefile will still be created.')

#=======================================
# run app
#=======================================
mainWindow.show()
sys.exit(app.exec_())