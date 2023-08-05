from .client import Client

import jwt
import requests

class Portforwarding(object):
    def __init__(self, url, headers={}):
        self.url = url
        self.headers = headers
        self.msg = None
    
    def create(self, machine_id, public_ip, cloudspace_id, public_port, local_port, protocol):
        """
        Creates new port forwarding
        """
        body_data = {}
        body_data['cloudspaceId'] = cloudspace_id
        body_data['machineId'] = machine_id
        body_data['publicIp'] = public_ip
        body_data['publicPort'] = public_port
        body_data['localPort'] = local_port
        body_data['protocol'] = protocol
        response = requests.post(self.url + '/cloudapi/portforwarding/create', json=body_data, headers=self.headers)
        return Client.check_response(response)
    
    def check_existence(self, machine_id, cloudspace_id, local_port, public_port):
        """
        Checks if port forwarding exists
        """
        ports = self.list(machine_id=machine_id, cloudspace_id=cloudspace_id)
        for port in ports:
            if port['localPort'] == str(local_port) and port['publicPort'] == str(public_port):
                return True
        return False
    
    def delete(self, machine_id, public_ip, cloudspace_id, public_port, local_port, protocol):
        """
        Deletes a port forwarding
        """
        body_data = {}
        body_data['cloudspaceId'] = cloudspace_id
        body_data['machineId'] = machine_id
        body_data['publicIp'] = public_ip
        body_data['publicPort'] = public_port
        body_data['localPort'] = local_port
        body_data['protocol'] = protocol
        response = requests.post(self.url + '/cloudapi/portforwarding/deleteByPort', json=body_data, headers=self.headers)
        return Client.check_response(response)
    
    def list(self, machine_id, cloudspace_id):
        """
        Gets all relevant information of port forward
        """
        body_data = {}
        body_data['cloudspaceId'] = cloudspace_id
        body_data['machineId'] = machine_id
        response = requests.post(self.url + '/cloudapi/portforwarding/list', json=body_data, headers=self.headers)
        return Client.check_response(response).json()