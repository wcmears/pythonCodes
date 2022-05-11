import datetime
import pytz
from tzwhere import tzwhere
import timezonefinder

tf = timezonefinder.TimezoneFinder()
timezone = pytz.timezone(tf.certain_timezone_at(lat=37, lng=-120))
offSet_str = str(timezone.utcoffset(datetime.datetime.strptime( '2020-5-12' + ' 12:12:12', '%Y-%m-%d %H:%M:%S')))
if offSet_str[0] != '-':
    offSet = int(offSet_str[0])
else:
    offSet = int(offSet_str[8] + offSet_str[9]) - 24

print(offSet)