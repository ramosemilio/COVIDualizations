#COVID_VIZ v0.1
#By Emilio Ramos
import maya.cmds as cmds

#POINT TO JHU .CSV WITH COVIV DATA
#MAKE FILE BROWSER
file_path = (r"C:\Users\ramos\Documents\SVA\GRAD SCHOOL PORTFOLIO\07_COVID_VIZ\PYTHON\data.csv")

#FUNCTION TO READ .CSV FILE AND RETURN ROWS OF DATA
def read_data(path):
  data_file = open(path,"r")
  data_all = data_file.read().splitlines()
  return data_all

#CREATE GLOBAL data_lines variable
data_lines = read_data(file_path)

#FUNCTION TO READ .CSV COLUMN HEADERS TO MAKE SURE DATA SCTRUCTURE HASN'T CHANGED
def get_headers():
    return data_lines[0]

def get_start_date():
    return data_lines[12]

get_start_date()


#FUNCTION TO GET STATE-LEVEL DATA
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

#FUNCTION TO GET COUNTRY-LEVEL DATA
def get_country_data(country_name):
    country_data = []

    #ITERATE OVER .CSV DATA
    for line in data_lines:
        #SPLIT ROW INTO LIST AFTER REPLACING COMMAS IN FULL PLACE NAMES
        line = line.replace(", ", "-")
        split_line = line.split(",")
        #print (split_line)
        #IF LIST == state_name ADD TO state_data
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
            NAME = split_line[10].strip('"')
            POP = float(split_line[11])
            CASES = split_line[13:]

            #CREATE AND ADD NEW ENTRY
            new_entry = [FIPS,LAT,LON,NAME,POP,CASES]
            country_data.append(new_entry)

    return country_data

#TABLE SCTRUCTURE
#UID,iso2,iso3,code3,FIPS,Admin2,Province_State,Country_Region,Lat,Long_,Combined_Key,Population,[DATES]
#INDEX 8(lat), 9(long), 12+

def make_cubes(place_string, animation, height_scale):
    #places=get_state_data(place_string)
    places=get_country_data(place_string)
    for location in places:
        #NEED GROUPING FUNCTION
        new_plane = cmds.polyPlane(n= location[3], height=0.01, width =0.01, axis=[0,0,1], sh= 1, sw=1, ch=False)
        #print (new_plane)
        cmds.polyMoveVertex(new_plane[0]+".vtx[0:3]", tz=57.2965, ch=False)
        cmds.setAttr(new_plane[0]+".rx",-1*float(location[1]))
        cmds.setAttr(new_plane[0]+".ry", float(location[2]))
        cmds.polyExtrudeFacet(new_plane[0]+".f[0]", kft=True, ltz=float(location[-1][-1])*height_scale)
        connections = cmds.listConnections(new_plane[0]+"Shape")
        extrude_node = connections[1]

        #print (location[3])

        #GET DAILY CASE DATA FROM LIST
        case_numbers = location[5]
        timer = 0

        if animation:
            #ITERATE OVER DAILY NUMBERS AND SET EXTRUSION KEYFRAMES
            for number in case_numbers:
                #CHECK TO SEE IF NEW KEYFRAME NEEDED
                index = timer
                if index == 0:
                    cmds.setKeyframe(extrude_node+".ltz", time = 0, value = (float(case_numbers[(timer)])*height_scale))
                    timer = timer+1
                else:
                    if case_numbers[index]==case_numbers[index-1]:
                        #NO KEYFRAME NEEDED
                        timer = timer+1
                    else:
                        cmds.setKeyframe(extrude_node+".ltz", time = (timer+1)*6, value = (float(case_numbers[(timer)])*height_scale))
                        timer = timer+1



make_cubes("USA", False, 0.000015)
#get_state_data("Virginia")
