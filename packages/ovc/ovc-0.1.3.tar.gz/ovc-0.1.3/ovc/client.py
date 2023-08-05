import requests

class Client(object):

    @staticmethod
    def check_response(response):
        """
        Checks the API response
        """
        if response.status_code in range(200, 299):
            return response
        else:
            raise DoError(response.text)

    @staticmethod
    def first_login(client_id, client_secret):
        """
        First login to get token
        """
        auth_data = {}
        auth_data['grant_type']= 'client_credentials'
        auth_data['client_id'] = str(client_id)
        auth_data['client_secret'] = str(client_secret)
        auth_data['response_type'] = 'id_token'

        response = requests.post('https://itsyou.online/v1/oauth/access_token', data=auth_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        return response.text

class DoError(RuntimeError):
    pass