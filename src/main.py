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

    print(validListings)

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