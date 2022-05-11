import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
import datetime
import pytz
from tzwhere import tzwhere

# obj = SkyCoord(ra=10.625*u.degree, dec=41.2*u.degree, frame='icrs')
obj = SkyCoord.from_name('Sirius')
bear_mountain = EarthLocation(lat=41.3*u.deg, lon=-74*u.deg, height=0*u.m)

altitude = []
timeArr = []

for i in range(0, 86400, 60):
    timeStr = '2012-7-31 ' + str(datetime.timedelta(seconds=i))
    timeArr.append(timeStr)
    time = Time(timeStr)
    objaltaz = obj.transform_to(AltAz(obstime=time,location=bear_mountain))
    altitude.append(f"{objaltaz.alt:.2}")
    
altOne = altitude[0]
altTwo = altitude[1]

if float(altOne[:-4]) < 0 and float(altTwo[:-4]) >= 0:
    print("Source rises at " + timeArr[1])
elif float(altOne[:-4]) > 0 and float(altTwo[:-4]) <= 0:
    print("Source sets at " + timeArr[1])

for i in range(1,1440):
    altOne = altitude[i-1]
    altTwo = altitude[i]
    if float(altOne[:-4]) < 0 and float(altTwo[:-4]) >= 0:
        print("Source rises at " + timeArr[i])
    elif float(altOne[:-4]) > 0 and float(altTwo[:-4]) <= 0:
        print("Source sets at " + timeArr[i])