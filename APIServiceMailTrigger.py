#!/usr/bin/python3.8

import json
from socket import timeout
import requests


from mailFn import mail_notification


# Service Specific Health Check
def dockerComposeServiceHealthCheckFn():
    # servicename, container_name, url
    servicedata = ''
    body = []
    with open("./apiservicedata.json") as f:
        data = json.load(f)
        for service in data:
            try:
                servicedata = data[service]
                urlresponse = requests.get(servicedata['url'], timeout=1)
                datanew = urlresponse.json()
                servicedata['message'] = datanew['message']
                servicedata['statusCode'] = datanew['statusCode']
                body.append(servicedata)
            except:
                servicedata['message'] = 'Container is down'
                servicedata['statusCode'] = 500
                body.append(servicedata)
        mail_notification(body)


if __name__ == '__main__':
    dockerComposeServiceHealthCheckFn()
