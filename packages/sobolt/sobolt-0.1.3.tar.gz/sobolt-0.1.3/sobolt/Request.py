import json
import requests


class Request:
    TERRAVISIE = "https://vizi.ai/terravisie"
    
    api_key = None
    service = None


    def __init__(self, api_key, service = None):
        if service == None:
            service = Request.TERRAVISIE
        
        if api_key == None:
            raise ValueError("api_key == None but an API key must be supplied")
        
        self.api_key = api_key
        self.service = service


    # The method do_request performs an HTTP request to Sobolt's servers, submitting a list of image
    # urls to be analysed. The return value is either a dictionary of the parsed JSON values,
    # or the raw JSON text if the parse parameter was set to False.
    # In:  A list of images conforming to the specifications of the called API function 
    # In:  Optionally, the url of the request can be 
    # Out: JSON text
    # Exception: Might raise exceptions for incorrect JSON or failed HTTP requests
    def do_request(self, imgs, parse=True):
        if len(imgs) == 0:
            msg = "Request must send data to be analyzed. Parameter imgs' length == 0"
            raise ValueError(msg)
    
        json_response = self.do_request_get_response(imgs)
        
        if json_response.status_code == 200:
            if parse:
                return json_response.json()
            else:
                return json_response.text
        else:
            json_response.raise_for_status()
    

    # The method do_request_get_response performs an HTTP request to Sobolt's servers,
    # submitting a list of image urls to be analysed, without doing any further processing.
    # The return value is the response object as the requests module returns.
    def do_request_get_response(self, imgs):
        data = json.dumps({ "signature_name": "serving_default",
                            "api_key": self.api_key,
                            "instances": imgs })
        headers = { "Content-Type": "application/json" }
        json_response = requests.post(self.service,
                                      data=data, 
                                      headers=headers)

        json_response.close()
        return json_response
