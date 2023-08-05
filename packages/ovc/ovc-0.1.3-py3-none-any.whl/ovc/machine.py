from .client import Client

import jwt
import requests

class Machine(object):
    def __init__(self, url, headers={}):
        self.msg = None
        self.url = url
        self.headers = headers

    def check_existence(self, cloudspace_id, machine_name):
        """
        Checks if machine name exists
        returns the machine ID if machine exists
        """
        body_data = {}
        body_data['cloudspaceId'] = cloudspace_id
        response = requests.post(self.url + '/cloudapi/machines/list', json=body_data, headers=self.headers)
        machines = response.json()
        for machine in machines:
            if machine['name'] == machine_name:
                return machine['id']
        return None
    
    def create(self, cloudspace_id, machine_name, description, 
            size_id, image_id, disk_size, data_disks, vcpus, memory):
        """
        Makes new machine based on input values
        """
        body_data = {}
        body_data['cloudspaceId'] = cloudspace_id
        body_data['name'] = machine_name
        body_data['description'] = description
        body_data['imageId'] = image_id
        if size_id is not None:
            body_data['sizeId'] = size_id
        else:
            body_data['vcpus'] = vcpus
            body_data['memory'] = memory
        body_data['disksize'] = disk_size
        body_data['datadisks'] = data_disks
        response = requests.post(self.url + '/cloudapi/machines/create', json=body_data, headers=self.headers)
        return Client.check_response(response)

    def get(self, machine_id):
        """
        Returns the machine information
        """
        body_data = {}
        body_data['machineId'] = machine_id
        response = requests.post(self.url + '/cloudapi/machines/get', json=body_data, headers=self.headers)
        return Client.check_response(response).json()
    
    def delete(self, machine_id):
        """
        Removes selected machine
        """
        body_data = {}
        body_data['machineId'] = machine_id
        body_data['permanently'] = True
        response = requests.post(self.url + '/cloudapi/machines/delete', json=body_data, headers=self.headers)
        return Client.check_response(response)

    def update(self, machine_id, machine_name, description, size_id, vcpus, memory):
        """
        Updates the machine
        """
        body_data = {}
        body_data['machineId'] = machine_id
        body_data['name'] = machine_name
        body_data['description'] = description
        self.update_size(machine_id, size_id, vcpus=vcpus, memory=memory)
        response = requests.post(self.url + '/cloudapi/machines/update', json=body_data, headers=self.headers)
        return Client.check_response(response)

    def update_size(self, machine_id, size_id, vcpus, memory):
        """
        Update the machine's size
        """
        body_data = {}
        if size_id is not None:
            body_data['sizeId'] = size_id
        else:
            body_data['vcpus'] = vcpus
            body_data['memory'] = memory
        body_data['machineId'] = machine_id
        response = requests.post(self.url + '/cloudapi/machines/resize', json=body_data, headers=self.headers)
        return Client.check_response(response)

