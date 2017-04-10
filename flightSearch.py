import pandas as pd
from pandas.io.json import json_normalize
from skyscanner.skyscanner import FlightsCache
from boto.s3.connection import S3Connection
import os
import sys

API_KEY = os.environ.get('SKYSCANNER_API_KEY', None)
print 'API key used:', API_KEY[0]
sys.stdout.flush()

flights_cache_service = FlightsCache(API_KEY)



def getQuotes(origin,destination,date):
    print 'get Quotes started'
    sys.stdout.flush()

    oneWay = True
    result = flights_cache_service.get_cheapest_quotes(
        market='US',
        currency='USD',
        locale='en-US',
        originplace=origin,
        destinationplace=destination,
        outbounddate=date,
        inbounddate='').parsed

    places = json_normalize(result['Places'])
    quotes = json_normalize(result['Quotes'])

    fullQuotes = quotes.merge(places.set_index('PlaceId')[['IataCode']].rename(columns={'IataCode':'OutboundDest'})
                 , left_on = ['OutboundLeg.DestinationId'],
                right_index = True, how = 'left' )

    print fullQuotes[0]

    sys.stdout.flush()
    return fullQuotes[['OutboundDest','OutboundLeg.DepartureDate','MinPrice']]


def comparePrices(originList,destinationList,date):
    print 'compare prices started'
    sys.stdout.flush()
    
    df_final = pd.DataFrame()
    
    for destination in destinationList:
        flightLists = []
        for origin in originList:
            flightLists.append(getQuotes(origin,destination,date))
        
        df = flightLists[0]
        for i in xrange(1,len(flightLists)):
           
            df = df.merge(flightLists[i],on=['OutboundDest','OutboundLeg.DepartureDate']
              ,suffixes = ('_1','_2'))
            df['MinPrice'] = df.MinPrice_1 + df.MinPrice_2
            df = df[['OutboundDest','OutboundLeg.DepartureDate','MinPrice']]
        df_final = df_final.append(df[['OutboundDest','MinPrice']])

    
    return df_final.groupby('OutboundDest').min().sort_values('MinPrice').reset_index()


#List of origin cities followed by list of country destinations
#comparePrices(['AUS','BOS','DFW'],['CA','MX','UK'],'2017-05-12')