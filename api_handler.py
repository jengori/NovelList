import requests

# The ApiHandler class is responsible for making calls to the New York Times Books API
class ApiHandler:

    def __init__(self, api_key: str):
        self.api_key = api_key

    def list_names_call(self):
        list_names_url = f"https://api.nytimes.com/svc/books/v3/lists/names.json?api-key={self.api_key}"
        list_names_response = requests.get(list_names_url)
        list_names_data = list_names_response.json()

        return list_names_data["results"]

    def lists_call(self, encoded_category: str, date: str):
        list_url = f"https://api.nytimes.com/svc/books/v3/lists/{date}/{encoded_category}.json?api-key={self.api_key}"
        list_response = requests.get(list_url)
        list_data = list_response.json()

        return list_data["results"]["books"]



