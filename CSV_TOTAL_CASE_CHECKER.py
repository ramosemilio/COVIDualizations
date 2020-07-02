#COVID CSV CHECKER v0.11
#By Emilio Ramos
from tkinter import filedialog
import tkinter


root = tkinter.Tk()
root.filename =  filedialog.askopenfilename(initialdir = "/",
    title = "Select file",
    filetypes = (("csv files","*.csv"),("all files","*.*")))
print (root.filename)


#POINT TO JHU .CSV WITH COVIV DATA
file_path = root.filename

#POINT TO JHU .CSV WITH COVIV DATA
file_path = root.filename

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
    return (data_lines[0], len(data_lines[0].split(",")))


#FUNCTION TO GET COUNTRY-LEVEL DATA
def check_lines():
    #ITERATE OVER .CSV DATA
    for line in data_lines:
        #SPLIT ROW INTO LIST AFTER REPLACING COMMAS IN FULL PLACE NAMES
        line = line.replace(", ", "|")
        split_line = line.split(",")
        #IF LIST == country_name ADD TO country_data
        if len(split_line) > get_header_info()[1]:
            print (line)

def get_deaths():
    deaths_num = 0
    death_lines = data_lines
    del death_lines[0]

    for line in death_lines:
        split = line.split(",")
        deaths_num = deaths_num + int(split[-1])

    return deaths_num
check_lines()
print ("Entries= "+ str(get_header_info()[1]))
print ("Total Cases: "+str(get_deaths()))
