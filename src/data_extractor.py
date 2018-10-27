import time
import json
import requests


class DataExtractor(object):

    def __init__(self, *args, **kwargs):
        self._pro_matches_url = 'https://api.opendota.com/api/proMatches'
        self._match_url = 'https://api.opendota.com/api/matches/{match_id}'

    def extract_pro_matches_from_api(self, match_id=None):

        pro_matches_url = self._pro_matches_url

        if match_id is not None:
            params = {'less_than_match_id': match_id}
            print('Pulling pro matches with match_id less than', match_id)
        else:
            params = None
            print('Pulling latest pro matches.')

        resp = requests.get(pro_matches_url, params=params)

        time.sleep(1.0)

        while resp.status_code != 200:
            time.sleep(30.0)
            print('Querying pro matches less than match id', match_id,
                  'is failing', 'with status code', resp.status_code)
            resp = requests.get(pro_matches_url)

        resp = json.loads(resp.text)
        return resp

    def extract_match_data_from_api(self, match_id):
        match_url = self._match_url.format(match_id=match_id)
        print('Querying match', match_id, 'data')

        resp = requests.get(match_url)

        time.sleep(1.0)

        while resp.status_code != 200:
            time.sleep(30.0)
            print('Querying Match id', match_id, 'is failing',
                  'with status code', resp.status_code)
            resp = requests.get(match_url)

        resp = json.loads(resp.text)
        return resp

    def extract_pro_matches_from_local(self):
        raise NotImplementedError

    def extract_match_data_from_local(self):
        raise NotImplementedError
