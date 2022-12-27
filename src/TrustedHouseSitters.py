import requests
import json
import urllib.parse

class TrustedHouseSitter:
    apiKey = ""
    url = "https://www.trustedhousesitters.com/api/v3"
    headers = {}
    def __init__(self,apiKey="",headersFile="headers.json"):
        self.apiKey = apiKey
        with open(headersFile,"r") as file:
            self.headers = json.load(file)
        

    ## Returns a python dict of listings
    def search_listings(self,location="colorado",resultsPerPage=100,page=1):
        
        with open("search_query.json","r") as file:
            queryParamters = json.load(file)

        ## Get First Page
        queryParamters["page"]                                      = page
        queryParamters["filters"]["geoHierarchy"]["admin1Slug"]     = location
        queryParamters["resultsPerPage"]                            = resultsPerPage

        endPoint = self.url +"/search/listings/?query="+urllib.parse.quote(json.dumps(queryParamters))       
        response = requests.get(url=endPoint,headers=self.headers)

        ##
        # Get the next page, check if the next page respsonse is equal to current page, if not equal, append nextpage.content["results"] to results
        results = []
        try:
            while json.loads(response.content)["results"] != []:
                results.append(json.loads(response.content)["results"])
                queryParamters["page"] = queryParamters["page"] + 1
                endPoint = self.url +"/search/listings/?query="+urllib.parse.quote(json.dumps(queryParamters))
                response = requests.get(url=endPoint,headers=self.headers)
                
        
        except Exception as e:
            print(e)

        return results
        # try:    
        #     results = json.loads(response.content)
        #     return results
        # except Exception as e:
        #     print(e)
        

    def url_encode_string(inputString):
        output = urllib.parse.quote(inputString)
        return output
        
