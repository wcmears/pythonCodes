import numpy as np
from astropy.io import fits
import csv
import os
print("\nFITS Image Info, Version 1.0. Written by W. Mears.\n")
#parameter file with previous enteries
y = 0
s = 0
n = -1
m = -1
q = 0
while q == 0:
    directory = input("Enter the directory name (Relative or full pathnames accepted. Ex: .\subdir_name): ")
    while s != 'sub' and s != 'full' and s != 'both': #convert to desired case
        s = input("Would you like to see statistics for a subframe extending from (150, 150), a full frame, or both? (Enter sub, full, or both) : ")
        if s != 'sub' and s != 'full' and s != 'both':
            print("Please enter either sub, full, or both!")
    if s == 'sub' or s == 'both':
        while n < 0 or n > 1898:
            n = input("Enter vertical dimension for subframe : ") #Ask user if they want to enter their own dimensions or use the default
            n = int(n)
            if n > 1898 or n < 0:
                print("Please enter a vertical dimension between 0 and 1898!")
        while m < 0 or m > 1898:
            m = input("Enter horizontal dimension for subframe : ")
            m = int(m)
            if m > 1898 or m < 0:
                print("Please enter a horizontal dimension between 0 and 1898!")
    while y != 'write' and y != 'disp' and y != 'both':
        y = input("Would you like to write result to a CSV file, only display result on screen, or both? (Enter write or disp or both) : ") 
        if y != 'disp' and y != 'write' and y != 'both':
            print("Please enter either write, disp, or both!")
    if y == 'both':
        z = input("Name your csv file in the following format: fileName.csv : ")
        os.chdir(directory);
        with open(z, 'w') as f:
            thewriter = csv.writer(f)
            if s == 'full' or s == 'both':
                print("Filename ------------------------------------------------------- ", "Average in ADUs/pix ------ ", "STD       \n", "Full Frame")
                thewriter.writerow(['File Name', 'Average', 'STD', 'Median', 'Full Frame'])
                for filename in os.listdir(directory):
                    if filename.endswith(".fts") or filename.endswith(".fits") or filename.endswith(".fit"):
                        x = fits.open(os.path.join(directory, filename));
                        x = x[0].data
                        x = np.matrix(x)
                        print(os.path.join(directory, filename), "        ", round(np.matrix.mean(x), 1), end=" ")
                        print("      ", round(np.matrix.std(x), 1), "   ", round(np.median(np.squeeze(np.asarray(x))), 1))
                        thewriter.writerow([os.path.join(directory, filename), round(np.matrix.mean(x), 1), round(np.matrix.std(x), 1), round(np.median(np.squeeze(np.asarray(x))), 1)])
                    else:
                        continue;
            if s == 'sub' or s == 'both':
                print("Filename ------------------------------------------------------- ", "Average in ADUs/pix ------ ", "STD       \n", "Subframe")
                thewriter.writerow(['File Name', 'Average', 'STD', 'Median', str(n) + 'x' + str(m) + ' Subframe  starting from (150,150)'])
                for filename in os.listdir(directory):
                    n = int(n)
                    m = int(m)
                    if filename.endswith(".fts") or filename.endswith(".fits") or filename.endswith(".fit"):
                        x = fits.open(os.path.join(directory, filename));
                        x = x[0].data
                        x = np.matrix(x)
                        x = x[150:150+n,150:150+m]
                        print(os.path.join(directory, filename), "        ", round(np.matrix.mean(x),1), end=" ")
                        print("      ", round(np.matrix.std(x), 1), "   ", round(np.median(np.squeeze(np.asarray(x))), 1))
                        thewriter.writerow([os.path.join(directory, filename), round(np.matrix.mean(x),1), round(np.matrix.std(x),1), round(np.median(np.squeeze(np.asarray(x))),1)])
                    else:
                        continue;        
    elif y == 'write':
        z = input("Name your csv file in the following format: fileName.csv : ")
        os.chdir(directory);
        with open(z, 'w') as f:
            thewriter = csv.writer(f)
            if s == 'full' or s == 'both':
                thewriter.writerow(['File Name', 'Average', 'STD', 'Median', 'Full'])
                for filename in os.listdir(directory):
                    if filename.endswith(".fts") or filename.endswith(".fits") or filename.endswith(".fit"):
                        x = fits.open(os.path.join(directory, filename));
                        x = x[0].data
                        x = np.matrix(x)
                        thewriter.writerow([os.path.join(directory, filename), round(np.matrix.mean(x),1), round(np.matrix.std(x),1), round(np.median(np.squeeze(np.asarray(x))),1)])
                    else:
                        continue;
            if s == 'sub' or s == 'both':
                thewriter.writerow(['File Name', 'Average', 'STD', 'Median', str(n) + 'x' + str(m) + ' Subframe starting from (150,150)'])
                for filename in os.listdir(directory):
                    n = int(n)
                    m = int(m)
                    if filename.endswith(".fts") or filename.endswith(".fits") or filename.endswith(".fit"):
                        x = fits.open(os.path.join(directory, filename));
                        x = x[0].data
                        x = np.matrix(x)
                        x = x[150:150+n,150:150+m]
                        thewriter.writerow([os.path.join(directory, filename), round(np.matrix.mean(x),1), round(np.matrix.std(x),1), round(np.median(np.squeeze(np.asarray(x))),1)])
                    else:
                        continue; 
    else:
        if s == 'full' or s == 'both':
            print("Filename ------------------------------------------------------- ", "Average in ADUs/pix ------ ", "STD       \n", "Full Frame")
            for filename in os.listdir(directory):
                if filename.endswith(".fts") or filename.endswith(".fits") or filename.endswith(".fit"):
                    x = fits.open(os.path.join(directory, filename));
                    x = x[0].data
                    x = np.matrix(x)
                    print(os.path.join(directory, filename), "        ", round(np.matrix.mean(x),1), end=" ")
                    print("      ", round(np.matrix.std(x), 1), "   ", round(np.median(np.squeeze(np.asarray(x))), 1))
                else:
                    continue;
        if s == 'sub' or s == 'both':
            print("Filename ------------------------------------------------------- ", "Average in ADUs/pix ------ ", "STD       \n", "Subframe")
            for filename in os.listdir(directory):
                    n = int(n)
                    m = int(m)
                    if filename.endswith(".fts") or filename.endswith(".fits") or filename.endswith(".fit"):
                        x = fits.open(os.path.join(directory, filename));
                        x = x[0].data
                        x = np.matrix(x)
                        x = x[150:150+n,150:150+m]
                        print(os.path.join(directory, filename), "        ", round(np.matrix.mean(x),1), end=" ")
                        print("      ", round(np.matrix.std(x), 1), "   ", round(np.median(np.squeeze(np.asarray(x))), 1))
                    else:
                        continue;
    cont = input("Would you like to parse through another directory? (y/n) : ")
    if cont == 'y':
        sett = input('Would you like to keep the same settings or enter new ones? (same/new) : ')
        if sett == 'same':
            continue
        if sett == 'new':
            y = 0
            s = 0
            n = -1
            m = -1
            q = 0
    else:
        q = 1
    