import requests

class KarakeepAPI:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def search_bookmarks(self, query: str):
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        endpoint = f'{self.base_url}/api/v1/bookmarks/search'
        params = {'q': query}
        
        try:
            response = requests.get(endpoint, headers=headers, params=params)
        except requests.exceptions.RequestException as e:
            raise ConnectionError(e)
        
        if response.status_code == 200:
            return response.json().get('bookmarks')
        else:
            response.raise_for_status()
