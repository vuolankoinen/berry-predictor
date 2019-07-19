**This is still work in progress**

Combining Finnish berry sales data from documents MARSI LUONNONMARJOJEN JA -SIENTEN KAUPPAANTULOMAARAT to weather data from FMI at https://ilmatieteenlaitos.fi/havaintojen-lataus (loaded on 12.7.2019). Planning to host a predictor on Heroku that queries the FMI API for fresh data as necessary and predicts the berry sales for the next season.

Retrieving recent meteorological data requires enviromental variable FMI-API that contains a valid API key for the Finnish meteorological institute. Data is loaded at regular intervals using Heroku scheduler.
