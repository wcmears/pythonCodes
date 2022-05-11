from astropy.io import fits
import os
from astropy.utils.data import get_pkg_data_filename
import csv
import pandas as pd
print("\nFITS Header Editor, Version 1.0. Written by W. Mears.\n")
q = 0
while q == 0:
    directory = input("Enter the directory name (Relative or full pathnames accepted. Ex: .\subdir_name): ")
    os.chdir(directory)
    keyWord = input("Enter key word that you would like to search for in the FITS header in the form: keyWord : ")
    z = 0
    y = 0
    while z != 'disp' and z != 'edit':
        z = input("Would you like to display the value of the FITS keyword for each file or edit the value? (Enter disp or edit) : ")
        if z != 'disp' and z != 'edit':
            print("Please enter either disp or edit!")
    if z == 'edit':
        newVal = input("Input what you would like to change the value of your inputed key word to in the following format: newValue : ")
    while y != 'write' and y != 'disp':
        y = input("Would you like to write result to a CSV file or only display result on screen? (Enter write or disp) : ") 
        if y != 'disp' and y != 'write':
            print("Please enter either write or disp!")
    if y == 'write':
        name = input("What would you like to name your CSV file? Input in format: input.csv : ")
        csvDf = pd.DataFrame({'File Name' : [], 'Object': []})
    for filename in os.listdir(directory):
            if filename.endswith(".fts") or filename.endswith(".fits") or filename.endswith(".fit"):
                fits_file = get_pkg_data_filename(filename)
                if z == 'disp':
                    print(filename + " : ")
                    print(fits.getval(fits_file, keyWord))
                else:
                    fits.setval(fits_file, keyWord,value=newVal)
                if y == 'write':
                    frame = pd.DataFrame({'File Name': [str(filename)], 'Object': [str(fits.getval(fits_file, keyWord))]})
                    csvDf = [csvDf, frame]
                    csvDf = pd.concat(csvDf)
                elif z == 'disp':
                    continue
                else:
                    print(filename + " : ")
                    print(fits.getval(fits_file, keyWord))
    if y == 'write':
        csvDf.to_csv(os.path.join(directory, name))
        print("Values successfuly saved in CSV file to the input directory")
    cont = input("Would you like to parse through another directory? (y/n) : ")
    if cont == 'y':
        continue
    else:
        q = 1
            
                