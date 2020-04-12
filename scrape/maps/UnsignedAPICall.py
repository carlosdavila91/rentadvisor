
# By Carlos Davila

import requests, json
from pandas.io.json import json_normalize

# api_url = "https://directa.carto.com:443/api/v2/sql?q=select * from public.fonsinversi_edificisbcn"

class UnsignedAPICall:
    """
    Simple API. Feed an API URL and get an object with:
    - json: json object, which is printed “nicely” formatted if requested
    - data_frame: the data parsed to data_frame
    """

    def __init__(self, api_url):
        self.api_url = api_url

        # Get the server response
        response = requests.get(api_url)
        self.json_dict = response.json()

    def main_keys(self):
        """Return a list of main keys in the json from the API"""
        keys_level_0 = response.json_dict.keys()
        return list(keys_level_0)

    def json_formatted(self):
        """Return the json object printed "nicely"""
        json_formatted = json.dumps(self.json_dict,
                            ensure_ascii=False, sort_keys=True, indent=2)
        return json_formatted

    """TODO: add a method to extract data frame from the response"""
    # def data_frame(self, key_index):
    #     """Parse data inside the desired key to data frame"""
    #
    #     # Get the string of the desired key
    #     key_str = response.main_keys()[key_index]
    #     # Transform response to dict to get a python usable structure
    #     dict = json.loads(response)
    #     data_frame = json_normalize(dict[key_str])
    #     return data_frame


# Usage
# Get the response
# response = UnsignedAPICall(api_url)

# To explore the full json object
# print(response.json_formatted())

# To get the main keys, i.e. level 0 keys
# print(responses.main_keys())

# To get a data frame from the response
# records = response["rows"]
# data_frame = json_normalize(records)
# print(data_frame.head(10))
