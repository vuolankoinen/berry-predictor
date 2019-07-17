import urllib.request # https://docs.python.org/3.7/library/urllib.request.html#module-urllib.request
import urllib.parse
import sys
import time
import pandas as pd
import xml.etree.ElementTree as et

# Seuraavaksi: senhetkisen pvm:n ottaminen huomioon datan lataamisessa.
# pvm:n mukaan data ennusteita varten joko ladatusta tai keskiarvoista.
# sitten naista muodostetun uusimman datan tallentaminen

begin = 'http://data.fmi.fi/fmi-apikey/' + sys.argv[1]
# starttime = '2018-09-01T01:00:00Z'
# endtime = '2019-06-24T10:30:00Z'
y = int(time.strftime('%Y'))
m = int(time.strftime('%m'))
starttime = time.strftime('{}-06-01T01:00:00Z'.format(y-1))
endtime = time.strftime('{}-{:02d}-01T01:00:00Z'.format(y,m))
print(starttime)
print(endtime)
# req = begin + '/wfs?request=getFeature&storedquery_id=fmi::observations::weather::multipointcoverage&place=Helsinki&starttime=' + starttime  + '&endtime=' + endtime + '&timestep=120&parameters=r_1h,t2m,ws_10min,wg_10min,wd_10min,rh,td,p_sea,vis,n_man'

# print(time.strftime('%Y-%m-%dT01:00:00Z', time.gmtime(time.time())))
# print(time.strftime('%Y-%m-%dT01:00:00Z', time.gmtime(time.time()-60*60*24)))

req = begin + '/wfs?request=getFeature&storedquery_id=fmi::observations::weather::monthly::multipointcoverage&place=Kittil' + urllib.parse.quote('ä') + '&Starttime=' + starttime + '&endtime=' + endtime + '&'

# Korkeintaan 10 vuoden kuukausikeskiarvot kerralla.

# print(time.strftime('%Y-%m-%dT01:00:00Z'))

# The index picks the data from the months that have already passed this year,
# interlacing the temperature and rain measurements.
# The indexes 0-8 are the temperatures of the ongoing year.
# The indexes 9-15 are the temperatures of the previous year.
# The indexes 16-24 are the rain amounts of the ongoing year.
# The indexes 25-31 are the rain amounts of the previous year.
month_now = int(time.strftime('%m'))
ind = [16, 0, 17, 1, 18, 2, 19, 3, 20, 4, 21, 5, 22, 6, 23, 7, 24, 8][0:(2*month_now-2)]

data = urllib.request.urlopen(req).read().decode("utf-8")

file = open('recent.dat', 'w')
file.write(data)
file.close()

root = et.fromstring(data)

prediction_input = pd.read_csv('column-means.csv')
prediction_input = prediction_input.set_index(prediction_input.iloc[:, 0])
prediction_input = prediction_input.iloc[:, 1]
print(prediction_input)

for br in root.iter():
    if br.tag == '{http://www.opengis.net/gml/3.2}doubleOrNilReasonTupleList':
        da = list(map(float, br.text.split()))

print(da)

for uus, i in enumerate(ind):
    prediction_input[i] = da[uus]

print(prediction_input)
