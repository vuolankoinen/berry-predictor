import urllib.request
import urllib.parse
import sys
import time
import os
import pandas as pd
import xml.etree.ElementTree as et

# Get recent meteorological data
begin = 'http://data.fmi.fi/fmi-apikey/' + os.environ['FMI-API']
y = int(time.strftime('%Y'))
m = int(time.strftime('%m'))
m = min(m, 8) # Months after the harvest have no effect on the harvest
last_year = 8 # How many months are used from last year in training the net? 7 = June - December
starttime = time.strftime('{}-{:02d}-01T00:00:00Z'.format(y-1, 13-last_year))
endtime = time.strftime('{}-{:02d}-01T00:00:00Z'.format(y,m))
# req = begin + '/wfs?request=getFeature&storedquery_id=fmi::observations::weather::monthly::multipointcoverage&place=Kittil' + urllib.parse.quote('ä') + '&Starttime=' + starttime + '&endtime=' + endtime + '&'
req = begin + '/wfs?request=getFeature&storedquery_id=fmi::observations::weather::monthly::multipointcoverage&place=Pello&Starttime=' + starttime + '&endtime=' + endtime + '&'
FIMresponse = urllib.request.urlopen(req).read().decode("utf-8")
root = et.fromstring(FIMresponse)
for br in root.iter():
    if br.tag == '{http://www.opengis.net/gml/3.2}doubleOrNilReasonTupleList':
        data = list(map(float, br.text.split()))

# The index picks the data from the months that have already passed this year,
# interlacing the temperature and rain measurements.
# The indexes 0-7 are the temperatures of the ongoing year.
# The indexes 8-15 are the temperatures of the previous year.
# The indexes 16-23 are the rain amounts of the ongoing year.
# The indexes 24-31 are the rain amounts of the previous year.
ind = [16, 0, 17, 1, 18, 2, 19, 3, 20, 4, 21, 5, 22, 6, 23, 7, 24, 8][0:(2*m-2)]

# Start off with the means for input, to be replaced by actual input values where possible
prediction_input = pd.read_csv(os.getcwd() + '/data/inputs-column-means.csv')
prediction_input = prediction_input.set_index(prediction_input.iloc[:, 0])
prediction_input = prediction_input.iloc[:, 1]

# Include this year's data
for uu, i in enumerate(ind):
    prediction_input[i] = data[uu + 2*last_year]

# Include last year's data
for uu, i in enumerate(range(0, 15, 2)):
    prediction_input[uu + 8] = data[i+1]
    prediction_input[uu + 24] = data[i]

# Save the result
prediction_input = pd.DataFrame(prediction_input)
prediction_input.to_csv(os.getcwd() + '/data/inputs-recent.csv')
