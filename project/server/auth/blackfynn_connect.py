import requests

class BlackfynnConnect(object):

    def __init__(self, email, password, api_token=None, api_secret=None):
        self.email = email
        self.password = password
        if api_token is None:
            self.status_code, self.session_token = self.get_session_token(email, password)
            if self.status_code is 200 or 201:
                self.status_code, self.api_token, self.api_secret = self.create_keys(self.session_token)



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
        params = ( ('api_key', '4bd923ad-924c-4dfc-b500-9ae9902802d8'), )
        data = '{"name": "Auckland Biongineering Institute Apps Key"}'
        response = requests.post('https://api.blackfynn.io/token/', headers=headers, params=params, data=data)
        if response.status_code is 200 or 201:
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
