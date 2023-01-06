from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import brotli
import json

from util import load_headers, get_webpage, extract_listing_data, extract_next_page_url
from TrustedHouseSitters import TrustedHouseSitter

from typing import overload
import numpy as np
import pandas as pd
from tqdm import tqdm 
import json
import os
from scraping import *


def haversine(lat1, lon1, lat2, lon2, to_radians=True, earth_radius=6371):
    """
    slightly modified version: of http://stackoverflow.com/a/29546836/2901002

    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees or in radians)

    All (lat, lon) coordinates must have numeric dtypes and be of equal length.

    """
    if to_radians:
        lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])

    a = np.sin((lat2-lat1)/2.0)**2 + \
        np.cos(lat1) * np.cos(lat2) * np.sin((lon2-lon1)/2.0)**2

    return earth_radius * 2 * np.arcsin(np.sqrt(a))




def top_n_nearest_airports(listing_lat,listing_lon, continent, n):

    print('############## AIRPORT CSV OUTPUT ############')
    airports = pd.read_csv('../airports.csv')

    # Clean up continent data
    airports['continent'] = airports['continent'].astype(str)
    airports.loc[airports['continent']=='nan','continent'] = 'NA'
    print(list(set(airports['continent'])))
    

    # Filter down to same continent
    airports  = airports[airports['continent']==continent]

    # Calculate distance between listing lat lon and airports



    for index, row in airports.iterrows():

        airports.loc[index,'dist'] = haversine(listing_lat, listing_lon, row['latitude_deg'], row['longitude_deg'])


    # coords_1 = (listing_lat, listing_lon)
    # coords_2 = (52.406374, 16.9251681)

    # print(geopy.distance.geodesic(coords_1, [()]).km
    # print( (airports['longitude_deg'] - listing_lon)**2)
    # airports['dist_temp'] = (airports['longitude_deg'] - listing_lon)**2 + (airports['latitude_deg'] - listing_lat)**2
    # airports['dist'] = airports['dist_temp'].apply(lambda x: math.sqrt(x))

    #airports = airports.drop(columns = ['dist_temp'])
    #print(airports['dist'].describe())

    print(airports.sort_values(by = ['dist'])[['name', 'continent','latitude_deg', 'longitude_deg', 'local_code','iata_code','dist']])

 
    #airports['dist'] = math.sqrt( ((airports['longitude_deg'] - ax)**2) + (airports['latitude_deg'] - ay)**2 )

    # print(math.sqrt(((listing_lon - ax)**2)+((listing_lat-ay)**2)))
    

    
    # print(list(set(airports['iso_country'])))
    # print(airports.head(20))



def generate_flight_dataframe(start_date, end_date, departure_location):
    

    #result = scrape_data(__,__, str(start_date), str(end_date))
    result = scrape_data('JFK', 'IST', '2023-05-20', '2023-06-10')
    #print(result)
    #print(pd.DataFrame.from_dict(result))

    # Check type of columns in dataframe
    print([(c, type(pd.DataFrame.from_dict(result)[c][0])) for c in pd.DataFrame.from_dict(result).columns])
    res_df = pd.to_datetime(pd.DataFrame.from_dict(result))

    ## Cleaning dataframe columns

    # Convert date columns to datetime type
    res_df['Leave Date'] = pd.to_datetime(res_df['Leave Date'])
    res_df['Return Date'] = pd.to_datetime(res_df['Return Date'])

    # Convert 'Travel Time' column to int
    res_df['Travel Time_hour_to_min'] = res_df['Travel Time'].apply(lambda x: int(str(x).split('hr')[0].strip())*60 )
    res_df['Travel Time_min'] = res_df['Travel Time'].apply(lambda x: int(str(x).split('min')[0].split('hr')[1].strip()) if 'min' in str(x) else 0 )
    res_df['Travel Time Converted'] = res_df['Travel Time_hour_to_min'] + res_df['Travel Time_min']
    
    return res_df



def generate_THS_dataframe():
    ths = TrustedHouseSitter(headersFile="query_headers.json")

    allListings = ths.search_listings()
    tempList = []
    for listing in allListings:
        tempList = tempList + listing
    
    validListings = []
    for listing in tempList:
        if listing["assignments"] != []:
            validListings.append(listing)

    print(len(validListings))

    # print(tempList)
    print(len(tempList))
    # tempList = list(set(tempList))


    ### Convert Json output to dataframe export ### 

    print('######### PRINTING VALID LISTINGS ###########')

    res_df = pd.DataFrame()

    for v in validListings:

        listingId = v['id']
        listingLocation1a = v['location']['name']
        listingLocation1b = v['location']['admin1Name']
        listingLocation1c = v['location']['countryName']
        listingLocation1d = v['location']['continentName']
        listingLocationLat= v['location']['coordinates']['lat']
        listingLocationLon= v['location']['coordinates']['lon']
        
        listingUserId = v['user']['id']
        listingUserFirstName = v['user']['firstName']
        listingPetCount = [i['name'] + ' (' + str(i['count']) + ')' for i in v['animals']]
        listingTotalPetCount = sum([i['count'] for i in v['animals']])
        
        listingAssignmentsCount = len(v['assignments'])

        for assign in v['assignments']:
            listingAssignmentStart = assign['startDate']
            listingAssignmentEnd = assign['endDate']
            listingAssignmentNumApplicant = assign['numberOfApplicants']
            listingAssignmentReview = assign['isReviewing']
            listingAssignmentConfirmed = assign['isConfirmed']
            
            row_df = {'Listing ID': listingId,
                    'Listing Location 1a': listingLocation1a,
                    'Listing Location 1b': listingLocation1b,
                    'Listing Location 1c': listingLocation1c,
                    'Listing Location 1d': listingLocation1d,
                    'Latitude': listingLocationLat,
                    'Longitude': listingLocationLon,
                    'User ID': listingUserId,
                    'First Name': listingUserFirstName,
                    'Pets': listingPetCount,
                    'Number of Pets': listingTotalPetCount,
                    'Start Date': listingAssignmentStart,
                    'End Date': listingAssignmentEnd,
                    'Number of Applicants': listingAssignmentNumApplicant,
                    'Assignment in Review': listingAssignmentReview,
                    'Assignment is Confirmed': listingAssignmentConfirmed}

            res_df = res_df.append(row_df, ignore_index = True)     


    res_df['Start Date'] = pd.to_datetime(res_df['Start Date'])
    res_df['End Date'] = pd.to_datetime(res_df['End Date'])
    res_df['Duration (Days)'] = res_df['End Date'] - res_df['Start Date']
    

    print(res_df[['Listing Location 1a', 'Listing Location 1b', 'Listing Location 1c', 'Listing Location 1d']])




    # unique = { each['id'] : each for each in tempList }.values()
    # print(len(unique))
    # # print(len(tempList))
    # tempMap = {}
    # for listing in tempList:
    #     tempMap[listing["id"]] = listing["id"]
    # print(len(tempMap.keys()))
        # print(hash(str(listing)))
    # print(allListings[9])


def main():
    baseUrl = "https://www.trustedhousesitters.com"
    url     = "https://www.trustedhousesitters.com/house-and-pet-sitting-assignments/?q=eyJmaWx0ZXJzIjp7ImFjdGl2ZU1lbWJlcnNoaXAiOnRydWUsImFzc2lnbm1lbnRzIjp7InJldmlld2luZyI6ZmFsc2UsImNvbmZpcm1lZCI6ZmFsc2V9LCJnZW9IaWVyYXJjaHkiOnsiY291bnRyeVNsdWciOiJ1bml0ZWQtc3RhdGVzIiwiYWRtaW4xU2x1ZyI6ImNvbG9yYWRvIn19LCJmYWNldHMiOltdLCJzb3J0IjpbeyJwdWJsaXNoZWQiOiJkZXNjIn1dLCJwYWdlIjoxLCJyZXN1bHRzUGVyUGFnZSI6MTIsImRlYnVnIjpmYWxzZX0="
    
    headers = load_headers()
    webpage = get_webpage(url=url,headers=headers)

    df = extract_listing_data(webpage)
    # print(df['Links'])
    next_page = extract_next_page_url(webpage)

    while(next_page != ""):
        # print(next_page)
        page = get_webpage(url=(baseUrl+str(next_page)),headers=headers)
        
        data = extract_listing_data(page)
        if data is not None:
            df = pd.concat([df,data],ignore_index=True)
        next_page = extract_next_page_url(page)

    print(df)
    # for index,row in df.iterrows():
    #     print(index, row)
        
    # print(next_page)


def main2():
    
    # Generate listings for TS
    ths_listings = generate_THS_dataframe()
    continent = ths_listings['Listing Location 1d'][0]


    # Find ton n nearest airports to TS listing location

    top_n_nearest_airports(lat, lon, continent, 2)

    # Feed these airports to generate_flight_dataframe() and generate list of flights





if __name__ == '__main__':
    # main()
    # test()
    #generate_THS_dataframe()
    top_n_nearest_airports(38.922250, -77.254710, 'NA', 2)
    #main2()