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

    dmsexmplLbl = Label(window, text="Enter degrees minutes seconds in the following format: DD:MM:SS.ss (ex. 79:14:19.12)", font = ("Arial", 10))
    dmsexmplLbl.grid(column=0,row=5)       
    
    datelbl = Label(window, text="Enter the date you would like to calculate for (YYYY-MM-DD)", font=("Arial Bold", 10)) #Label for txt entry window
    datelbl.grid(column=0, row=6) #Place label on grid
    dateEntry = Entry(window,width=10) #Entry window for keyword
    dateEntry.grid(column=1, row=6) #Place entry window on grid

    presetLbl = Label(window, text="Enter 'Olin', 'SRO', 'MMO', or 'cc' for custom coordinates", font=("Arial Bold", 10)) #Label for txt entry window
    presetLbl.grid(column=0, row=7) #Place label on grid
    presetEntry = Entry(window,width=10) #Entry window for keyword
    presetEntry.grid(column=1, row=7) #Place entry window on grid    
    
    latLbl = Label(window, text="If custom coordinates, enter observer latitude", font=("Arial Bold", 10)) #Label for txt entry window
    latLbl.grid(column=0, row=8) #Place label on grid
    latEntry = Entry(window,width=10) #Entry window for keyword
    latEntry.grid(column=1, row=8) #Place entry window on grid
    
    latchk_state = BooleanVar() #Make check state true or false variable
    latchk_state.set(False) #Have check box set to false upon opening window
    latchk_stateTwo = BooleanVar() #^
    latchk_stateTwo.set(False)#^    
    latchk = Checkbutton(window, text='Decimal Degree', var=latchk_state) #Set first check box and assign to boolean variable
    latchk.grid(column=2, row=8) #Place check box on grid
    latchkOne = Checkbutton(window, text='Degrees Minutes Seconds', var=latchk_stateTwo) #Set second check box and assign to boolean variable
    latchkOne.grid(column=3, row=8) #Place check box on grid

    longLbl = Label(window, text="If custom coordinates, enter observer longitude", font=("Arial Bold", 10)) #Label for txt entry window
    longLbl.grid(column=0, row=9) #Place label on grid
    longEntry = Entry(window,width=10) #Entry window for keyword
    longEntry.grid(column=1, row=9) #Place entry window on grid

    longchk_state = BooleanVar() #Make check state true or false variable
    longchk_state.set(False) #Have check box set to false upon opening window
    longchk_stateTwo = BooleanVar() #^
    longchk_stateTwo.set(False)#^    
    longchk = Checkbutton(window, text='Decimal Degree', var=longchk_state) #Set first check box and assign to boolean variable
    longchk.grid(column=2, row=9) #Place check box on grid
    longchkOne = Checkbutton(window, text='Degrees Minutes Seconds', var=longchk_stateTwo) #Set second check box and assign to boolean variable
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
    ascchk = Checkbutton(window, text='Decimal Degree', var=ascchk_state) #Set first check box and assign to boolean variable
    ascchk.grid(column=2, row=11) #Place check box on grid
    ascchkOne = Checkbutton(window, text='Hours Minutes Seconds', var=ascchk_stateOne) #Set second check box and assign to boolean variable
    ascchkOne.grid(column=3, row=11) #Place check box on grid    
    ascchkOne = Checkbutton(window, text='Degrees Minutes Seconds', var=ascchk_stateTwo) #Set second check box and assign to boolean variable
    ascchkOne.grid(column=4, row=11) #Place check box on grid    
    
    decLbl = Label(window, text="If custom, enter objects declination", font=("Arial Bold", 10)) #Label for txt entry window
    decLbl.grid(column=0, row=12) #Place label on grid
    decEntry = Entry(window,width=10) #Entry window for keyword
    decEntry.grid(column=1, row=12) #Place entry window on grid
    
    decchk_state = BooleanVar() #Make check state true or false variable
    decchk_state.set(False) #Have check box set to false upon opening window
    decchk_stateTwo = BooleanVar() #^
    decchk_stateTwo.set(False)#^       
    decchk = Checkbutton(window, text='Decimal Degree', var=decchk_state) #Set first check box and assign to boolean variable
    decchk.grid(column=2, row=12) #Place check box on grid
    decchkOne = Checkbutton(window, text='Degrees Minutes Seconds', var=decchk_stateTwo) #Set second check box and assign to boolean variable
    decchkOne.grid(column=3, row=12) #Place check box on grid  

    gridLbl = Label(window, text="If graph, would you like gridlines (Y/N)", font=("Arial Bold", 10)) #Label for txt entry window
    gridLbl.grid(column=0, row=13) #Place label on grid
    gridEntry = Entry(window,width=10) #Entry window for keyword
    gridEntry.grid(column=1, row=13) #Place entry window on grid

    sunLbl = Label(window, text="If graph, would you like to plot the sun (Y/N)", font=("Arial Bold", 10)) #Label for txt entry window
    sunLbl.grid(column=0, row=14) #Place label on grid
    sunEntry = Entry(window,width=10) #Entry window for keyword
    sunEntry.grid(column=1, row=14) #Place entry window on grid

    formLbl = Label(window, text="Enter 'local', 'utc', or 'both' for rise/set time output", font=("Arial Bold", 10)) #Label for txt entry window
    formLbl.grid(column=0, row=15) #Place label on grid
    formEntry = Entry(window,width=10) #Entry window for keyword
    formEntry.grid(column=1, row=15) #Place entry window on grid

    formaLbl = Label(window, text="If graph, enter 'local' or 'utc' for graph output", font=("Arial Bold", 10)) #Label for txt entry window
    formaLbl.grid(column=0, row=16) #Place label on grid
    formaEntry = Entry(window,width=10) #Entry window for keyword
    formaEntry.grid(column=1, row=16) #Place entry window on grid    

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
    
    #hmsToDD Function
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
    
    #dmsToDD Function
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
    
    #Clear Function
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
        global a 
        a = 1

        if presettwoEntry.get() == 'custom':

            asc = ascEntry.get()
            if ascchk_stateOne.get() == True:
                asc = hmsToDD(asc)           
            elif ascchk_stateTwo.get() == True: 
                asc = dmsToDD(asc)             
            else:
                asc = float(asc)
                
            decl = decEntry.get()      
            if decchk_stateTwo.get() == True: 
                decl = dmsToDD(decl)             
            else:
                decl = float(decl)    

            obj = SkyCoord(ra=asc*u.degree, dec=decl*u.degree, frame='icrs')
        else:
            try:
                obj = SkyCoord.from_name(presettwoEntry.get())  
            except:
                tk.messagebox.showinfo("Error", "Object not found")
                return
        
        if presetEntry.get() == 'cc':
        
            lati = latEntry.get()
            if latchk_stateTwo.get() == True: 
                lati = dmsToDD(lati)        
            else:
                lati = float(lati)
            
            long = longEntry.get()      
            if longchk_stateTwo.get() == True: 
                long = dmsToDD(long)           
            else:
                long = float(long)   

            loca = EarthLocation(lat=lati*u.deg, lon=long*u.deg, height=0*u.m)

            offset = getUTCoffset(dateEntry.get(), lati, long)

        elif presetEntry.get() == 'Olin':
            lati = 41.3789
            long = -72.1053            
            loca = EarthLocation(lat=lati*u.deg, lon=long*u.deg, height=0*u.m)
            offset = getUTCoffset(dateEntry.get(), lati, long)            
        elif presetEntry.get() == 'SRO':
            lati = 37
            long = -120         
            loca = EarthLocation(lat=lati*u.deg, lon=long*u.deg, height=0*u.m)
            offset = getUTCoffset(dateEntry.get(), lati, long)            
        elif presetEntry.get() == 'MMO':
            lati = 41.28068
            long = -70.10363
            loca = EarthLocation(lat=lati*u.deg, lon=long*u.deg, height=0*u.m)
            offset = getUTCoffset(dateEntry.get(), lati, long)            
        else:
             tk.messagebox.showinfo("Error", "Enter 'Olin', 'SRO', 'MMO', or 'cc'")

        if formEntry.get() == 'utc' or formEntry.get() == 'both':      
            altitude = []
            az = []
            timeArr = []  
            for i in range(0, 86400, 60):
                timeStr = dateEntry.get() + ' ' + str(datetime.timedelta(seconds=i))
                timeArr.append(str(datetime.timedelta(seconds=i)))     
                time = Time(timeStr)
                objaltaz = obj.transform_to(AltAz(obstime=time,location=loca))
                altitude.append(objaltaz.alt.degree)
                az.append(objaltaz.az.degree)

            for i in range(1,1440):
                altOne = altitude[i-1]
                altTwo = altitude[i]            
                if float(altOne) < 0 and float(altTwo) >= 0:

                    readability = Label(window, text="", font=("Arial Bold", 10)) #Label for txt entry window
                    readability.grid(column=0, row=18)  

                    if hmsToDD()
                    riseLbl = Label(window, text="Source rises at " + timeArr[i] + " UTC (Azimuth = " + str(az[i]) 
                    + " degrees)", font=("Arial Bold", 10)) #Label for txt entry window
                    riseLbl.grid(column=0, row=19)

                elif float(altOne) > 0 and float(altTwo) <= 0:  

                    readabilityTwo = Label(window, text="", font=("Arial Bold", 10)) #Label for txt entry window
                    readabilityTwo.grid(column=0, row=20)                       

                    setLbl = Label(window, text="Source sets at " + timeArr[i] + " UTC (Azimuth = " + str(az[i]) 
                    + " degrees), ", font=("Arial Bold", 10)) 
                    setLbl.grid(column=0, row=21)

            altitude = np.array(altitude)
            altitude = altitude.astype(float)

            if all(i >= 0 for i in altitude):
                readabilityf = Label(window, text="", font=("Arial Bold", 10)) #Label for txt entry window
                readabilityf.grid(column=0, row=18)  
                nosetLbl = Label(window, text="Source never sets (UTC)", font=("Arial Bold", 10)) #Label for txt entry window
                nosetLbl.grid(column=0, row=19)      
            elif all(i <= 0 for i in altitude):
                readabilityff = Label(window, text="", font=("Arial Bold", 10)) #Label for txt entry window
                readabilityff.grid(column=0, row=18)              
                noriseLbl = Label(window, text="Source never rises (UTC)", font=("Arial Bold", 10)) #Label for txt entry window
                noriseLbl.grid(column=0, row=19)    
        
        if formEntry.get() == 'local' or formEntry.get() == 'both':
            localAlt = []
            localAz = []
            timeArr = []  
            date = datetime.datetime.strptime(dateEntry.get(), '%Y-%m-%d')
            for i in range(0, 86400, 60):
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


                    riseLblOne = Label(window, text="Source rises at " + timeArr[i] + " local time (Azimuth = " + str(localAz[i]) 
                    + " degrees)", font=("Arial Bold", 10)) #Label for txt entry window
                    riseLblOne.grid(column=0, row=23)

                elif float(localtOne) > 0 and float(localtTwo) <= 0:  

                    readabilityFour = Label(window, text="", font=("Arial Bold", 10)) #Label for txt entry window
                    readabilityFour.grid(column=0, row=24)                       

                    setLblOne = Label(window, text="Source sets at " + timeArr[i] + " local time (Azimuth = " + str(localAz[i]) 
                    + " degrees), ", font=("Arial Bold", 10)) 
                    setLblOne.grid(column=0, row=25)

            localAlt = np.array(localAlt)
            localAlt = localAlt.astype(float)

            if all(i >= 0 for i in localAlt):
                readabilityfff = Label(window, text="", font=("Arial Bold", 10)) #Label for txt entry window
                readabilityfff.grid(column=0, row=22)  
                nosetLblOne = Label(window, text="Source never sets (Local)", font=("Arial Bold", 10)) #Label for txt entry window
                nosetLblOne.grid(column=0, row=23)      
            elif all(i <= 0 for i in localAlt):
                readabilityffff = Label(window, text="", font=("Arial Bold", 10)) #Label for txt entry window
                readabilityffff.grid(column=0, row=22)              
                noriseLblOne = Label(window, text="Source never rises (Local)", font=("Arial Bold", 10)) #Label for txt entry window
                noriseLblOne.grid(column=0, row=23)                

    def graph():

        if presettwoEntry.get() == 'custom':

            asc = ascEntry.get()
            if ascchk_stateOne.get() == True:
                asc = hmsToDD(asc)           
            elif ascchk_stateTwo.get() == True: 
                asc = dmsToDD(asc)             
            else:
                asc = float(asc)
                
            decl = decEntry.get()      
            if decchk_stateTwo.get() == True: 
                decl = dmsToDD(decl)             
            else:
                decl = float(decl)    

            obj = SkyCoord(ra=asc*u.degree, dec=decl*u.degree, frame='icrs')
        else:
            try:
                obj = SkyCoord.from_name(presettwoEntry.get())
            except:
                tk.messagebox.showinfo("Error", "Object not found")
                return
        
        if presetEntry.get() == 'cc':
        
            lati = latEntry.get()
            if latchk_stateTwo.get() == True: 
                lati = dmsToDD(lati)        
            else:
                lati = float(lati)
            
            long = longEntry.get()      
            if longchk_stateTwo.get() == True: 
                long = dmsToDD(long)           
            else:
                long = float(long)   

            loca = EarthLocation(lat=lati*u.deg, lon=long*u.deg, height=0*u.m)
            offset = getUTCoffset(dateEntry.get(), lati, long)

        elif presetEntry.get() == 'Olin':
            lati = 41.3789
            long = -72.1053            
            loca = EarthLocation(lat=lati*u.deg, lon=long*u.deg, height=0*u.m)
            offset = getUTCoffset(dateEntry.get(), lati, long)
        elif presetEntry.get() == 'SRO':
            lati = 37
            long = -120          
            loca = EarthLocation(lat=lati*u.deg, lon=long*u.deg, height=0*u.m)
            offset = getUTCoffset(dateEntry.get(), lati, long)
        elif presetEntry.get() == 'Mariah Mitchell':
            lati = 41.28068
            long = -70.10363
            loca = EarthLocation(lat=lati*u.deg, lon=long*u.deg, height=0*u.m)
            offset = getUTCoffset(dateEntry.get(), lati, long)
        else:
             tk.messagebox.showinfo("Error", "Enter 'Olin', 'SRO', 'Mariah Mitchell', or 'cc'")

        if formaEntry.get() == 'utc':    
            altitude = []
            timeArr = []
            
            for i in range(0, 86400, 1800):
                timeStr = dateEntry.get() + ' ' + str(datetime.timedelta(seconds=i))   
                timeArr.append(str(datetime.timedelta(seconds=i)))         
                time = Time(timeStr)
                objaltaz = obj.transform_to(AltAz(obstime=time,location=loca))
                altitude.append(objaltaz.alt.degree)
        else:
            altitude = []
            timeArr = []  
            date = datetime.datetime.strptime(dateEntry.get(), '%Y-%m-%d')
            for i in range(0, 86400, 1800):
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

       
        plt.figure()

        plt.xticks(rotation = 45) 

        if presettwoEntry.get() == '':
            plt.title("Altitude of Object on " + dateEntry.get())
        else:
            plt.title("Altitude of " + presettwoEntry.get() + " on " + dateEntry.get())
        
        plt.xlabel("Time (UTC)")
        plt.ylabel("Altitude (Degrees)")

        horizon = [0]*len(altitude)

        if sunEntry.get() == 'Y' or 'y':
            sunAlt = []
            year = ''
            month = ''
            day = ''
            colon = 0
            date = dateEntry.get()
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
                if formaEntry.get() == 'utc':         
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

            plt.plot(timeArr, sunAlt, "y", label="Sun")
            
        
        if presettwoEntry.get() == '':
            plt.plot(timeArr, altitude, "b", label="Object")
        else:
            plt.plot(timeArr, altitude, "b", label=presettwoEntry.get())

        plt.plot(timeArr, horizon, "r", label="Horizon")

        if gridEntry.get() == 'Y' or 'y':
            plt.grid()

        plt.legend(loc="upper right")

        plt.axhspan(0, -90, facecolor='0.2', alpha=0.5)
        
        plt.tick_params(labelright=True)

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