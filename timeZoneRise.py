import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
import datetime
import pytz
from tzwhere import tzwhere

tzwhere = tzwhere.tzwhere()
timezone = pytz.timezone(tzwhere.tzNameAt(41, -74)) 
offSet_str = str(timezone.utcoffset(datetime.datetime.now()))
if offSet_str[0] != '-':
    offSet = int(offSet_str[0])
else:
    offSet = int(offSet_str[8] + offSet_str[9]) - 24
    

objCoord = SkyCoord(ra=10.625*u.degree, dec=41.2*u.degree, frame='icrs')
m33 = SkyCoord.from_name('M33')
bear_mountain = EarthLocation(lat=41.3*u.deg, lon=-74*u.deg, height=390*u.m)

utcoffset = offSet*u.hour
time = Time('2012-7-12 23:00:00') - utcoffset
m33altaz = m33.transform_to(AltAz(obstime=time,location=bear_mountain))
print(f"M33's Altitude = {m33altaz.alt:.2}")    