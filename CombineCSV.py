import csv
import os
import glob
import pandas as pd
import numpy as np
print("\CSV Combine and Remove Duplicate Headers, Written by W. Mears.\n")
directory = input(r"Enter the directory name (Relative or full pathnames accepted. Ex: C:\Users\yourname\path): ")
os.chdir(directory)
name = input("What would you like to name your combined file? Ex. name.csv : ")
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
combinedInfo = pd.read_csv(all_filenames[1])
for i in range(2, len(all_filenames)):
    csvInfo = pd.read_csv(all_filenames[i])
    conc = [combinedInfo, csvInfo]
    combinedInfo = pd.concat(conc)
combinedInfo.to_csv( name, index=False, encoding='utf-8-sig')
print("Combined file successfuly saved to input directory")