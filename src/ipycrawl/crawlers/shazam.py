# -*- coding: utf-8 -*-

# pip install shazamio


import requests

url = "https://shazam.p.rapidapi.com/auto-complete"

querystring = {"term":"kiss the","locale":"en-US"}

headers = {
    'x-rapidapi-host': "shazam.p.rapidapi.com",
    'x-rapidapi-key': "8c0dfe8daamsh2f5235df6e2a05dp1268f8jsnc0ee65f8f42c"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
