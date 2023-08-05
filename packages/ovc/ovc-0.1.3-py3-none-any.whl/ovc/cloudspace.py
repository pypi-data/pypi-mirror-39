from .client import Client

import jwt
import requests

class Cloudspace(object):
    
    def __init__(self, url, headers={}):
        self.msg = None
        self.url = url
        self.headers = headers

    def check_existence(self, cloudspace_name):
        """
        Checks if cloudspace name exists
        returns the cloudspace ID if cloudspace exists
        """
        body_data = {}
        body_data['includedeleted'] = False
        response = requests.post(self.url + '/cloudapi/cloudspaces/list', json=body_data, headers=self.headers)
        cloudspaces = response.json()
        for cloudspace in cloudspaces:
            if cloudspace['name'] == cloudspace_name:
                cloudspace_id = cloudspace['id']
                return cloudspace_id
        return None

    def create(self, access, account_id, cloudspace_name, max_memory_capacity, 
            max_vdisk_capacity, max_cpu_capacity, max_network_peer_transfer, 
            max_num_public_ip):
        """
        Makes new cloudspace based on input values
        """
        body_data = {}
        body_data['accountId'] = account_id
        body_data['name'] = cloudspace_name
        body_data['location'] = self.get_location()
        body_data['access'] = access
        body_data['maxMemoryCapacity'] = max_memory_capacity
        body_data['maxVDiskCapacity'] = max_vdisk_capacity
        body_data['maxCPUCapacity'] = max_cpu_capacity
        body_data['maxNetworkPeerTransfer'] = max_network_peer_transfer
        body_data['maxNumPublicIP'] = max_num_public_ip
        response = requests.post(self.url + '/cloudapi/cloudspaces/create', json=body_data, headers=self.headers)
        return Client.check_response(response)

    def get(self, cloudspace_id):
        """
        Returns the cloudspace information
        """
        body_data = {}
        body_data['cloudspaceId'] = cloudspace_id
        response = requests.post(self.url + '/cloudapi/cloudspaces/get', json=body_data, headers=self.headers)
        return Client.check_response(response).json()

    def delete(self, cloudspace_id):
        """
        Deletes selected cloudspace
        """
        body_data = {}
        body_data['cloudspaceId'] = cloudspace_id
        body_data['permanently'] = True
        response = requests.post(self.url + '/cloudapi/cloudspaces/delete', json=body_data, headers=self.headers)
        return Client.check_response(response)

    def update(self, cloudspace_id, cloudspace_name, max_memory_capacity, max_cpu_capacity, max_network_peer_transfer, max_num_public_ip, 
            max_vdisk_capacity):
        """
        Updates selected cloudspace
        """
        body_data = {}
        body_data['cloudspaceId'] = cloudspace_id
        body_data['name'] = cloudspace_name
        body_data['maxMemoryCapacity'] = max_memory_capacity
        body_data['maxVDiskCapacity'] = max_vdisk_capacity
        body_data['maxCPUCapacity'] = max_cpu_capacity
        body_data['maxNetworkPeerTransfer'] = max_network_peer_transfer
        body_data['maxNumPublicIP'] = max_num_public_ip
        response = requests.post(self.url + '/cloudapi/cloudspaces/update', json=body_data, headers=self.headers)
        return Client.check_response(response)


    def get_location(self):
        res = self.url.split('://')
        return res[1].split('.', 1)[0]