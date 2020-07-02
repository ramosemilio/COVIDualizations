import maya.cmds as cmds

#SCRIPT TO CREATE A SPHERE MODEL OF THE EARTH
earth_sphere = cmds.polySphere(
    name="EARTH_SPHERE",
    createUVs = 0,
    subdivisionsAxis= 360,
    subdivisionsHeight=180,
    constructionHistory=False,
    r=57.2965067401)

#HELPER FUNCTION TO CONVERT LAT LON DATA TO STRING FOR MAPPING
def latlon_to_string(lat,latdeg,lon,londeg):
    new_string = lat+str(latdeg).zfill(2)+lon+str(londeg).zfill(3)
    return new_string

def face_to_latlon(sphere_geo):

    #CREATE DICTIONARY TO HOLD MAPPING
    face_mapping = {}
    #HARD CODE # OF FACES BC IT WILL NEVER CHANGE (180*360)
    num_face = 64800
    face_index = 0
    LAT_DIR = "S"
    LAT_DEG = 90
    LON_DIR = "E"
    LON_DEG = 91

    #ITERATE OVER FACES EXCLUDING POLAR REGIONS (LAST 720 FACES)
    while face_index < (num_face-720):

        degree_offset = face_index%360

        if (degree_offset)==0:
            LON_DIR = "E"

            if LAT_DIR == "N":
                LAT_DEG = LAT_DEG+1
            if LAT_DIR == "S":
                LAT_DEG = LAT_DEG-1
                if LAT_DEG < 1:
                    LAT_DIR = "N"

        if (degree_offset>0 and degree_offset<89):
            LON_DIR = "E"
            LON_DEG = LON_DEG+degree_offset
        if (degree_offset>=89 and degree_offset<269):
            LON_DIR = "W"
            LON_DEG = 180+(89-degree_offset)
        if (degree_offset>=269 and degree_offset<360):
            LON_DIR ="E"
            LON_DEG = 0+(degree_offset-269)

        new_key = latlon_to_string(LAT_DIR,LAT_DEG,LON_DIR,LON_DEG)
        face_mapping[new_key] = face_index

        face_index = face_index+1

    return face_mapping

map = face_to_latlon("EARTH_SPHERE")

#SELCT FACE AT THE EQUATOR AND PRIME MERIDIAN
cmds.select("EARTH_SPHERE.f[{}]".format(str(map["N00E000"])))
