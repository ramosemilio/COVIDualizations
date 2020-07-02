#COVID_VIZ v0.1
#By Emilio Ramos
import maya.cmds as cmds
import maya.mel as mel
#POINT TO JHU .CSV WITH COVIV DATA
file_path = (r"C:\Users\ramos\Documents\SVA\GRAD SCHOOL PORTFOLIO\07_COVID_VIZ\PYTHON\CSV DATA\data_051220.csv")

#FUNCTION TO READ .CSV FILE AND RETURN ROWS OF DATA
def read_data(path):
  data_file = open(path,"r")
  data_all = data_file.read().splitlines()
  return data_all

#CREATE GLOBAL data_lines variable
data_lines = read_data(file_path)

#FUNCTION TO READ .CSV COLUMN HEADERS TO MAKE SURE DATA SCTRUCTURE HASN'T CHANGED
#SECOND TUPLE VALUE IS USED TO COMPARE TO MAKE SURE ALL LINES ARE SAME LENGTH
#AFTER PARSING AND DATA PROCESSING
def get_header_info():
    return (data_lines[0], len(data_lines[0]))


#FUNCTION TO GET COUNTRY-LEVEL DATA
def get_country_data(country_name):
    country_data = []

    #ITERATE OVER .CSV DATA
    for line in data_lines:
        #SPLIT ROW INTO LIST AFTER REPLACING COMMAS IN FULL PLACE NAMES
        line = line.replace(", ", "|")
        split_line = line.split(",")
        #IF LIST == country_name ADD TO country_data
        if split_line[2]==country_name:
            UID = float(split_line[0])
            ISO2 = split_line[1]
            ISO3 = split_line[2]
            CODE3 = int(split_line[3])
            FIPS = split_line[4]
            ADMIN2 = split_line[5]
            PROV_STATE = split_line[6]
            COUNTRY = split_line[7]
            LAT = float(split_line[8])
            LON = float(split_line[9])

            #REMOVE "US" FROM PLACE NAME
            RAW_NAME = split_line[10].strip('"').split("|")
            NAME = RAW_NAME[0]+", "+ RAW_NAME[1]

            POP = float(split_line[11])
            CASES = split_line[12:]

            #CREATE AND ADD NEW ENTRY
            new_entry = [NAME,LAT,LON,FIPS,POP,CASES]
            country_data.append(new_entry)

    return country_data

#FUNCTION TO GET STATE-LEVEL DATA USED FOR TESTING BEFORE GETTING ALL OF USA
#COMBINE BASED ON HEADER CHECKS
def get_state_data(state_name):
    state_data = []

    #ITERATE OVER .CSV DATA
    for line in data_lines:
        #SPLIT ROW INTO LIST AFTER REPLACING COMMAS IN FULL PLACE NAMES
        line = line.replace(", ", "-")
        split_line = line.split(",")

        #IF LIST == state_name ADD TO state_data
        if split_line[6]==state_name:
            UID = float(split_line[0])
            ISO2 = split_line[1]
            ISO3 = split_line[2]
            CODE3 = int(split_line[3])
            FIPS = split_line[4]
            ADMIN2 = split_line[5]
            PROV_STATE = split_line[6]
            COUNTRY = split_line[7]
            LAT = float(split_line[8])
            LON = float(split_line[9])
            NAME = split_line[10].strip('"')
            POP = float(split_line[11])
            CASES = split_line[13:]

            #CREATE AND ADD NEW ENTRY
            new_entry = [FIPS,LAT,LON,NAME,POP,CASES]
            state_data.append(new_entry)

    return state_data

earth_scale = 57.2965067401

#FUNCTION TO BE RUN IN MAYA THAT ITERATES OVER DATA AND CREATES AN ANIMATED
#BAR FOR EACH ROW FROM .CSV
def make_cubes(place_string, animation, height_scale, time_scale):
    #RUN ON STATE OR COUNTRY
    #places=get_state_data(place_string)
    places=get_country_data(place_string)

    #CREATE NEW PLANE NAMED AFTER LOCATION
    for location in places:
        #NEED GROUPING FUNCTION
        new_cube = cmds.polyCube(
            n= location[0]+"-BAR",
            height = .25,
            width = .25,
            depth = .25,
            axis=[0,0,1],
            ch=False)

        #ADD ATTRIBUTE DEATHS TO DRIVE ANIMATION AND COLOR
        cmds.addAttr(shortName='d', longName='deaths', defaultValue=0.0, minValue=0.0, maxValue=1000000 )
        cmds.setAttr(new_cube[0]+".deaths", float(location[-1][-1]))
        cmds.polySmooth(new_cube[0], dv =2, ch=False)

        #MOVE PLANE TO EDGE OF EARTH (57.2965067401 MAYA UNITS)
        cmds.polyMoveVertex(new_cube[0]+".vtx[0:97]", tz=earth_scale, ch=False)



        #ROTATE TO LAT LON POSITION
        #cmds.rotate(-1*float(location[1]), float(location[2]), 0, new_cube[0], objectSpace=True)
        #cmds.expression( string = new_cube[0]+".rx ="+str(-1*float(location[1])))
        #cmds.expression( string = new_cube[0]+".ry ="+str(float(location[1])))

        cmds.setAttr(new_cube[0]+".rx",-1*float(location[1]))
        cmds.setAttr(new_cube[0]+".ry", float(location[2]))
        cmds.xform(new_cube[0], cp=1, a=1)

        #2*(((3V)/(4.0*3.1415926))**(1.0/3.0))
        #death_scalar = 1.611661654
        death_scalar = 2
        cmds.expression( string = new_cube[0]+".sx = "+str(death_scalar)+" * pow(((.75)*"+new_cube[0]+".deaths/3.141592654),(1.0/3.0))")
        cmds.expression( string = new_cube[0]+".sy = "+str(death_scalar)+" * pow(((.75)*"+new_cube[0]+".deaths/3.141592654),(1.0/3.0))")
        cmds.expression( string = new_cube[0]+".sz = "+str(death_scalar)+" * pow(((.75)*"+new_cube[0]+".deaths/3.141592654),(1.0/3.0))")

        #GROUP GEOMETRY BASED ON STATE
        #CHECK TO SEE IF STATE GROUP ALREADY EXISTS
        bar_location = location[0].split(", ")[1].replace(" ", "_")
        if cmds.ls(str(bar_location)):
            cmds.parent(new_cube, bar_location)
        else:

            cmds.group(new_cube, name = bar_location)

        #GET DAILY CASE DATA FROM LIST
        case_numbers = location[5]
        timer = 0

        #TO RUN IF ANIMATION ARG SET IN FUNCTION CALL
        if animation:
            #ITERATE OVER DAILY NUMBERS AND SET EXTRUSION KEYFRAMES
            for number in case_numbers:
                #CHECK TO SEE IF NEW KEYFRAME NEEDED
                index = timer
                #BASE CASE
                if index == 0:
                    cmds.setKeyframe(new_cube[0]+".deaths", time = 0, value = (float(case_numbers[(timer)])))
                    timer = timer+1
                else:
                    cmds.setKeyframe(new_cube[0]+".deaths", time = (timer)*time_scale, value = (float(case_numbers[(timer)])))
                    timer = timer+1

#VARIABLE USED TO DETEMINE HOW MANY MAYA FRAMES ARE A DAY OF DATA
global_time_scale = 3

make_cubes("USA", True, 0.00, global_time_scale)
