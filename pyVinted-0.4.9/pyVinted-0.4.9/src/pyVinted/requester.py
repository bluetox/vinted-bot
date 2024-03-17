import json
import requests
import re
import random
from requests.exceptions import HTTPError


#this is the base headers to be used in the first requests made to vinted to get the cookies
HEADERS = {
            "User-Agent": "PostmanRuntime/7.28.4",
            "Host": "www.vinted.fr",
}
#set max number of retries to 3
MAX_RETRIES = 3

#defines the requester
class Requester:


    def __init__(self):  #initiate's object under the __init__ name
        self.session = requests.Session() #gets the session
        self.session.headers.update(HEADERS) #updates current headers
        self.VINTED_AUTH_URL = f"https://www.vinted.fr/auth/token_refresh" #defines vinted authentication URL



    def get(self, url, params=None): #defines the get function takes an url and params as an option
        """
        Perform a http get request.
        :param url: str
        :param params: dict, optional
        :return: dict
            Json format
        """
        tried = 0 #sets tries to 0
        while tried < MAX_RETRIES: #tries function
            tried += 1 #adds 1 to tries
            with self.session.get(url, params=params) as response: #uses the session to send a GET request to specific URL with parameters as an option

                if response.status_code == 401 and tried < MAX_RETRIES: #checks for unauthorized access and number of tries
                    print(f"Cookies invalid retrying {tried}/{MAX_RETRIES}") #sends infos about the advancement of the cookie grabbing
                    self.setCookies() #uses the setcookie object to try to set cookies again

                elif response.status_code == 200 or tried == MAX_RETRIES: #checks for valid response from the server aka status code 200
                    return response #returns the response from the server


        return HTTPError #else if the number of tries is exceeded

    def post(self,url, params=None): #create an object to send a POST request to a URL with parameters as an option
        response = self.session.post(url, params) #POST's a request using the session data and saves it in a response variable
        response.raise_for_status() #raise for status means that it extracts the status code to see if the request is succesful
        return response #the object returns the response of the server

    def setCookies(self):#this object sets the cookies of the session


        self.session.cookies.clear_session_cookies()#clears previous session data


        try:

            self.post(self.VINTED_AUTH_URL) #sets cookies
            print("Cookies set!") #outputs success message

        except Exception as e: #if the cookies aren't set outputs error message
            print(
                f"There was an error fetching cookies for vinted\n Error : {e}"
            )


requester = Requester() #assign the class with no values to a variable