import urllib.request # https://docs.python.org/3.7/library/urllib.request.html#module-urllib.request
import urllib.parse
import sys
import time
import pandas as pd
import xml.etree.ElementTree as et

# Get the weather data from this year and part of the last
begin = 'http://data.fmi.fi/fmi-apikey/' + sys.argv[1]
# starttime = '2018-09-01T01:00:00Z'
# endtime = '2019-06-24T10:30:00Z'
y = int(time.strftime('%Y'))
m = int(time.strftime('%m'))
starttime = time.strftime('{}-06-01T00:00:00Z'.format(y-1))
endtime = time.strftime('{}-{:02d}-01T00:00:00Z'.format(y,m))
req = begin + '/wfs?request=getFeature&storedquery_id=fmi::observations::weather::monthly::multipointcoverage&place=Kittil' + urllib.parse.quote('ä') + '&Starttime=' + starttime + '&endtime=' + endtime + '&'
data = urllib.request.urlopen(req).read().decode("utf-8")
root = et.fromstring(data)
for br in root.iter():
    if br.tag == '{http://www.opengis.net/gml/3.2}doubleOrNilReasonTupleList':
        data = list(map(float, br.text.split()))

# More measurements would be given by the query
# req = begin + '/wfs?request=getFeature&storedquery_id=fmi::observations::weather::multipointcoverage&place=Helsinki&starttime=' + starttime  + '&endtime=' + endtime + '&timestep=120&parameters=r_1h,t2m,ws_10min,wg_10min,wd_10min,rh,td,p_sea,vis,n_man'

# The index picks the data from the months that have already passed this year,
# interlacing the temperature and rain measurements.
# The indexes 0-8 are the temperatures of the ongoing year.
# The indexes 9-15 are the temperatures of the previous year.
# The indexes 16-24 are the rain amounts of the ongoing year.
# The indexes 25-31 are the rain amounts of the previous year.
ind = [16, 0, 17, 1, 18, 2, 19, 3, 20, 4, 21, 5, 22, 6, 23, 7, 24, 8][0:(2*m-2)]

# Start off with the means for input, to be replaced by actual input values where possible
prediction_input = pd.read_csv('column-means.csv')
prediction_input = prediction_input.set_index(prediction_input.iloc[:, 0])
prediction_input = prediction_input.iloc[:, 1]
last_year = 7 # How many months are used from last year in training the net? 7 = June - December

# Include this year's data
for uu, i in enumerate(ind):
    prediction_input[i] = data[uu + 2*last_year]

# Include last year's data
for uu, i in enumerate(range(0, 13, 2)):
    prediction_input[uu + 9] = data[i+1]
    prediction_input[uu + 25] = data[i]

prediction_input.to_csv('recent.csv')
