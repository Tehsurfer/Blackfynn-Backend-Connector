import requests
import json
from blackfynn import Blackfynn

class BlackfynnConnect(object):

    def __init__(self, email, password, api_token=None, api_secret=None, session_token=None):
        self.email = email
        self.password = password
        self.session_token = session_token
        if session_token is None:
            self.status_code, self.session_token = self.get_session_token(email, password)
            # if self.status_code is 200 or 201 and api_token is None:
            #     self.status_code, self.api_token, self.api_secret = self.create_keys(self.session_token)



    def get_session_token(self, email, password):
        headers = {
            'Content-Type': 'application/json',
        }
        data = '{"email": "' + email + '" ,"password" : "' + password + '"}'
        response = requests.post('https://api.blackfynn.io/account/login', headers=headers, data=data)
        if response.status_code is 200 or 201:
            return (response.status_code, response.json()['sessionToken'] )
        else:
            print(response.status_code, response.content)
            return (response.status_code, response.content)

    def create_keys(self, session_token):
        headers = {
            'Content-Type': 'application/json',
        }
        params = ( ('api_key', self.session_token), )
        data = '{"name": "Auckland Biongineering Institute Apps Key"}'
        response = requests.post('https://api.blackfynn.io/token/', headers=headers, params=params, data=data)
        if response.status_code is 200 or 201:
            self.api_token = response.json()['key']
            self.api_secret = response.json()['secret']
            return (response.status_code, response.json()['key'], response.json()['secret'])
        else:
            print(response.status_code, response.content)
            return (response.status_code, response.content, None )
    
    def session_token_is_valid(self):
        headers = {
            'Content-Type': 'application/json',
        }
        params = (('api_key', self.session_token),)
        response = requests.post('https://api.blackfynn.io/user/', headers=headers, params=params)
        if response.status_code is 200 or 201:
            print('Session token still valid')
            return True
        else:
            print(response.status_code, response.content)
            self.get_session_token(self.email,self.password)


    def get_dataset_names(self):
        headers = {
            'Content-Type': 'application/json',
        }
        params = (('api_key', self.session_token),)
        response = requests.get('https://api.blackfynn.io/datasets/', headers=headers, params=params)
        if response.status_code is 200 or 201:
            dataset_names = []
            for dataset in response.json():
                dataset_names.append(dataset['content']['name'])


            return (response.status_code, json.dumps({'names': dataset_names}))
        else:
            print(response.status_code, response.content)
            return (response.status_code, response.content, None )
        
      def create_python_conection(self):
          self.bf = Blackfynn(api_token=self.api_token,api_secret=self.api_secret)
        


#     def get_datasets(self):
#
#         headers = {
#             'Content-Type': 'application/json',
#         }
#         params = (('api_key', self.session_token),)
#         response = requests.get('https://api.blackfynn.io/datasets/', headers=headers, params=params)
#         if response.status_code is 200 or 201:
#             return (response.status_code, response.json())
#         else:
#             print(response.status_code, response.content)
#             return (response.status_code, response.content, None)
#
#     def get_dataset(self, dataset_id):
#         headers = {
#             'Content-Type': 'application/json',
#         }
#         params = (('api_key', self.session_token),)
#         response = requests.get(f'https://api.blackfynn.io/datasets/{dataset_id}', headers=headers, params=params)
#         if response.status_code is 200 or 201:
#             return (response.status_code, response.json())
#         else:
#             print(response.status_code, response.content)
#             return (response.status_code, response.content, None)
#
#     def get_packages(self, dataset_id):
#         headers = {
#             'Content-Type': 'application/json',
#         }
#         params = (('api_key', self.session_token),)
#         response = requests.get(f'https://api.blackfynn.io/packages/{dataset_id}/files', headers=headers, params=params)
#         if response.status_code is 200 or 201:
#             return (response.status_code, response.json())
#         else:
#             print(response.status_code, response.content)
#             return (response.status_code, response.content, None)
#
#     def get_timeseries_items(self):
#         pass
#
#
#
#
#
#
#
#
#
#
#
# bf = BlackfynnConnect('jessekhorasanee@gmail.com', 'Asameswayhey6')
# dss = bf.get_datasets()
# for i,dsd in enumerate(dss[1]):
#     ds = bf.get_dataset(dsd['content']['id'])
#     for item in ds[1]['children']:
#         print(item['content']['packageType'])
#         if item['content']['packageType'] == 'Timseries':
#             print('found a timerseries set')
#
# pk = bf.get_packages(ds[1]['children'][0]['content']['id'])
#
# print(pk)
