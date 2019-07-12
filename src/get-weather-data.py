import urllib.request # https://docs.python.org/3.7/library/urllib.request.html#module-urllib.request
import urllib.parse
import sys
import time

begin = 'http://data.fmi.fi/fmi-apikey/' + sys.argv[1]
starttime = '2018-09-01T01:00:00Z'
endtime = '2019-06-24T10:30:00Z'
#req = begin + '/wfs?request=getFeature&storedquery_id=fmi::observations::weather::multipointcoverage&place=Helsinki&starttime=' + starttime  + '&endtime=' + endtime + '&timestep=120&parameters=r_1h,t2m,ws_10min,wg_10min,wd_10min,rh,td,p_sea,vis,n_man'

req = begin + '/wfs?request=getFeature&storedquery_id=fmi::observations::weather::monthly::multipointcoverage&place=Kittil' + urllib.parse.quote('ä') + '&Starttime=' + starttime + '&endtime=' + endtime + '&'

req = begin + '/wfs?request=getFeature&storedquery_id=fmi::observations::weather::monthly::multipointcoverage&place=Pello&Starttime=' + starttime + '&endtime=' + endtime + '&'

# Korkeintaan 10 vuoden kuukausikeskiarvot kerralla.
# req = list(urllib.parse.urlsplit(req))
# req[3] = urllib.parse.quote(req[3])
# req = urllib.parse.urlunsplit(req)

# print(time.strftime('%Y-%m-%dT01:00:00Z'))
print(req)
data = urllib.request.urlopen(req)
print(data)
