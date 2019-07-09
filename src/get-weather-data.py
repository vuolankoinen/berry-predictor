import urllib.request as urlr # https://docs.python.org/3.7/library/urllib.request.html#module-urllib.request
import sys

starttime = '1999-06-20T10:30:00Z'
endtime = '1999-06-24T10:30:00Z'
req = '/wfs?request=getFeature&storedquery_id=fmi::observations::weather::multipointcoverage&place=Helsinki&starttime=' + starttime  + '&endtime=' + endtime + '&timestep=120&parameters=r_1h,t2m,ws_10min,wg_10min,wd_10min,rh,td,p_sea,vis,n_man'

req2 = 'http://data.fmi.fi/fmi-apikey/5a8163a1-6462-419d-b0aa-66d9e27ed373/wfs?request=getFeature&storedquery_id=fmi::observations::weather::monthly::multipointcoverage&place=Rovaniemi&starttime=2005-05-05T01:00:00Z&endtime=2013-05-05T01:00:00Z&'
# Korkeintaan 10 vuoden kuukausikeskiarvot kerralla.

print(('http://data.fmi.fi/fmi-apikey/' + sys.argv[1] + req), '\n')

data = urlr.urlopen('http://data.fmi.fi/fmi-apikey/' + sys.argv[1] + req).read()
print(data)
