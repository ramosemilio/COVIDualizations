#DEM WRANGLER v0.1
#BY Emilio Ramos
import json
import sys
import os
import requests

#SCRIPT TO DOWNLOAD DIGITAL ELEVATION MODEL FILES FROM THE USGS USING REQUESTS

#READ IN JSON DATA DOWNLADED FROM USGS
file_path = (r"C:\Users\ramos\Documents\SVA\GRAD SCHOOL PORTFOLIO\07_COVID_VIZ\PYTHON\srtm30m_bounding_boxes.json")

def read_json(path):
  data_file = open(path,"r")
  data_all = data_file.read()
  return data_all

#STORE JSON DATA FOR PROCESSING
py_json = json.loads(read_json(file_path))

DEM_features = py_json["features"]

raw_file_list= []

#ITERATE OVER JSON TO GET EVERY DEM FILE NAME
for feature in DEM_features:
    file_name = feature["properties"]["dataFile"]
    #print (file_name)
    raw_file_list.append(file_name)


#########################################
#USA'S BOUDNING_BOX = N60-N05 , W142-W053
#########################################

#ITERATE OVER FILE NAMES AND SORT FOR EASE OF PROCESSING
sorted_tiles =[]
for file in raw_file_list:

    file_strip = file.split(".")
    sorted_tiles.append(file_strip[0])
    sorted_tiles.sort()

#ITERATE OVER SORTED TILES AND COMPARE TO BOUNDS
selected_tiles = []
for sort in sorted_tiles:
    if sort[0]=="S":
        continue

    if sort[3]=="E":
        continue

    if sort[0]=="N":
        lat_degree = int(sort[1:3:1])
        lon_degree = int(sort[4:7:1])
        #CHECK TO SEE IF TILE IS PART OF USA
        if (lat_degree < 60) & (lat_degree > 5):
            if (lon_degree < 142) & (lon_degree > 53):

                #APPEND FILE NAME IF NORTH AMERICAN
                selected_tiles.append(sort+".SRTMGL1.hgt.zip")
                #selected_tiles.append(sort+".SRTMGL1.2.jpg")

#USE REQUESTS MODULE TO QUERY WITH CREDENTIALS TO DOWNLOAD SELECTED TILES
def download_hgt_files(file_names):
    #os.mkdir(".\\DEM_FILES")
    for file in file_names:
        file_url = r"https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/2000.02.11/"+file
        print (file_url)

        s = requests.session()
        url_login = file_url

        payload = {
            "username": "eramos10",
            "password": "REDACTED"}

        r = requests.get(file_url, auth=('eramos10', r'REDACTED'), allow_redirects=False)
        redirect = r.headers["Location"]
        print(redirect)
        r2 = requests.get(redirect, auth=('eramos10', r'REDACTED'), allow_redirects=True)
        print(r2.status_code)

        r2.raise_for_status()

        #SAVE FILE TO DRIVE
        with open("C:\\Users\\ramos\\Documents\\SVA\\GRAD SCHOOL PORTFOLIO\\07_COVID_VIZ\\DEMS\\"+file, 'wb') as fd:
            fd.write(r2.content)

#DOWNLOAD SELECTED TILES CALL
download_hgt_files(selected_tiles)

#SIMILAR FUNCTION FOR JPG PROXIES
def download_jpg_files(file_names):
    #os.mkdir(".\\DEM_FILES")
    for file in file_names:
        file_url = r"https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/2000.02.11/"+file
        print (file_url)

        s = requests.session()
        url_login = file_url

        payload = {
            "username": "eramos10",
            "password": "REDACTED"}

        r = requests.get(file_url, auth=('eramos10', r'REDACTED'), allow_redirects=False)
        #redirect = r.headers["Location"]
        #print(redirect)
        #r2 = requests.get(redirect, auth=('eramos10', r'FUN!&)fun170'), allow_redirects=True)
        #print(r2.status_code)

        r.raise_for_status()

        with open(".\\DEMS\\"+file, 'wb') as fd:
            fd.write(r.content)


#download_jpg_files(selected_tiles)
