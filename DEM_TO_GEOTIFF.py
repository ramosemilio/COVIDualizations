#DEM_TO_GEOTIFF v0.1
#By Emilio Ramos

#SCRIPT TO BE RUN IN QGIS TO BATCH PROCESS DEM HGT FILES FROM DEM_WRANGLER.py
#INTO GEOTIFFS FOR NUKE_UV_BATCHER.py

#GET OPEN LAYERS

export_list = ["N46W122", "N46W123","N46W124","N46W125"]
row_width = 4
column_height = 4


for dem in export_list:
    path_to_hgt = "S:\\DATA\\DEMS\\{}.hgt".format(dem)

    tile_coord = dem

    rlayer = QgsRasterLayer(path_to_hgt, tile_coord)
    if not rlayer.isValid():
        print("Layer failed to load!")

    #ADD TO PROJECT
    QgsProject.instance().addMapLayer(rlayer)

    renderer= rlayer.renderer()
    #REMOVE COLOR ENCHANCEMENT
    rlayer.setContrastEnhancement(QgsContrastEnhancement.NoEnhancement)

    bohLayer = rlayer
    entries = []
    # Define band1
    calc_entry = QgsRasterCalculatorEntry()
    calc_entry.ref = dem+'@1'
    calc_entry.raster = rlayer
    calc_entry.bandNumber = 1
    entries.append(calc_entry)
    print (entries)
    # Process calculation with input extent and resolution
    calc = QgsRasterCalculator( dem+"@1",
                            "S:\\DATA\\DEMS\\{}.tif".format(dem),
                            "GTiff",
                            rlayer.extent(),
                            3601,
                            3601,
                            entries)

    calc.processCalculation()

###
import processing

input_raster = QgsRasterLayer('path/to/your/input/raster', 'raster')
output_raster = 'path/to/your/output/raster'

#I find it nice to create parameters as a dictionary
parameters = {'INPUT_A' : input_raster,
        'BAND_A' : 1,
        'FORMULA' : '(A > 100)',   #your expression here. Mine finds all cells with value > 100. Experiment in the GUI if needed. You can copy and paste exactly the same expression to into your code here
        'OUTPUT' : output_raster}

processing.runAndLoadResults('gdal:rastercalculator', parameters)
###
