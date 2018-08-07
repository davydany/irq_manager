import requests

class URLManager(object):

    def __init__(self, host, port):

        self.host = host
        self.port = port

    def path(self, path):

        return 'http://{host}:{port}{path}'.format(
            host=self.host,
            port=self.port,
            path=path
        )

    def list_devices(self):

        return self.path('/devices')

    def cpu_count(self):

        return self.path('/cpu_count')

    def device_detail(self, device):

        return self.path('/devices/{device}/'.format(device=device))

    def cpu_affinity(self, device):

        return self.path('/devices/{device}/affinity/'.format(device=device))


class IRQClient(object):

    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.urls = URLManager(host, port)

    def list_devices(self):

        response = requests.get(self.urls.list_devices())
        if response.status_code == 200:
            return response.json().get('devices')

    def get_cpu_count(self):

        response = requests.get(self.urls.cpu_count())
        if response.status_code == 200:
            return response.json().get('cpu_count')

    def get_device_detail(self, device, start_dt=None, end_dt=None):

        url = self.urls.device_detail(device)
        if start_dt and end_dt:
            response = requests.get(url, params={
                'start_dt': start_dt,
                'end_dt': end_dt
            })
        else:
            response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()

    def get_cpu_affinity(self, device):

        response = requests.get(self.urls.cpu_affinity(device))
        if response.status_code == 200:
            return response.json().get('affinity')

    def set_cpu_affinity(self, device, affinity):

        response = requests.post(self.urls.cpu_affinity(device), data={
            'affinity': affinity
        })
        if response.status_code == 200:
            return response.json().get('affinity')