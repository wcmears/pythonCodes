#All code written by William Mears III

#Import neccessary packages
from re import A
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox
import tkinter as tk
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
import datetime
import pytz
import numpy as np
from dateutil import tz
import matplotlib.pyplot as plt
from pysolar.solar import *
import timezonefinder
from matplotlib.ticker import AutoMinorLocator

#Define entire code as a function, neccessary for turning into EXE
#CMD prompt to make executable : pyinstaller.exe --onefile --noconsole --icon=logoHeader.ico headereditor2.py 
def main():
    
    #Portion to initialize and name window
    global a
    a = 0
    window = Tk()
    window.geometry('1050x460') #Set window parameters
    window.title("Celestial Rise/Set Time Calculator") #name window
    #window.iconbitmap(logoHeader.ico)#set icon for program
    
    #Section initializes all labels, entry boxes, check buttons, and directory select buttons
    titlelbl = Label(window, text="Celestial Rise/Set Time Calculator", font=("Arial Bold", 10))
    titlelbl.grid(column=0, row=0)#Place title on grid

    namelbl = Label(window, text="All code written by William Mears", font=("Arial", 10))
    namelbl.grid(column=0, row=1)#Place title on grid    
    
    ddexmplLbl = Label(window, text="Enter decimal degrees as a floating point number (ex. 76.98)", font = ("Arial", 10))
    ddexmplLbl.grid(column=0,row=2)
    
    coordexmplLbl = Label(window, text="Enter west and south coordinates as negative and north and east coordinates as positive", font = ("Arial", 10))
    coordexmplLbl.grid(column=0,row=3)

    hmsexmplLbl = Label(window, text="Enter hours minutes seconds in the following format: HH:MM:SS.ss (ex. 13:12:19.12)", font = ("Arial", 10))
    hmsexmplLbl.grid(column=0,row=4)

    dmsexmplLbl = Label(window, text="Enter DMS in the following format: DD:MM:SS.ss (ex. 79:14:19.12)", font = ("Arial", 10))
    dmsexmplLbl.grid(column=0,row=5)       
    
    datelbl = Label(window, text="Enter the date you would like to calculate for (YYYY-MM-DD)", font=("Arial Bold", 10)) #Label for txt entry window
    datelbl.grid(column=0, row=6) #Place label on grid
    dateEntry = Entry(window,width=10) #Entry window for keyword
    dateEntry.grid(column=1, row=6) #Place entry window on grid

    presetLbl = Label(window, text="Select Olin, SRO, MMO, or custom coordinates", font=("Arial Bold", 10)) #Label for txt entry window
    presetLbl.grid(column=0, row=7) #Place label on grid
    observechk_state = BooleanVar() #Make check state true or false variable
    observechk_state.set(False) #Have check box set to false upon opening window
    observechk_stateOne = BooleanVar() #^
    observechk_stateOne.set(False)#^
    observechk_stateTwo = BooleanVar() #^
    observechk_stateTwo.set(False)#^     
    observechk_stateThree = BooleanVar() #^
    observechk_stateThree.set(False)#^   
    observechk = Checkbutton(window, text='Olin', var=observechk_state) #Set first check box and assign to boolean variable
    observechk.grid(column=1, row=7) #Place check box on grid
    observechkOne = Checkbutton(window, text='SRO', var=observechk_stateOne) #Set second check box and assign to boolean variable
    observechkOne.grid(column=2, row=7) #Place check box on grid    
    observechkTwo = Checkbutton(window, text='MMO', var=observechk_stateTwo) #Set second check box and assign to boolean variable
    observechkTwo.grid(column=3, row=7) #Place check box on grid  
    observechkThree = Checkbutton(window, text='CC', var=observechk_stateThree) #Set second check box and assign to boolean variable
    observechkThree.grid(column=4, row=7) #Place check box on grid       
   
    
    latLbl = Label(window, text="If custom coordinates, enter observer latitude", font=("Arial Bold", 10)) #Label for txt entry window
    latLbl.grid(column=0, row=8) #Place label on grid
    latEntry = Entry(window,width=10) #Entry window for keyword
    latEntry.grid(column=1, row=8) #Place entry window on grid
    
    latchk_state = BooleanVar() #Make check state true or false variable
    latchk_state.set(False) #Have check box set to false upon opening window
    latchk_stateTwo = BooleanVar() #^
    latchk_stateTwo.set(False)#^    
    latchk = Checkbutton(window, text='DD', var=latchk_state) #Set first check box and assign to boolean variable
    latchk.grid(column=2, row=8) #Place check box on grid
    latchkOne = Checkbutton(window, text='DMS', var=latchk_stateTwo) #Set second check box and assign to boolean variable
    latchkOne.grid(column=3, row=8) #Place check box on grid

    longLbl = Label(window, text="If custom coordinates, enter observer longitude", font=("Arial Bold", 10)) #Label for txt entry window
    longLbl.grid(column=0, row=9) #Place label on grid
    longEntry = Entry(window,width=10) #Entry window for keyword
    longEntry.grid(column=1, row=9) #Place entry window on grid

    longchk_state = BooleanVar() #Make check state true or false variable
    longchk_state.set(False) #Have check box set to false upon opening window
    longchk_stateTwo = BooleanVar() #^
    longchk_stateTwo.set(False)#^    
    longchk = Checkbutton(window, text='DD', var=longchk_state) #Set first check box and assign to boolean variable
    longchk.grid(column=2, row=9) #Place check box on grid
    longchkOne = Checkbutton(window, text='DMS', var=longchk_stateTwo) #Set second check box and assign to boolean variable
    longchkOne.grid(column=3, row=9) #Place check box on grid

    presettwoLbl = Label(window, text="Enter object name, or enter 'custom' to enter object coordinates", font=("Arial Bold", 10)) #Label for txt entry window
    presettwoLbl.grid(column=0, row=10) #Place label on grid
    presettwoEntry = Entry(window,width=10) #Entry window for keyword
    presettwoEntry.grid(column=1, row=10) #Place entry window on grid      
    
    ascLbl = Label(window, text="If custom, enter object right ascension", font=("Arial Bold", 10)) #Label for txt entry window
    ascLbl.grid(column=0, row=11) #Place label on grid
    ascEntry = Entry(window,width=10) #Entry window for keyword
    ascEntry.grid(column=1, row=11) #Place entry window on grid   
    
    ascchk_state = BooleanVar() #Make check state true or false variable
    ascchk_state.set(False) #Have check box set to false upon opening window
    ascchk_stateOne = BooleanVar() #^
    ascchk_stateOne.set(False)#^
    ascchk_stateTwo = BooleanVar() #^
    ascchk_stateTwo.set(False)#^      
    ascchk = Checkbutton(window, text='DD', var=ascchk_state) #Set first check box and assign to boolean variable
    ascchk.grid(column=2, row=11) #Place check box on grid
    ascchkOne = Checkbutton(window, text='HMS', var=ascchk_stateOne) #Set second check box and assign to boolean variable
    ascchkOne.grid(column=3, row=11) #Place check box on grid    
    ascchkOne = Checkbutton(window, text='DMS', var=ascchk_stateTwo) #Set second check box and assign to boolean variable
    ascchkOne.grid(column=4, row=11) #Place check box on grid    
    
    decLbl = Label(window, text="If custom, enter objects declination", font=("Arial Bold", 10)) #Label for txt entry window
    decLbl.grid(column=0, row=12) #Place label on grid
    decEntry = Entry(window,width=10) #Entry window for keyword
    decEntry.grid(column=1, row=12) #Place entry window on grid
    
    decchk_state = BooleanVar() #Make check state true or false variable
    decchk_state.set(False) #Have check box set to false upon opening window
    decchk_stateTwo = BooleanVar() #^
    decchk_stateTwo.set(False)#^       
    decchk = Checkbutton(window, text='DD', var=decchk_state) #Set first check box and assign to boolean variable
    decchk.grid(column=2, row=12) #Place check box on grid
    decchkOne = Checkbutton(window, text='DMS', var=decchk_stateTwo) #Set second check box and assign to boolean variable
    decchkOne.grid(column=3, row=12) #Place check box on grid 

    optionsLbl = Label(window, text="If graph, select options for graph ouput", font=("Arial Bold", 10)) #Label for txt entry window
    optionsLbl.grid(column=0, row=13) #Place label on grid 
    optionschk_state = BooleanVar() #Make check state true or false variable    
    optionschk_state.set(False) #Have check box set to false upon opening window
    optionschk_stateTwo = BooleanVar() #^
    optionschk_stateTwo.set(False)#^    
    optionschk = Checkbutton(window, text='Gridlines', var=optionschk_state) #Set first check box and assign to boolean variable
    optionschk.grid(column=1, row=13) #Place check box on grid
    optionschkOne = Checkbutton(window, text='Plot Sun', var=optionschk_stateTwo) #Set second check box and assign to boolean variable
    optionschkOne.grid(column=2, row=13) #Place check box on grid

    txtLbl = Label(window, text="Enter name for text file", font=("Arial Bold", 10)) #Label for txt entry window
    txtLbl.grid(column=0, row=14) #Place label on grid
    txtEntry = Entry(window,width=10) #Entry window for keyword
    txtEntry.grid(column=1, row=14) #Place entry window on grid

    formLbl = Label(window, text="Select Local, UTC, or both for rise/set time output", font=("Arial Bold", 10)) #Label for txt entry window
    formLbl.grid(column=0, row=15) #Place label on grid
    outputchk_state = BooleanVar() #Make check state true or false variable
    outputchk_state.set(False) #Have check box set to false upon opening window
    outputchk_stateOne = BooleanVar() #^
    outputchk_stateOne.set(False)#^   
    outputchk = Checkbutton(window, text='Local', var=outputchk_state) #Set first check box and assign to boolean variable
    outputchk.grid(column=1, row=15) #Place check box on grid
    outputchkOne = Checkbutton(window, text='UTC', var=outputchk_stateOne) #Set second check box and assign to boolean variable
    outputchkOne.grid(column=2, row=15) #Place check box on grid     


    formaLbl = Label(window, text="Select local or UTC for graph output", font=("Arial Bold", 10)) #Label for txt entry window
    formaLbl.grid(column=0, row=16) #Place label on grid
    grphchk_state = BooleanVar() #Make check state true or false variable    
    grphchk_state.set(False) #Have check box set to false upon opening window
    grphchk_stateTwo = BooleanVar() #^
    grphchk_stateTwo.set(False)#^    
    grphchk = Checkbutton(window, text='Local', var=grphchk_state) #Set first check box and assign to boolean variable
    grphchk.grid(column=1, row=16) #Place check box on grid
    grphchkOne = Checkbutton(window, text='UTC', var=grphchk_stateTwo) #Set second check box and assign to boolean variable
    grphchkOne.grid(column=2, row=16) #Place check box on grid

    #Offset function
    def getUTCoffset(date, latit, longit):

        tf = timezonefinder.TimezoneFinder()
        timezone = pytz.timezone(tf.certain_timezone_at(lat=latit, lng=longit))
        offSet_str = str(timezone.utcoffset(datetime.datetime.strptime( date + ' 12:12:12', '%Y-%m-%d %H:%M:%S')))

        if offSet_str[0] != '-':
            offSet = int(offSet_str[0])
        else:
            offSet = int(offSet_str[8] + offSet_str[9]) - 24

        return offSet
    
    #hmsToDD Function: Goes through a string with HMS and converts to decimal degrees. Each character is appended to appropriate string
    #until no longer needed. Then each measurement is converted to degrees
    def hmsToDD(inp):
        colon = 0
        degrees = 0
        hours = ''
        minutes = ''
        seconds = ''
        for i in range(0,len(inp)):
            if colon == 0 and inp[i] != ':':
                hours = hours + inp[i]
            elif colon == 0 and inp[i] == ':':
                colon += 1
            elif colon == 1 and inp[i] != ':':
                minutes = minutes + inp[i]
            elif colon == 1 and inp[i] == ':':
                colon += 1    
            else:
                seconds = seconds + inp[i]
        degrees = (float(hours) / 24)*360
        degrees = degrees + (float(minutes)/1440)*360
        degrees = degrees + (float(seconds)/86400)*360
        if degrees <= 180:
            degrees = degrees * -1        
        return degrees
    
    #dmsToDD Function: Does the same thing as hms to dd except with no conversion for the first number
    def dmsToDD(inp):
        colon = 0
        degrees = ''
        minutes = ''
        seconds = ''
        for i in range(0,len(inp)):
            if colon == 0 and inp[i] != ':':
                degrees = degrees + inp[i]
            elif colon == 0 and inp[i] == ':':
                colon += 1
            elif colon == 1 and inp[i] != ':':
                minutes = minutes + inp[i]
            elif colon == 1 and inp[i] == ':':
                colon += 1    
            else:
                seconds = seconds + inp[i]
        degrees = float(degrees)
        degrees = degrees + (float(minutes)*(-1)/60)
        degrees = degrees + (float(seconds)*(-1)/3600)
        if degrees <= 180:
            degrees = degrees * -1
        return degrees
    
    #Clear Function: clears all of the labels that are below the buttons
    def clear():
        global a
        if a == 0: #a will only be one if the display portion is empty
            tk.messagebox.showinfo("Error", "No data to clear!")
            return
        else:
            for label in window.grid_slaves():
                if int(label.grid_info()["row"]) > 17:
                    label.grid_forget()
        a = 0
        
    
    #Process Function
    def process():
        #a is created so, if there is no data to clear, an error will pop up
        global a 
        a = 1
        selectOne = 0
        txtName = txtEntry.get() + '.txt'
        #If nothing was added to the string, give an error
        if txtName == '.txt':
            tk.messagebox.showinfo("Error", "Add name for txt file")
            return
        #Define source name for multiple purposes
        sourceName = presettwoEntry.get()

        txtStr = ''        
        #If source is not looked up, call generic name source
        if sourceName == 'custom':
            sourceName = 'Source'

        #If custom coordinates, get right ascension and declanation and convert to degrres if neccessary
        #Give errror if hms or dms functions give error
        if presettwoEntry.get() == 'custom':

            asc = ascEntry.get()
            if ascchk_stateOne.get() == True:
                try:
                    asc = hmsToDD(asc)    
                except:
                    tk.messagebox.showinfo("Error", "Check right ascension HMS format")
                    return            
            elif ascchk_stateTwo.get() == True: 
                try:
                    asc = dmsToDD(asc)    
                except:
                    tk.messagebox.showinfo("Error", "Check right ascension DMS format")
                    return                             
            else:
                try:
                    asc = float(asc)
                except:
                    tk.messagebox.showinfo("Error", "Check right ascension format")
                    return
                
            decl = decEntry.get()      
            if decchk_stateTwo.get() == True: 
                try:
                    decl = dmsToDD(decl)    
                except:
                    tk.messagebox.showinfo("Error", "Check declination DMS format")
                    return              
            else:
                try:
                    decl = float(decl)  
                except:
                    tk.messagebox.showinfo("Error", "Check declination format")
                    return   
            try:
                if asc > 360 or asc < 0:
                    tk.messagebox.showinfo("Error", "For DD, enter right ascension between 0 and 360")
                    return         
            except:
                    tk.messagebox.showinfo("Error", "Check right ascension format")
                    return   

            try:
                if decl > 90 or decl < -90:
                    tk.messagebox.showinfo("Error", "Declination too large or too small")
                    return         
            except:
                    tk.messagebox.showinfo("Error", "Check declination format")
                    return                                                  

            obj = SkyCoord(ra=asc*u.degree, dec=decl*u.degree, frame='icrs')
        else:
            try:
                obj = SkyCoord.from_name(presettwoEntry.get())  
            except:
                tk.messagebox.showinfo("Error", "Object not found")
                return
        
        #Do the same thing as right ascension and declination with latitude and longitude. Change format to decimal degrees
        if observechk_stateThree.get() == True:                                            
            selectOne += 1
            lati = latEntry.get()
            if latchk_stateTwo.get() == True: 
                try:
                    lati = dmsToDD(lati)    
                except:
                    tk.messagebox.showinfo("Error", "Check latitude DMS format")
                    return         
            else:
                try:
                    lati = float(lati)
                except:
                    tk.messagebox.showinfo("Error", "Check latitude format")
                    return
            
            long = longEntry.get()      
            if longchk_stateTwo.get() == True: 
                try:
                    long = dmsToDD(long)    
                except:
                    tk.messagebox.showinfo("Error", "Check longitude DMS format")
                    return           
            else:
                try:
                    long = float(long)
                except:
                    tk.messagebox.showinfo("Error", "Check longitude format")
                    return

            loca = EarthLocation(lat=lati*u.deg, lon=long*u.deg, height=0*u.m)

            try:
                offset = getUTCoffset(dateEntry.get(), lati, long)
            except:
                tk.messagebox.showinfo("Error", "Enter date in the format YYYY-MM-DD")
                return
            try:
                float(latEntry.get())
                float(longEntry.get())
            except:
                tk.messagebox.showinfo("Error", "Check format for latitude and longitude")
                return   
                 
            if int(latEntry.get()) > 90 or int(latEntry.get()) < -90:
                tk.messagebox.showinfo("Error", "Latitude too large or too small!")
                return
            if int(longEntry.get()) > 180 or int(longEntry.get()) < -180:
                tk.messagebox.showinfo("Error", "Longitude too large or too small!")
                return                    
        
        #Get coordinates for observatory. If preset observatory, hardcode in coordinates. Else, get coordinates from user entries
        #Used try and except on a few instances of date being called to make sure format was correct
        #Made variable called select one. If more than one option was chosen for observatory, give error and return.
        if observechk_state.get() == True:
            selectOne += 1
            lati = 41.3789
            long = -72.1053            
            loca = EarthLocation(lat=lati*u.deg, lon=long*u.deg, height=0*u.m)
            try:
                offset = getUTCoffset(dateEntry.get(), lati, long)    
            except:
                tk.messagebox.showinfo("Error", "Enter date in the format YYYY-MM-DD")       
                return 
        if observechk_stateOne.get() == True:
            selectOne += 1
            lati = 37
            long = -120         
            loca = EarthLocation(lat=lati*u.deg, lon=long*u.deg, height=0*u.m)
            try:
                offset = getUTCoffset(dateEntry.get(), lati, long)     
            except:
                tk.messagebox.showinfo("Error", "Enter date in the format YYYY-MM-DD")    
                return   
        if observechk_stateTwo.get() == True:
            selectOne += 1
            lati = 41.28068
            long = -70.10363
            loca = EarthLocation(lat=lati*u.deg, lon=long*u.deg, height=0*u.m)
            try:
                offset = getUTCoffset(dateEntry.get(), lati, long)    
            except:
                tk.messagebox.showinfo("Error", "Enter date in the format YYYY-MM-DD")    
                return

        if observechk_stateTwo.get() == False and observechk_state.get() == False and observechk_stateOne.get() == False and observechk_stateThree.get() == False:
             tk.messagebox.showinfo("Error", "Enter 'Olin', 'SRO', 'Mariah Mitchell', or 'cc'")
             return

        if selectOne > 1:
            tk.messagebox.showinfo("Error", "Select only one option for observatory")    
            return         

        if outputchk_stateOne.get() == False and outputchk_state.get() == False: 
            tk.messagebox.showinfo("Error", "Select local, utc, or both for rise/set time outputs")
            return            

     #If UTC, create and populate an array full of the altitudes for the source. This is done at every minute here. Results are then
     #printed on labels in the GUI and saved to a text file
        if outputchk_stateOne.get() == True:  
            altitude = []
            az = []
            timeArr = []
            for i in range(0, 86400, 300):
                try:
                    timeStr = dateEntry.get() + ' ' + str(datetime.timedelta(seconds=i))
                    timeArr.append(str(datetime.timedelta(seconds=i)))     
                    time = Time(timeStr)
                    objaltaz = obj.transform_to(AltAz(obstime=time,location=loca))
                except:
                    tk.messagebox.showinfo("Error", "Enter date in the format YYYY-MM-DD")    
                altitude.append(objaltaz.alt.degree)
                az.append(objaltaz.az.degree)
            #Go through all of the altitudes and see where it crosses 0. If it never crosses 0,
            #note this
            for i in range(1,1440):
                altOne = altitude[i-1]
                altTwo = altitude[i]            
                if float(altOne) < 0 and float(altTwo) >= 0:

                    readability = Label(window, text="", font=("Arial Bold", 10)) #Label for txt entry window
                    readability.grid(column=0, row=18)  

                    riseLbl = Label(window, text=sourceName + " rises at " + timeArr[i] + " UTC (Azimuth = " + str(az[i]) 
                    + " degrees)", font=("Arial Bold", 10)) #Label for txt entry window
                    riseLbl.grid(column=0, row=19)

                    txtStr = txtStr + sourceName + " rises at " + timeArr[i] + " UTC (Azimuth = " + str(az[i]) + " degrees) "

                elif float(altOne) > 0 and float(altTwo) <= 0:  

                    readabilityTwo = Label(window, text="", font=("Arial Bold", 10)) #Label for txt entry window
                    readabilityTwo.grid(column=0, row=20)                       

                    setLbl = Label(window, text=sourceName + " sets at " + timeArr[i] + " UTC (Azimuth = " + str(az[i]) 
                    + " degrees)", font=("Arial Bold", 10)) 
                    setLbl.grid(column=0, row=21)

                    txtStr = txtStr + sourceName + " sets at " + timeArr[i] + " UTC (Azimuth = " + str(az[i]) + " degrees) "

            altitude = np.array(altitude)
            altitude = altitude.astype(float)

            if all(i >= 0 for i in altitude):
                readabilityf = Label(window, text="", font=("Arial Bold", 10)) #Label for txt entry window
                readabilityf.grid(column=0, row=18)  
                nosetLbl = Label(window, text=sourceName + " never sets (UTC)", font=("Arial Bold", 10)) #Label for txt entry window
                nosetLbl.grid(column=0, row=19)   
                txtStr = txtStr + sourceName + " never sets (UTC) "             
            elif all(i <= 0 for i in altitude):
                readabilityff = Label(window, text="", font=("Arial Bold", 10)) #Label for txt entry window
                readabilityff.grid(column=0, row=18)              
                noriseLbl = Label(window, text=sourceName + " never rises (UTC)", font=("Arial Bold", 10)) #Label for txt entry window
                noriseLbl.grid(column=0, row=19)   
                txtStr = txtStr + sourceName + " never rises (UTC) "                      
        #Local time calculation, do the same thing as UTC
        if outputchk_state.get() == True:  
            localAlt = []
            localAz = []
            timeArr = []  
            try:
                date = datetime.datetime.strptime(dateEntry.get(), '%Y-%m-%d')
            except:
                tk.messagebox.showinfo("Error", "Enter date in the format YYYY-MM-DD")  
                return  
            for i in range(0, 86400, 300):
                timeStr = dateEntry.get() + ' ' + str(datetime.timedelta(seconds=i))
                timeArr.append(str(datetime.timedelta(seconds=i)))   
                if offset < 0:
                    offset = offset * -1
                    timeStr = date + datetime.timedelta(seconds=i) - datetime.timedelta(hours=offset)
                    timeStr = str(timeStr)
                    time = Time(timeStr)
                else:
                    timeStr = date + datetime.timedelta(seconds=i) + datetime.timedelta(hours=offset)
                    timeStr = str(timeStr)
                    time = Time(timeStr)
                objaltaz = obj.transform_to(AltAz(obstime=time,location=loca))
                localAlt.append(objaltaz.alt.degree)
                localAz.append(objaltaz.az.degree)    

            for i in range(1,1440):
                localtOne = localAlt[i-1]
                localtTwo = localAlt[i]            
                if float(localtOne) < 0 and float(localtTwo) >= 0:

                    readabilitythree = Label(window, text="", font=("Arial Bold", 10)) #Label for txt entry window
                    readabilitythree.grid(column=0, row=22)  


                    riseLblOne = Label(window, text=sourceName + " rises at " + timeArr[i] + " local time (Azimuth = " + str(localAz[i]) 
                    + " degrees)", font=("Arial Bold", 10)) #Label for txt entry window
                    riseLblOne.grid(column=0, row=23)

                    txtStr = txtStr + sourceName + " rises at " + timeArr[i] + " local time (Azimuth = " + str(localAz[i]) + " degrees) "

                elif float(localtOne) > 0 and float(localtTwo) <= 0:  

                    readabilityFour = Label(window, text="", font=("Arial Bold", 10)) #Label for txt entry window
                    readabilityFour.grid(column=0, row=24)                       

                    setLblOne = Label(window, text=sourceName + " sets at " + timeArr[i] + " local time (Azimuth = " + str(localAz[i]) 
                    + " degrees)", font=("Arial Bold", 10)) 
                    setLblOne.grid(column=0, row=25)

                    txtStr = txtStr + sourceName + " sets at " + timeArr[i] + " local time (Azimuth = " + str(localAz[i]) + " degrees) "

            localAlt = np.array(localAlt)
            localAlt = localAlt.astype(float)

            if all(i >= 0 for i in localAlt):
                readabilityfff = Label(window, text="", font=("Arial Bold", 10)) #Label for txt entry window
                readabilityfff.grid(column=0, row=22)  
                nosetLblOne = Label(window, text=sourceName + " never sets (Local)", font=("Arial Bold", 10)) #Label for txt entry window
                nosetLblOne.grid(column=0, row=23)     
                txtStr = txtStr + sourceName + " never sets (Local) "              
            elif all(i <= 0 for i in localAlt):
                readabilityffff = Label(window, text="", font=("Arial Bold", 10)) #Label for txt entry window
                readabilityffff.grid(column=0, row=22)              
                noriseLblOne = Label(window, text=sourceName + " never rises (Local)", font=("Arial Bold", 10)) #Label for txt entry window
                noriseLblOne.grid(column=0, row=23)  
                txtStr = txtStr + sourceName + " never rises (Local) "   
                
            with open(txtName, 'w') as f:
                f.write(txtStr)    
    def graph():

        if grphchk_state.get() == grphchk_stateTwo.get():
            tk.messagebox.showinfo("Error", "Check either local or UTC for graph format")
            return 

        if presettwoEntry.get() == 'custom':

            asc = ascEntry.get()
            if ascchk_stateOne.get() == True:
                try:
                    asc = hmsToDD(asc)    
                except:
                    tk.messagebox.showinfo("Error", "Check right ascension HMS format")
                    return             
            elif ascchk_stateTwo.get() == True: 
                try:
                    asc = dmsToDD(asc)    
                except:
                    tk.messagebox.showinfo("Error", "Check right ascension DMS format")
                    return    
            else:
                try:
                    asc = float(asc)
                except:
                    tk.messagebox.showinfo("Error", "Check right ascension format")
                    return
                
            decl = decEntry.get()      
            if decchk_stateTwo.get() == True: 
                try:
                    decl = dmsToDD(decl)    
                except:
                    tk.messagebox.showinfo("Error", "Check declination DMS format")
                    return               
            else:
                try:
                    decl = float(decl)  
                except:
                    tk.messagebox.showinfo("Error", "Check declination format")
                    return   
            try:
                if asc > 360 or asc < 0:
                    tk.messagebox.showinfo("Error", "For DD, enter right ascension between 0 and 360")
                    return         
            except:
                    tk.messagebox.showinfo("Error", "Check right ascension format")
                    return   

            try:
                if decl > 90 or decl < -90:
                    tk.messagebox.showinfo("Error", "Declination too large or too small")
                    return         
            except:
                    tk.messagebox.showinfo("Error", "Check declination format")
                    return    

            obj = SkyCoord(ra=asc*u.degree, dec=decl*u.degree, frame='icrs')
        else:
            try:
                obj = SkyCoord.from_name(presettwoEntry.get())
            except:
                tk.messagebox.showinfo("Error", "Object not found")
                return
        
        observeCheck = 0
        
        if observechk_stateThree.get() == True:         
            observeCheck += 1
        
            lati = latEntry.get()
            if latchk_stateTwo.get() == True: 
                try:
                    lati = dmsToDD(lati)    
                except:
                    tk.messagebox.showinfo("Error", "Check latitude DMS format")
                    return                        
            else:
                try:
                    lati = float(lati)
                except:
                    tk.messagebox.showinfo("Error", "Check latitude format")
                    return
            
            long = longEntry.get()      
            if longchk_stateTwo.get() == True: 
                try:
                    long = dmsToDD(long)    
                except:
                    tk.messagebox.showinfo("Error", "Check longitude DMS format")
                    return             
            else:
                try:
                    long = float(long)
                except:
                    tk.messagebox.showinfo("Error", "Check longitude format")
                    return

            loca = EarthLocation(lat=lati*u.deg, lon=long*u.deg, height=0*u.m)
            try:
                offset = getUTCoffset(dateEntry.get(), lati, long)
            except:
                tk.messagebox.showinfo("Error", "Enter date in the format YYYY-MM-DD") 
                return   
            try:
                int(latEntry.get())
                int(longEntry.get())
            except:
                tk.messagebox.showinfo("Error", "Check format for latitude and longitude")
                return    
            if int(latEntry.get()) > 90 or int(latEntry.get()) < -90:
                tk.messagebox.showinfo("Error", "Latitude too large or too small!")
                return
            if int(longEntry.get()) > 180 or int(longEntry.get()) < -180:
                tk.messagebox.showinfo("Error", "Longitude too large or too small!")
                return    

        if observechk_state.get() == True:
            observeCheck += 1
            lati = 41.3789
            long = -72.1053            
            loca = EarthLocation(lat=lati*u.deg, lon=long*u.deg, height=0*u.m)
            try:
                offset = getUTCoffset(dateEntry.get(), lati, long)
            except:
                tk.messagebox.showinfo("Error", "Enter date in the format YYYY-MM-DD")   
                return 
        if observechk_stateOne.get() == True:
            observeCheck += 1
            lati = 37
            long = -120          
            loca = EarthLocation(lat=lati*u.deg, lon=long*u.deg, height=0*u.m)
            try:
                offset = getUTCoffset(dateEntry.get(), lati, long)
            except:
                tk.messagebox.showinfo("Error", "Enter date in the format YYYY-MM-DD")    
                return
        if observechk_stateTwo.get() == True:
            observeCheck += 1
            lati = 41.28068
            long = -70.10363
            loca = EarthLocation(lat=lati*u.deg, lon=long*u.deg, height=0*u.m)
            try:
                offset = getUTCoffset(dateEntry.get(), lati, long)
            except:
                tk.messagebox.showinfo("Error", "Enter date in the format YYYY-MM-DD")   
                return 
        if observechk_stateTwo.get() == False and observechk_state.get() == False and observechk_stateOne.get() == False and observechk_stateThree.get() == False:
             tk.messagebox.showinfo("Error", "Enter 'Olin', 'SRO', 'Mariah Mitchell', or 'cc'")
             return

        if observeCheck > 1:
            tk.messagebox.showinfo("Error", "Select only one option for observatory")    
            return

        if grphchk_state.get() == True:    
            altitude = []
            timeArr = []
            
            for i in range(-1800, 86400, 1800):
                if i == -1800:
                    i = 0
                try:
                    timeStr = dateEntry.get() + ' ' + str(datetime.timedelta(seconds=i))   
                    timeArr.append(str(datetime.timedelta(seconds=i)))         
                    time = Time(timeStr)
                    objaltaz = obj.transform_to(AltAz(obstime=time,location=loca))
                except:
                    tk.messagebox.showinfo("Error", "Enter date in the format YYYY-MM-DD")    
                    return
                altitude.append(objaltaz.alt.degree)
        elif grphchk_state.get() == False and grphchk_stateTwo.get() == True:
            altitude = []
            timeArr = []  
            try:
                date = datetime.datetime.strptime(dateEntry.get(), '%Y-%m-%d')
            except:
                tk.messagebox.showinfo("Error", "Enter date in the format YYYY-MM-DD")    
                return
            for i in range(-1800, 86400, 1800):
                if i == -1800:
                    i = 0                
                timeStr = dateEntry.get() + ' ' + str(datetime.timedelta(seconds=i))
                timeArr.append(str(datetime.timedelta(seconds=i)))   
                if offset < 0:
                    offset = offset * -1
                    timeStr = date + datetime.timedelta(seconds=i) - datetime.timedelta(hours=offset)
                    timeStr = str(timeStr)
                    time = Time(timeStr)
                else:
                    timeStr = date + datetime.timedelta(seconds=i) + datetime.timedelta(hours=offset)
                    timeStr = str(timeStr)
                    time = Time(timeStr)
                objaltaz = obj.transform_to(AltAz(obstime=time,location=loca))
                altitude.append(objaltaz.alt.degree)    
        else:     
            tk.messagebox.showinfo("Error", "Choose local or UTC for graph output")
            return
       
        plt.figure()

        fig, ax = plt.subplots()

        plt.xticks(rotation = 45) 

        if presettwoEntry.get() == '':
            plt.title("Altitude of Object on " + dateEntry.get())
        else:
            plt.title("Altitude of " + presettwoEntry.get() + " on " + dateEntry.get())
        
        plt.xlabel("Time (UTC)")
        plt.ylabel("Altitude (Degrees)")

        horizon = [0]*len(altitude)

        if optionschk_stateTwo.get() == True:
            sunAlt = []
            year = ''
            month = ''
            day = ''
            colon = 0
            try:
                date = dateEntry.get()
            except:
                tk.messagebox.showinfo("Error", "Enter date in the format YYYY-MM-DD")    
                return
            for i in range(0,len(date)):
                if colon == 0 and date[i] != '-':
                    year = year + date[i]
                elif colon == 0 and date[i] == '-':
                    colon += 1
                elif colon == 1 and date[i] != '-':
                    month = month + date[i]
                elif colon == 1 and date[i] == '-':
                    colon += 1    
                else:
                    day = day + date[i]
            for i in range(0, len(timeArr)):
                colon = 0
                hours = ''
                minutes = ''
                seconds = ''
                time = timeArr[i]
                for i in range(0,len(time)):
                    if colon == 0 and time[i] != ':':
                        hours = hours + time[i]
                    elif colon == 0 and time[i] == ':':
                        colon += 1
                    elif colon == 1 and time[i] != ':':
                        minutes = minutes + time[i]
                    elif colon == 1 and time[i] == ':':
                        colon += 1    
                    else:
                        seconds = seconds + time[i]
                if grphchk_stateTwo.get() == True:         
                    date = datetime.datetime(int(year), int(month), int(day), int(hours), int(minutes), int(seconds), 0, tzinfo=datetime.timezone.utc)
                else:
                    tf = timezonefinder.TimezoneFinder()  
                    date = datetime.datetime(int(year), int(month), int(day), int(hours), int(minutes), int(seconds), 0, tzinfo=datetime.timezone.utc)
                    if offset < 0:
                        offset = offset * -1
                        date = date - datetime.timedelta(hours=offset)
                    else:
                        date = date + datetime.timedelta(hours=offset)
                sunAlt.append(get_altitude(lati, long, date))

            ax.plot(timeArr[1:], sunAlt[1:], "y", label="Sun")
            
        
        if presettwoEntry.get() == '':
            ax.plot(timeArr[1:], altitude[1:], "b", label="Object")
        else:
            ax.plot(timeArr[1:], altitude[1:], "b", label=presettwoEntry.get())

        ax.plot(timeArr[1:], horizon[1:], "r", label="Horizon")

        plt.legend(loc="upper right")

        plt.axhspan(0, -90, facecolor='0.2', alpha=0.5)
        
        plt.tick_params(labelright=True)

        if optionschk_state.get() == True:
            ax.grid(which='major', color='grey', linewidth=1)
            ax.grid(which='minor', color='grey', linewidth=1)

        ax.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax.xaxis.set_minor_locator(AutoMinorLocator(2))
        ax.xaxis.set_major_locator(plt.MaxNLocator(26))

        plt.show()



   
    #Place function buttons on grid
    processbtn = Button(window, text="Process", command=process) #Initialize process button, assign command as process function
    processbtn.grid(column=0, row=17) #place process button on grid     

    clrbtn = Button(window, text="Clear", command=clear) #Initialize clear button, assign command as clear function
    clrbtn.grid(column=1, row=17) #place clear button on grid 
    
    graphbtn = Button(window, text="Graph", command=graph) #Initialize clear button, assign command as clear function
    graphbtn.grid(column=2, row=17) #place clear button on grid 

    #Run
    window.mainloop()


if __name__ == '__main__':
    main()