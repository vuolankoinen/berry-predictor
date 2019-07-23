
Combining Finnish berry sales data from documents _Marsi luonnonmarjojen ja -sienten kauppaantulomaarat_ to meteorological data from FMI at https://ilmatieteenlaitos.fi/havaintojen-lataus (loaded on 12.7.2019).

A predictor is hosted on Heroku at https://berry-predictor.herokuapp.com/. The predictor queries the FMI API for fresh data at regular intervals using Heroku scheduler. Retrieving recent meteorological data requires the enviromental variable FMI-API to contain a valid API key for the Finnish meteorological institute. The predictions of the berry sales for the next season are made using a feedforward network built with Keras (TensorFlow backend).

