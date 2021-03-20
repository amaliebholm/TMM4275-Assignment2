# NX 1957
# Journal created by Kasper on Sat Mar 20 18:05:04 2021 Vest-Europa (normaltid)
#
import math
import sys
import clr

# Managed NXOpen DLL's goes also in this directory
sys.path.append("C:\\Program Files\\Siemens\\NX1953\\NXBIN\\python")

clr.AddReference('NXOpen')

import NXOpen
import NXOpen.Gateway
def main() : 

    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display
    workPart.RuleManager.Reload(True)
    
    markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Add New Child Rule")
    
    workPart.RuleManager.CreateDynamicRule("root:", "railorder", "Child", "{\n Class, Rail_Order; \n}", None)
    
    nErrs1 = workPart.RuleManager.DoKfUpdate(markId1)
    
    # ----------------------------------------------
    #   Menu: Fit
    # ----------------------------------------------
    workPart.ModelingViews.WorkView.Fit()
    
    # ----------------------------------------------
    #   Menu: File->Export->Image...
    # ----------------------------------------------
    markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
    
    theUI = NXOpen.UI.GetUI()
    
    imageExportBuilder1 = theUI.CreateImageExportBuilder()
    
    imageExportBuilder1.RegionMode = False
    
    regiontopleftpoint1 = [None] * 2 
    regiontopleftpoint1[0] = 0
    regiontopleftpoint1[1] = 0
    imageExportBuilder1.SetRegionTopLeftPoint(regiontopleftpoint1)
    
    imageExportBuilder1.RegionWidth = 1
    
    imageExportBuilder1.RegionHeight = 1
    
    imageExportBuilder1.FileFormat = NXOpen.Gateway.ImageExportBuilder.FileFormats.Png
    
    imageExportBuilder1.FileName = "K:\\Biblioteker\\Dokumenter\\Skole\\Automatisering\\TMM4275-Assignment2\\rail_model_image.png"
    
    imageExportBuilder1.BackgroundOption = NXOpen.Gateway.ImageExportBuilder.BackgroundOptions.Original
    
    imageExportBuilder1.EnhanceEdges = False
    
    nXObject1 = imageExportBuilder1.Commit()
    
    theSession.DeleteUndoMark(markId2, "Export Image")
    
    imageExportBuilder1.Destroy()
    
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()