import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication

import gui_Project_manhole, core_function_manhole
# =======================================
# GUI event handler and related functions
# =======================================
#
# query and direct input functions
       
def selectManholeShapefile():    
    """open file dialog to select exising shapefile and if accepted, update GUI accordingly"""
    fileName, _ = QFileDialog.getOpenFileName(mainWindow,"Select shapefile", "","Shapefile (*.shp)")
    if fileName:
        ui.OpenManholeShapefileLE.setText(fileName)

def selectInspectionAreaShapefile():    
    """open file dialog to select exising shapefile and if accepted, update GUI accordingly"""
    fileName, _ = QFileDialog.getOpenFileName(mainWindow,"Select shapefile", "","Shapefile (*.shp)")
    if fileName:
        ui.OpenSewerAreaShapefileLE.setText(fileName)

def makeAreaList(): 
    """update sewer area combo box with sewer basin names"""
    ui.PickSewerAreaCB.clear()
    areas = ['Alcovy', 'Beaver Ruin', 'Brooks Road', 'Crooked Creek', 'East Park Place', 'Hog Mountain', 'Ivy Creek', 
             'Level Creek', 'Lower Big Haynes', 'Mulberry', 'No Business Creek', 'Norris Lake', 'North Chattahoochee', 
             'North Fork Peachtree', 'Patterson', 'Pole Bridge', 'Ross Road', 'Suwanee Creek', 'Wolf Creek', 'Yellow River'] 
    
    for basin in areas:
        ui.PickSewerAreaCB.addItem(str(basin))
    
    
def createNewShapefile():
    try:
        ui.statusbar.clearMessage()
        ui.statusbar.showMessage('Creating shapefile... please wait!')
        manholeFC = ui.OpenManholeShapefileLE.text()
        areaFC = ui.OpenSewerAreaShapefileLE.text()
        path = ui.outputPathLE.text()
        name = ui.fileNameLE.text()
        area = ui.PickSewerAreaCB.currentText()
        core_function_manhole.createManholeFeatureLayer(manholeFC)
        core_function_manhole.createInspectionArea(areaFC)
        core_function_manhole.createShapefile(area, path, name)
        ui.statusbar.showMessage('New shapefile has been created.You may now close the form.')
           
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
ui = gui_Project_manhole.Ui_MainWindow()
ui.setupUi(mainWindow)


#==========================================
# connect signals
#==========================================
makeAreaList()
ui.OpenManholeShapefileTB.clicked.connect(selectManholeShapefile)
ui.OpenSewerAreaShapefileTB.clicked.connect(selectInspectionAreaShapefile)
ui.outputPathTB.clicked.connect(selectFileLocation)
ui.shapefileCreateNewPB.clicked.connect(createNewShapefile)

#============================================
# test availability and if run as script tool
#============================================
arcpyAvailable = core_function_manhole.importArcpyIfAvailable()
if not arcpyAvailable:
    ui.statusbar.showMessage('arcpy not available. Adding to shapefiles and layers has been disabled.')

else:
    import arcpy
    if core_function_manhole.runningAsScriptTool():
        runningAsScriptTool = True
        createNewShapefile()
    else:
        ui.statusbar.showMessage(ui.statusbar.currentMessage() + 'Not running as a script tool in ArcMap. Shapefile will still be created.')
        
#=======================================
# run app
#=======================================
mainWindow.show()
sys.exit(app.exec_())