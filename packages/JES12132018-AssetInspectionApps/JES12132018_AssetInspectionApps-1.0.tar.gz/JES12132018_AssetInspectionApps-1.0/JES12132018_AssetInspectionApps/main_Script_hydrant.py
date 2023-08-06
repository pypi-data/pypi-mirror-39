import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox 
from PyQt5.QtCore import QCoreApplication

import gui_Project_hydrant, core_function_hydrant
# =======================================
# GUI event handler and related functions
# =======================================
#
# query and direct input functions
       
def selectHydrantShapefile():    
    """open file dialog to select exising shapefile and if accepted, update GUI accordingly"""
    fileName, _ = QFileDialog.getOpenFileName(mainWindow,"Select fire hydrant shapefile", "","Shapefile (*.shp)")
    if fileName:
        ui.OpenHydrantShapefileLE.setText(fileName)

def selectInspectionAreaShapefile():    
    """open file dialog to select exising shapefile and if accepted, update GUI accordingly"""
    fileName, _ = QFileDialog.getOpenFileName(mainWindow,"Select inspection area shapefile", "","Shapefile (*.shp)")
    if fileName:
        ui.OpenInspAreaShapefileLE.setText(fileName)

def createNewShapefile():
    try:
        ui.statusbar.clearMessage()
        ui.statusbar.showMessage('Creating shapefile... please wait!')
        hydrantFC = ui.OpenHydrantShapefileLE.text()
        areaFC = ui.OpenInspAreaShapefileLE.text()
        path = ui.outputPathLE.text()
        name = ui.fileNameLE.text()
        core_function_hydrant.createHydrantFeatureLayer(hydrantFC)
        core_function_hydrant.createInspectionArea(areaFC)
        core_function_hydrant.createShapefile(path, name)
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
ui = gui_Project_hydrant.Ui_MainWindow()
ui.setupUi(mainWindow)

#==========================================
# connect signals
#==========================================
ui.OpenHydrantShapefileTB.clicked.connect(selectHydrantShapefile)
ui.OpenInspAreaShapefileTB.clicked.connect(selectInspectionAreaShapefile)
ui.outputPathTB.clicked.connect(selectFileLocation)
ui.shapefileCreateNewPB.clicked.connect(createNewShapefile)

#============================================
# test availability and if run as script tool
#============================================

arcpyAvailable = core_function_hydrant.importArcpyIfAvailable()
if not arcpyAvailable:
    ui.statusbar.showMessage('arcpy not available. Adding to shapefiles and layers has been disabled.')

else:
    import arcpy
    if core_function_hydrant.runningAsScriptTool():
        runningAsScriptTool = True
        createNewShapefile()
    else:
        ui.statusbar.showMessage(ui.statusbar.currentMessage() + 'Not running as a script tool in ArcMap. Shapefile will still be created.')
#=======================================
# run app
#=======================================
mainWindow.show()
sys.exit(app.exec_())