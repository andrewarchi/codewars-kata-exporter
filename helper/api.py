import json
import requests


class CodeWarsAPI:
    def __init__(self, token):
        self.token = token

    def get_kata(self, kata_id):
        endpoint = 'https://www.codewars.com/api/v1/code-challenges/{}'.format(kata_id)
        res = requests.get(endpoint, params={'Authorization': self.token})
        data = json.loads(res.text)
        return data['name'].strip(), data['slug'], data['url'], data['description']
