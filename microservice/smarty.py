import requests
class Smarty:

    @staticmethod  
    def autocompleteAPI(inp):
        URL = "https://us-autocomplete-pro.api.smartystreets.com/lookup"
        
        auth_id = "YOUR AUTH-ID"
        token = "YOUR TOKEN"
        search = inp
        
        # defining a params dict for the parameters to be sent to the API
        PARAMS = {
            'search':search,
            'auth-id':auth_id,
            'auth-token':token
        }
        
        # sending get request and saving the response as response object
        r = requests.get(url = URL, params = PARAMS)
        
        # extracting data in json format
        data = r.json()
        return data