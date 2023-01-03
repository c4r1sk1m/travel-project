from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import brotli
import json

from util import load_headers, get_webpage, extract_listing_data, extract_next_page_url
from TrustedHouseSitters import TrustedHouseSitter

def test():
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
    

    print(res_df)




    unique = { each['id'] : each for each in tempList }.values()
    print(len(unique))
    # print(len(tempList))
    tempMap = {}
    for listing in tempList:
        tempMap[listing["id"]] = listing["id"]
    print(len(tempMap.keys()))
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




if __name__ == '__main__':
    # main()
    test()