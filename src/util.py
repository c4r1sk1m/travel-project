import requests
import json
from bs4 import BeautifulSoup
import brotli
import pandas as pd

def load_headers(filename="headers.json"):
    file = open(filename,"r")
    headers = json.load(file)
    return headers

## Returns BeautifulSoup object
def get_webpage(url,headers):
    webpage = requests.get(url,headers=headers)
    try:
        webpage.content.decode('UTF-8','strict')
        webpage = webpage.content
    except UnicodeDecodeError:
        webpage = brotli.decompress(webpage.content)
    return BeautifulSoup(webpage,'html.parser')


## Returns Pandas DataFrame
def extract_listing_data(soup):
    try:
        date_class       = "sc-80wmlu-9 UnOOR"
        location_class   = "sc-1p02vaf-8 sc-80wmlu-12 hGGdQq egUufc"
        link_class       = "sc-80wmlu-8 lalEzr"

        dates     = soup.find_all("div", {"class": date_class})
        locations = soup.find_all("span", {"class": location_class})
        links     = soup.find_all("a", {"class": link_class})

        dates_list  = [str(dates[i].find('span', {"class":'sc-1p02vaf-8 sc-80wmlu-10 hGGdQq dKdTpm'})).split('>')[1][:-6] for i in range(len(dates))]
        loc_list    = [str(locations[i]).split('>')[1][:-6] for i in range(len(locations))]
        links_list  = [i['href'] for i in links]

        ths_df = pd.concat([pd.Series(dates_list), pd.Series(loc_list), pd.Series(links_list)],axis = 1).rename(columns = {0: 'Date Range', 1: 'Location', 2: 'Links'})
        ths_df['Links'] = 'https://www.trustedhousesitters.com' + ths_df['Links']
        ths_df['Start Date'] = ths_df['Date Range'].apply(lambda x: x.split('-')[0].strip())
        ths_df['End Date'] = ths_df['Date Range'].apply(lambda x: x.split('-')[1].strip())  ## TODO: strip date string of chars

        return ths_df
    except Exception as e:
        return None

def extract_next_page_url(soup):
    nextPageClass = "sc-1xjnf9n-1 sc-1xjnf9n-3 eZIrdu jfSzpw"
    
    possibleNextPage = soup.find_all("a", {"class":nextPageClass})

    nextPage = None
    for i in possibleNextPage:
        if "next" in i['aria-label']:
            nextPage = i
    if nextPage == None:
        return ""
    
    return nextPage['href']

