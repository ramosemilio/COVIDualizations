#NUKE_UV_BATCHER
#By Emilio Ramos
import sys
import os

#SCRIPT TO GRADE AND RESIZE GEOTIFFS GENERATED BY DEM_TO_GEOTIFF.py
nuke.root()['format'].setValue( 'square_2K' )

read_node = nuke.createNode("Read")
grade_node = nuke.createNode("Grade")
reformat_node = nuke.createNode("Reformat")
transform_node = nuke.createNode("Transform")
bg_plate = nuke.createNode("Constant")
merge_node = nuke.createNode("Merge")
write_node = nuke.createNode("Write")

grade_node.setInput(0,read_node)
grade_node.knob("whitepoint").setValue(2000)

reformat_node.setInput(1,grade_node)
reformat_node.knob("type").setValue(1)
reformat_node.knob("box_width").setValue(2040)
reformat_node.knob("box_width").setValue(2040)

transform_node.setInput(1, reformat_node)
transform_node.knob("translate").setValue((4,4))
transform_node.knob("black_outside").setValue(False)

merge_node.setInput(1, transform_node)
merge_node.setInput(0, bg_plate)

write_node.setInput(1, merge_node)
write_node.knob("file").setValue("")
write_node.knob("colorspace").setValue("linear")
write_node.knob("file_type").setValue("tiff")
write_node.knob("datatype").setValue(1)

source_folder = "S:/DATA/DEMS/"
dest_folder = "C:/Users/ramos/Documents/SVA/GRAD SCHOOL PORTFOLIO/07_COVID_VIZ/DEM_FOR_UV/"

tiff_folder = os.listdir(source_folder)

for geotiff in tiff_folder:
    name_split = geotiff.split(".")
    if name_split[-1] == "tif":

        read_path = source_folder+geotiff
        read_node.knob("file").setValue(read_path)
        write_node.knob("file").setValue(dest_folder+"UV_"+name_split[0]+".tif")
        nuke.execute ("Write1",1,1,1)
