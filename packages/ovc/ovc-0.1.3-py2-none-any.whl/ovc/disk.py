from .client import Client

import jwt
import requests

class Disk(object):
    def __init__(self, url, headers={}):
        self.url = url
        self.headers = headers
        self.msg = None
    
    def check_existence(self, machine_details, disk_name):
        """
        Returns disk information
        """
        disks = machine_details['disks']
        for disk in disks:
            if disk['name'] == disk_name:
                return disk['id']
        return None

    def add(self, machine_id, disk_name, disk_description, disk_size,
            disk_type, ssd_size, disk_iops):
        """
        Updates size ID
        """
        body_data = {}
        body_data['machineId'] = machine_id
        body_data['diskName'] = disk_name
        body_data['description'] = disk_description
        body_data['size'] = disk_size
        body_data['type'] = disk_type
        body_data['ssdSize'] = ssd_size
        body_data['iops'] = disk_iops
        response = requests.post(self.url + '/cloudapi/machines/addDisk', json=body_data, headers=self.headers)
        return Client.check_response(response)
    
    def delete(self, disk_id):
        """
        Deletes disk
        """
        body_data = {}
        body_data['diskId'] = disk_id
        body_data['detach'] = True
        body_data['permanently'] = True
        response = requests.post(self.url + '/cloudapi/disks/delete', json=body_data, headers=self.headers)
        return Client.check_response(response)

    def get(self, disk_id):
        """
        Get all the information regarding the added or deleted disk
        """
        body_data = {}
        body_data['diskId'] = disk_id
        response = requests.post(self.url + '/cloudapi/disks/get', json=body_data, headers=self.headers)
        return Client.check_response(response).json()
