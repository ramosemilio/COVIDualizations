#COVID_VIZ v0.1
#By Emilio Ramos
import maya.cmds as cmds
import maya.mel as mel



#POINT TO JHU .CSV WITH COVIV DATA
file_path = (r"C:\Users\ramos\Documents\SVA\0_GRAD SCHOOL PORTFOLIO\07_COVID_VIZ\PYTHON\CSV DATA\time_series_covid19_confirmed_US_063020.csv")

file_path_2 = (r"C:\Users\ramos\Documents\SVA\0_GRAD SCHOOL PORTFOLIO\07_COVID_VIZ\PYTHON\CSV DATA\data_051220.csv")

#FUNCTION TO READ .CSV FILE AND RETURN ROWS OF DATA
def read_data(path):
  data_file = open(path,"r")
  data_all = data_file.read().splitlines()
  return data_all

#CREATE GLOBAL data_lines variable
data_lines = read_data(file_path)
pop_lines = read_data(file_path_2)


#FUNCTION TO READ .CSV COLUMN HEADERS TO MAKE SURE DATA SCTRUCTURE HASN'T CHANGED
#SECOND TUPLE VALUE IS USED TO COMPARE TO MAKE SURE ALL LINES ARE SAME LENGTH
#AFTER PARSING AND DATA PROCESSING
def get_header_info():
    return (data_lines[0], len(data_lines[0]))


def get_pop_data(country_name):
    pop_data = {}

    #ITERATE OVER .CSV DATA
    for line in pop_lines:
        #SPLIT ROW INTO LIST AFTER REPLACING COMMAS IN FULL PLACE NAMES
        line = line.replace(", ", "|")
        split_line = line.split(",")
        #IF LIST == country_name ADD TO country_data
        if split_line[2]==country_name:
            UID = float(split_line[0])
            POP = float(split_line[11])
            pop_data[UID] = POP

    return pop_data

POP_DATA = get_pop_data("USA")

#FUNCTION TO GET COUNTRY-LEVEL DATA
def get_country_data(country_name):
    country_data = []
    counter = 0
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

            POP = POP_DATA[UID]
            CASES = split_line[11:]

            #CREATE AND ADD NEW ENTRY
            new_entry = [NAME,LAT,LON,FIPS,POP,CASES]
            country_data.append(new_entry)
        counter = counter + 1

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

        shape_node = cmds.listRelatives( new_cube[0], children=True )
        #ADD ATTRIBUTE CASES AND POP TO DRIVE ANIMATION AND COLOR
        cmds.addAttr(shape_node[0], shortName='cases', longName='mtoa_constant_cases', defaultValue=0.0, minValue=0.0, maxValue=1000000 )
        cmds.addAttr(shape_node[0], shortName='pop', longName='mtoa_constant_population', defaultValue=0, minValue=0, maxValue=20000000 )
        cmds.addAttr(shape_node[0], shortName='day', longName='mtoa_constant_daily', defaultValue=0.0, minValue=0.0, maxValue=1000000 )
        cmds.addAttr(shape_node[0], shortName='avg', longName='mtoa_constant_average', defaultValue=0.0, minValue=0.0, maxValue=1000000 )

        cmds.setAttr(shape_node[0]+".cases", float(location[-1][-1]))
        cmds.setAttr(shape_node[0]+".pop", float(location[-2]))

        #MOVE PLANE TO EDGE OF EARTH (57.2965067401 MAYA UNITS)
        cmds.polyMoveVertex(new_cube[0]+".vtx[0:7]", tz=earth_scale, ch=False)



        #ROTATE TO LAT LON POSITION
        #cmds.rotate(-1*float(location[1]), float(location[2]), 0, new_cube[0], objectSpace=True)
        #cmds.expression( string = new_cube[0]+".rx ="+str(-1*float(location[1])))
        #cmds.expression( string = new_cube[0]+".ry ="+str(float(location[1])))

        cmds.setAttr(new_cube[0]+".rx",-1*float(location[1]))
        cmds.setAttr(new_cube[0]+".ry", float(location[2]))
        cmds.xform(new_cube[0], cp=1, a=1)

        #2*(((3V)/(4.0*3.1415926))**(1.0/3.0))
        #death_scalar = 1.611661654
        case_scalar = 0.25
        cmds.expression( string = new_cube[0]+".sx = "+str(case_scalar)+" * pow(("+shape_node[0]+".cases),(1.0/3.0))")
        cmds.expression( string = new_cube[0]+".sy = "+str(case_scalar)+" * pow(("+shape_node[0]+".cases),(1.0/3.0))")
        cmds.expression( string = new_cube[0]+".sz = "+str(case_scalar)+" * pow(("+shape_node[0]+".cases),(1.0/3.0))")

        #GROUP GEOMETRY BASED ON STATE
        #CHECK TO SEE IF STATE GROUP ALREADY EXISTS
        bar_location = location[0].split(", ")[1].replace(" ", "")
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
                    cmds.setKeyframe(shape_node[0]+".day", time = 0, value = 0)
                    cmds.setKeyframe(shape_node[0]+".avg", time = 0, value = 0)
                    cmds.setKeyframe(shape_node[0]+".cases", time = 0, value = (float(case_numbers[(timer)])))
                    timer = timer+1
                else:
                    average_cases = 0

                    today = (float(case_numbers[(timer)]))-(float(case_numbers[(timer)-1]))

                    if (timer-2)< 0:
                        day_1 = 0
                    else:
                        day_1 = (float(case_numbers[(timer-1)]))-(float(case_numbers[(timer)-2]))

                    if (timer-3)< 0:
                        day_2 = 0
                    else:
                        day_2 = (float(case_numbers[(timer-2)]))-(float(case_numbers[(timer)-3]))

                    if (timer-4)< 0:
                        day_3 = 0
                    else:
                        day_3 = (float(case_numbers[(timer-3)]))-(float(case_numbers[(timer)-4]))

                    if (timer-5)< 0:
                        day_4 = 0
                    else:
                        day_5 = (float(case_numbers[(timer-4)]))-(float(case_numbers[(timer)-5]))

                    if (timer-6)< 0:
                        day_5 = 0
                    else:
                        day_5 = (float(case_numbers[(timer-5)]))-(float(case_numbers[(timer)-6]))

                    if (timer-7)< 0:
                        day_6 = 0
                    else:
                        day_6 = (float(case_numbers[(timer-6)]))-(float(case_numbers[(timer)-7]))


                    average_cases = (today + day_1 + day_2 + day_3 + day_4 + day_5 + day_6)/7

                    cmds.setKeyframe(shape_node[0]+".day", time = (timer)*time_scale, value = today)
                    cmds.setKeyframe(shape_node[0]+".avg", time = (timer)*time_scale, value = average_cases)
                    cmds.setKeyframe(shape_node[0]+".cases", time = (timer)*time_scale, value = (float(case_numbers[(timer)])))
                    timer = timer+1

#VARIABLE USED TO DETEMINE HOW MANY MAYA FRAMES ARE A DAY OF DATA
global_time_scale = 3

make_cubes("USA", True, 0.00, global_time_scale)
