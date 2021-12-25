# 0  39.4350  39.840000  39.1200  39.6325  ok  1546214400  140013864
# 1  39.4800  39.712500  38.5575  38.7225  ok  1546387200  148158948
# 2  35.5475  36.430000  35.5000  35.9950  ok  1546473600  365248780
# 3  37.0650  37.137475  35.9500  36.1325  ok  1546560000  234428280
# 4  36.9825  37.207500  36.4750  37.1750  ok  1546819200  219111056

# Date
# 1577955600  295.73  295.75  295.05  295.05     ok   26138
# 1577959200  296.00  296.05  295.80  295.90     ok   13964
# 1577962800  295.51  295.85  295.30  295.76     ok   13840
# 1577966400  296.10  296.18  295.56  295.66     ok  114841
# 1577970000  296.55  296.75  295.90  296.15     ok  187351

import datetime
import dateutil.parser as dp

iso = datetime.datetime.fromtimestamp(1577955600)
print(iso)
print(type(iso))
print(iso.isoformat())
print('---')

def show(iso):
    parsed = dp.isoparse(iso)
    print(parsed)
    print(type(parsed))
    print(int(parsed.timestamp()))
    print(parsed.utcoffset())
    print(parsed.tzname())
    print('---')

show('2020-01-01T00:00:00+00:00')
show('2020-01-01')
