#DEM_QGIS_PROCESSOR v0.1
#By Emilio Ramos

#HELPER SCRIPT TO DETERMINE MIN AND MAX HEIGH VALUES OF GEOTIFF SET
#THESE VALUES WILL BE USED TO GRADE IN NUKE_UV_BATCHER.py

# get the path to a tif file  e.g. /home/project/data/srtm.tif
for dem in selected_tiles:
    path_to_hgt = "S:\\DATA\\DEMS\\{}.hgt".format(dem)

    tile_coord = dem

    rlayer = QgsRasterLayer(path_to_hgt, tile_coord)
    if not rlayer.isValid():
        print("Layer failed to load!")

    #ADD TO PROJECT
    QgsProject.instance().addMapLayer(rlayer)

    renderer= rlayer.renderer()

    #STORE MIN AND MAX FROM DEFAULT STATE
    min = renderer.contrastEnhancement().minimumValue()
    max = renderer.contrastEnhancement().maximumValue()
    print (min)
    print (max)

    #REMOVE COLOR ENCHANCEMENT
    rlayer.setContrastEnhancement(QgsContrastEnhancement.NoEnhancement)

    with open("S:\\DATA\\GEOTIFFS\\DEM_HEIGHT_RANGES.txt","a") as fd:
        fd.write(str(tile_coord)+"_"+str(min)+"_"+str(max)+"\n")

    QgsProject.instance().removeMapLayer(rlayer.id())


def get_max_min():

    data_file = open("S:\\DATA\\GEOTIFS\\DEM_HEIGHT_RANGES.txt","r")
    data_all = data_file.read()
    data_lines = data_all.splitlines()

    max=0.0
    min=0.0

    for line in data_lines:
        split = line.split("_")
        #print (split)
        if float(split[1]) < min:
            min = float(split[1])
        if float(split[2]) > max:
            print
            max = float(split[2])

    print(min) #-115.0
    print(max) #22768.0

get_max_min()
