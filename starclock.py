from PIL import ImageTk
import PIL.Image
import tkinter as tk
import tkinter.messagebox
from tkinter import *
from tkinter.ttk import *
from time import strftime
from datetime import datetime as dt
import datetime
import pandas as pd
import pytz
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import time
from pprint import pprint
import geocoder
from astropy.time import Time
from astropy import units as u
import tzwhere
from dateutil import tz
from decimal import Decimal

root = Tk()
root.title('StarClock')
root.geometry('1500x1000')
galaxy=PIL.Image.open("galaxy.jpg")
galaxy=galaxy.resize((1600,1100),PIL.Image.ANTIALIAS)
galaxy2=ImageTk.PhotoImage(galaxy)
label1 = Label( root, image = galaxy2)
label1.place(x = 0, y = 0)

#---------------------------------------------------------------------------------------------------------------------------------

global latitude
global longitude
latitude = 0
longitude = 0

#---------------------------------------------------------------------------------------------------------------------------------

notelab = Label(root, text = "Showing Time for:", font = ('calibri', 18, 'bold'), background = 'black', foreground = 'white')
notelab.grid(column=0, row=1) 

notelab = Label(root, text = "Latitude: " + str(latitude) + " Longitutde: " + str(longitude), font = ('calibri', 18, 'bold'), background = 'black', foreground = 'white')
notelab.grid(column=1, row=1) 

#---------------------------------------------------------------------------------------------------------------------------------

global timezone
t_find = TimezoneFinder()
timezone = t_find.timezone_at(lng=longitude, lat=latitude)
timezone = pytz.timezone(timezone)

#---------------------------------------------------------------------------------------------------------------------------------

translab = Label(root, text = "Time Translator", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
translab.grid(column=2, row=1) 

formlbl = Label(root, text = "Enter one of the following in 'From' Entry: Time, UTC, JD ", font = ('calibri', 12, 'bold'), background = 'black', foreground = 'white')
formlbl.grid(column=2, row=2) 

formlbl = Label(root, text = "Enter one of the following in 'To' Entry: Time, UTC, JD, GMST, LST ", font = ('calibri', 12, 'bold'), background = 'black', foreground = 'white')
formlbl.grid(column=2, row=3) 

formlbl = Label(root, text = "Format: Time/UTC = %Y-%m-%d %H:%M:%S.%f JD = %y%j.%f ", font = ('calibri', 12, 'bold'), background = 'black', foreground = 'white')
formlbl.grid(column=2, row=4) 

formlbl = Label(root, text = "Enter time in format seen to the left, exclude offset from date and time", font = ('calibri', 12, 'bold'), background = 'black', foreground = 'white')
formlbl.grid(column=2, row=5) 

fromlab = Label(root, text = "From:", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
fromlab.grid(column=2, row=6) 

fromEntry = Entry(root,width=10) 
fromEntry.grid(column=3, row=6)

tolab = Label(root, text = "To:", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
tolab.grid(column=2, row=7) 

toEntry = Entry(root,width=10) 
toEntry.grid(column=3, row=7)

timelab = Label(root, text = "Enter time to translate:", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
timelab.grid(column=2, row=8) 

timeEntry = Entry(root,width=10) 
timeEntry.grid(column=3, row=8)

#---------------------------------------------------------------------------------------------------------------------------------

def translate():
    #-----------------------------------------------------------------------------------------------------------------------------
    if fromEntry.get() != 'JD' and fromEntry.get() != 'UTC' and fromEntry.get() != 'Time':
        tk.messagebox.showinfo("Error", "Please enter JD, UTC, or Time in 'From' entry box")
        return
    if toEntry.get() != 'JD' and toEntry.get() != 'UTC' and toEntry.get() != 'Time' and toEntry.get() != 'LST' and toEntry.get() != 'GMST':
        tk.messagebox.showinfo("Error", "Please enter JD, UTC, Time, LST, or GMST in 'To' entry box")
        return
    if str(fromEntry.get()) == str(toEntry.get()):
        tk.messagebox.showinfo("Error", "'To' and 'From' entries should not be the same!")
        return        
    if fromEntry.get() == 'JD':
        try:
            float(timeEntry.get())
        except:
            tk.messagebox.showinfo("Error", "Please enter JD time as number greater than 2086303 and less than 5373484")
            return
    if fromEntry.get() == 'JD' and float(timeEntry.get()) < 2086303 or fromEntry.get() == 'JD' and float(timeEntry.get()) > 5373484 :
        tk.messagebox.showinfo("Error", "Please enter JD time as number greater than 2086303 and less than 5373484")
        return
    if fromEntry.get() == 'UTC' or fromEntry.get() == 'Time':
        try:
            dt.strptime(timeEntry.get(), "%Y-%m-%d %H:%M:%S.%f")
        except:
            tk.messagebox.showinfo("Error", "Please enter time entry in format %Y-%m-%d %H:%M:%S.%f. Seconds must have a decimal point.")
            return
    #-----------------------------------------------------------------------------------------------------------------------------
    for i in root.grid_slaves():
            if int(i.grid_info()["row"]) == 10 and int(i.grid_info()["column"]) == 2 : 
                 i.grid_forget()
    global latitude
    global longitude
    global timezone
    if fromEntry.get() == 'JD':
       times = timeEntry.get()
       t = Time(times, format = 'jd', scale = 'utc')
       utc = dt.strptime(str(t.utc.iso), "%Y-%m-%d %H:%M:%S.%f")
       timez = tz.tzutc()
       utc = utc.replace(tzinfo=timez)
       if toEntry.get() == 'UTC':
           utc = t.utc.iso
           utcstr = strftime(str(utc))
           newlab = Label(root, text = utcstr, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
           newlab.grid(column=2, row=10)            
       elif toEntry.get() == 'GMST':
           newt = utc.astimezone(timezone)
           time = Time(newt, scale='utc', location=(float(longitude), float(latitude)))
           GMST = time.sidereal_time('mean', 'greenwich')
           gmststr = strftime(str(GMST))
           newlab = Label(root, text = gmststr, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
           newlab.grid(column=2, row=10)  
       elif toEntry.get() == 'LST':
           newt = utc.astimezone(timezone)
           time = Time(newt, scale='utc', location=(float(longitude), float(latitude)))
           LST = time.sidereal_time('apparent')
           lststr = strftime(str(LST))
           newlab = Label(root, text = lststr, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
           newlab.grid(column=2, row=10)            
       elif toEntry.get() == 'Time':
           newt = utc.astimezone(timezone)
           nlab = Label(root, text = newt, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
           nlab.grid(column=2, row=10)            
    if fromEntry.get() == 'UTC':
       utc = dt.strptime(timeEntry.get(), "%Y-%m-%d %H:%M:%S.%f")
       timez = tz.tzutc()
       utc = utc.replace(tzinfo=timez)
       if toEntry.get() == 'JD':       
           ts = pd.Timestamp(utc)
           jdstr = strftime(str(ts.to_julian_date()))
           newjdlab = Label(root, text = jdstr, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
           newjdlab.grid(column=2, row=10) 
       elif toEntry.get() == 'GMST':
           newt = utc.astimezone(timezone)
           time = Time(newt, scale='utc', location=(float(longitude), float(latitude)))
           GMST = time.sidereal_time('mean', 'greenwich')
           gmststr = strftime(str(GMST))
           newlab = Label(root, text = gmststr, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
           newlab.grid(column=2, row=10)            
       elif toEntry.get() == 'LST':
           newt = utc.astimezone(timezone)
           time = Time(newt, scale='utc', location=(float(longitude), float(latitude)))
           LST = time.sidereal_time('apparent')
           lststr = strftime(str(LST))
           newlab = Label(root, text = lststr, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
           newlab.grid(column=2, row=10) 
       elif toEntry.get() == 'Time':
           newt = utc.astimezone(timezone)
           nlab = Label(root, text = newt, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
           nlab.grid(column=2, row=10)            
    if fromEntry.get() == 'Time':
       naive = dt.strptime(timeEntry.get(), "%Y-%m-%d %H:%M:%S.%f")
       local_dt = timezone.localize(naive, is_dst=None)
       if toEntry.get() == 'UTC':
           newut = local_dt.astimezone(pytz.utc)
           utcstr = strftime(str(newut))
           newlab = Label(root, text = utcstr, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
           newlab.grid(column=2, row=10) 
       elif toEntry.get() == 'GMST':
           newgm = local_dt.astimezone(pytz.utc)
           time = Time(newgm, scale='utc', location=(float(longitude), float(latitude)))
           GMST = time.sidereal_time('mean', 'greenwich')
           gmststr = strftime(str(GMST))
           newlab = Label(root, text = gmststr, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
           newlab.grid(column=2, row=10) 
       elif toEntry.get() == 'JD':
           newgm = local_dt.astimezone(pytz.utc)
           ts = pd.Timestamp(newgm)
           jdstr = strftime(str(ts.to_julian_date()))
           newjdlab = Label(root, text = jdstr, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
           newjdlab.grid(column=2, row=10) 
       elif toEntry.get() == 'LST':
           newlst = local_dt.astimezone(pytz.utc)
           time = Time(newlst, scale='utc', location=(float(longitude), float(latitude)))
           LST = time.sidereal_time('apparent')
           lststr = strftime(str(LST))
           newlab = Label(root, text = lststr, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
           newlab.grid(column=2, row=10) 
    
transl = Button(root, text="Translate", command=translate)
transl.grid(column=2, row=9)

#---------------------------------------------------------------------------------------------------------------------------------

timelab = Label(root, text = "Time:", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
timelab.grid(column=0, row=2) 

def time():
    datetimeTZ = dt.now(timezone)
    timestring = datetimeTZ.strftime("%I:%M:%S %p")
    timelbl.config(text = timestring)
    timelbl.after(1000, time)

timelbl = Label(root, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
timelbl.grid(column=1, row=2) 

#---------------------------------------------------------------------------------------------------------------------------------

datelab = Label(root, text = "Date and Time:", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
datelab.grid(column=0, row=3) 

def date():
    datetime_object = dt.now(timezone)
    datestr = strftime(str(datetime_object))
    datelbl.config(text = datestr)
    datelbl.after(1000, date)

datelbl = Label(root, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
datelbl.grid(column=1, row=3) 

#---------------------------------------------------------------------------------------------------------------------------------

jdlab = Label(root, text = "Time JD:", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
jdlab.grid(column=0, row=4) 

def jd():
    ts = pd.Timestamp(dt.utcnow()) 
    jdstr = strftime(str(ts.to_julian_date()))
    jdflt = float(jdstr)
    jdflt = round(jdflt, 5)
    jdstr = str(jdflt)
    jdlbl.config(text = jdstr)
    jdlbl.after(1000, jd)

jdlbl = Label(root, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
jdlbl.grid(column=1, row=4) 

#---------------------------------------------------------------------------------------------------------------------------------

mjdlab = Label(root, text = "Time MJD:", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
mjdlab.grid(column=0, row=5) 

def mjd():
    ts = pd.Timestamp(dt.utcnow())  
    mjdstr = strftime(str(ts.to_julian_date()))
    mjdflt = Decimal(mjdstr)
    sub = Decimal(2400000.5)
    mjdflt = mjdflt - sub
    mjdflt = float(mjdflt)
    mjdflt = round(mjdflt, 5)
    mjdstr = str(mjdflt)    
    mjdlbl.config(text = mjdstr)
    mjdlbl.after(1000, mjd)

mjdlbl = Label(root, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
mjdlbl.grid(column=1, row=5) 

#---------------------------------------------------------------------------------------------------------------------------------

utclab = Label(root, text = "Time UTC:", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
utclab.grid(column=0, row=6) 

def ut():
    datetime_object =  dt.utcnow()
    utcstr = strftime(str(datetime_object))  
    utclbl.config(text = utcstr)
    utclbl.after(1000, ut)

utclbl = Label(root, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
utclbl.grid(column=1, row=6) 

#---------------------------------------------------------------------------------------------------------------------------------

lstLabel = Label(root, text = "Local Sidereal Time:", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
lstLabel.grid(column=0, row=7) 

def lst():  
    global longitude
    global latitude
    time = Time(dt.now(timezone), scale='utc', location=(float(longitude), float(latitude)))
    LST = time.sidereal_time('apparent')
    stringloc = str(LST)
    labellocal.config(text = stringloc)
    labellocal.after(1000, lst)

labellocal = Label(root, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
labellocal.grid(column=1, row=7) 

#---------------------------------------------------------------------------------------------------------------------------------

gmstLabel = Label(root, text = "GMST:", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
gmstLabel.grid(column=0, row=8) 

def gmst():  
    global longitude
    global latitude
    time = Time(dt.now(timezone), scale='utc', location=(float(longitude), float(latitude)))
    GMST = time.sidereal_time('mean', 'greenwich')
    stringgreen = str(GMST)
    labelgreen.config(text = stringgreen)
    labelgreen.after(1000, gmst)

labelgreen = Label(root, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
labelgreen.grid(column=1, row=8) 

#---------------------------------------------------------------------------------------------------------------------------------

changetz = Label(root, text = 'Change Timezone', font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
changetz.grid(column=0, row=9) 

latlonlbl = Label(root, text = 'Format:West/South negative, East/North positive', font = ('calibri', 12, 'bold'), background = 'black', foreground = 'white')
latlonlbl.grid(column=1, row=9) 

latlonlbl2 = Label(root, text = 'Enter coordinates in decimal degrees format', font = ('calibri', 12, 'bold'), background = 'black', foreground = 'white')
latlonlbl2.grid(column=1, row=10) 

latlbl = Label(root, text = 'Enter Latitude', font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
latlbl.grid(column=0, row=11) 
latEntry = Entry(root,width=12) 
latEntry.grid(column=1, row=11)

lonlbl = Label(root, text = 'Enter Longitude', font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
lonlbl.grid(column=0, row=12) 
lngEntry = Entry(root,width=12)
lngEntry.grid(column=1, row=12)


#---------------------------------------------------------------------------------------------------------------------------------
def change() :
    #-----------------------------------------------------------------------------------------------------------------------------
    try:
        float(latEntry.get())
        float(lngEntry.get())
    except:
        tk.messagebox.showinfo("Error", "Please enter latitude between -90 and 90, and longitude between -180 and 180")
        return
    if float(latEntry.get()) > 90 or float(latEntry.get()) < -90 or float(lngEntry.get()) > 180 or float(lngEntry.get()) < -180:
        tk.messagebox.showinfo("Error", "Please enter latitude between -90 and 90, and longitude between -180 and 180")
        return    
    #-----------------------------------------------------------------------------------------------------------------------------
    global timezone
    global latitude
    global longitude
    latitude = float(latEntry.get())
    longitude = float(lngEntry.get())
    timezone = t_find.timezone_at(lng=longitude, lat=latitude)
    timezone = pytz.timezone(timezone)
    for i in root.grid_slaves():
            if int(i.grid_info()["row"]) == 1 and int(i.grid_info()["column"]) == 1: 
                 i.grid_forget()
    notelab = Label(root, text = "Latitude: " + str(latitude) + " Longitutde: " + str(longitude), font = ('calibri', 18, 'bold'), background = 'black', foreground = 'white')
    notelab.grid(column=1, row=1) 
    
tbz = Button(root, text="Calculate New Times", command=change)
tbz.grid(column=1, row=13)
lbltkw = Label(root, text = 'Calculate New Times:', font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
lbltkw.grid(column=0, row=13) 

#---------------------------------------------------------------------------------------------------------------------------------

def pause() :
    for i in root.grid_slaves():
            if int(i.grid_info()["row"]) > 14: 
                 i.grid_forget()
    global longitude
    global latitude
    time = Time(dt.now(timezone), scale='utc', location=(float(longitude), float(latitude)))
    LST = time.sidereal_time('apparent')
    GMST = time.sidereal_time('mean', 'greenwich')
    stringloc = str(LST)
    stringgreen = str(GMST)
    datetimeTZ = dt.now(timezone)
    datetime_object = dt.now(timezone)
    utc = dt.utcnow()
    ts = pd.Timestamp(dt.now(timezone))
    lb = Label(root, text = "Time:", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
    lb.grid(column=0, row=15) 
    DT = Label(root, text = "Date and Time:", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
    DT.grid(column=0, row=16) 
    JDT = Label(root, text = "JD Time:", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
    JDT.grid(column=0, row=17) 
    MJDT = Label(root, text = "MJD Time:", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
    MJDT.grid(column=0, row=18)     
    UTT = Label(root, text = "UTC Time:", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
    UTT.grid(column=0, row=19)     
    LTT = Label(root, text = "LST:", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
    LTT.grid(column=0, row=20)      
    GMT = Label(root, text = "GMST:", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
    GMT.grid(column=0, row=21)   
    ia = Label(root, text = "Paused times for:", font = ('calibri', 12, 'bold'), background = 'black', foreground = 'white')
    ia.grid(column=0, row=22)     
    b = Label(root, text = str(datetimeTZ.strftime("%I:%M:%S %p")), font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
    b.grid(column=1, row=15) 
    c = Label(root, text = str(datetime_object), font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
    c.grid(column=1, row=16) 
    jdstr = strftime(str(ts.to_julian_date()))
    jdflt = float(jdstr)
    jdflt = round(jdflt, 5)
    jdstr = str(jdflt)
    d = Label(root, text = str(jdstr), font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
    d.grid(column=1, row=17)  
    mjdstr = strftime(str(ts.to_julian_date()))
    mjdflt = Decimal(mjdstr)
    sub = Decimal(2400000.5)
    mjdflt = mjdflt - sub
    mjdflt = float(mjdflt)
    mjdflt = round(mjdflt, 5)
    mjdstr = str(mjdflt)
    mjdd = Label(root, text = str(mjdstr), font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
    mjdd.grid(column=1, row=18)
    e = Label(root, text = str(utc), font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
    e.grid(column=1, row=19) 
    e = Label(root, text = stringloc, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
    e.grid(column=1, row=20) 
    gm = Label(root, text = stringgreen, font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
    gm.grid(column=1, row=21) 
    inf = Label(root, text = "Latitude: " + str(latitude) + " Longitutde: " + str(longitude), font = ('calibri', 12, 'bold'), background = 'black', foreground = 'white')
    inf.grid(column=1, row=22) 
tiz = Label(root, text="Pause Time:", font = ('calibri', 17, 'bold'), background = 'black', foreground = 'white')
tiz.grid(column=0, row=14)
 
tiz = Button(root, text="Pause and Display time", command=pause)
tiz.grid(column=1, row=14)

#---------------------------------------------------------------------------------------------------------------------------------

time()
date()
jd()
mjd()
ut()
lst()
gmst()
#---------------------------------------------------------------------------------------------------------------------------------
mainloop()