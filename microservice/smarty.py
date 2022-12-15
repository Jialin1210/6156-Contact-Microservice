import requests
   
class Smarty:

    @staticmethod  
    def autocompleteAPI(inp):
        URL = "https://us-autocomplete-pro.api.smartystreets.com/lookup"
        
        auth_id = "4070fba4-036c-0f2d-aa09-b9ba9cceb8eb"
        token = "XdzuVVnBsOovBpJSZej8"
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