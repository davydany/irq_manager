import os

from flask import Flask, jsonify, request, abort

from irq_manager.constants import DEFAULT_DATE_TIME_FORMAT
from .constants import PATH_TO_INTERRUPTS
from .exceptions import UnableToStart, Http404
from .interrupt_reader import InterruptReader
from .models import InterruptRequest

app = Flask('irq_service')

class IRQService(object):

    def __init__(self, host, port):

        if not os.path.exists(PATH_TO_INTERRUPTS):
            raise UnableToStart("'%s' does not exist, and so this service cannot start." % (PATH_TO_INTERRUPTS))
        
        self.host = host
        self.port = port

    def response(self, data):

        response = jsonify(data)
        return response

    def configure(self):

        @app.route("/devices")
        def list_devices():
            
            devices = [d for d in InterruptRequest.objects.get_unique_devices()]
            return self.response({
                'devices': devices 
            })

        @app.route('/cpu_count')
        def cpu_count():

            reader = InterruptReader()
            cpu_count = reader.get_cpu_count()
            return self.response({
                'cpu_count': cpu_count
            })

        @app.route("/devices/<device>/")
        def device_detail(device):
            '''
            Returns Interrupt Details for a given device. Provide query parameters
            'start_dt' and 'end_dt' in the format 'YYYYMMDD-HHMMSS' to filter 
            results based on the time stamps.
            '''
            start_dt = request.args.get('start_dt')
            end_dt = request.args.get('end_dt')

            try:
                details = []
                if start_dt and end_dt:
                    for d in InterruptRequest.objects.get_irq_for_device_with_filters(device, start_dt, end_dt):
                        details.append(d.as_dict())
                else:
                    for d in InterruptRequest.objects.get_irq_for_device(device):
                        details.append(d.as_dict())
                    
                return self.response(details)
            except Http404:
                return abort(404)

        @app.route("/devices/<device>/affinity/", methods=['GET', 'POST'])
        def cpu_affinity(device):
            '''
            Gets and Sets the CPU Affinity for the provided device.
            '''
            reader = InterruptReader()
            irq = reader.get_irq_for_device(device)
            if irq and request.method == 'POST':
                affinity = request.form['affinity']
                reader.set_affinity(irq, affinity)

            affinity = reader.get_affinity(irq)
            return self.response({
                'affinity': affinity
            })


        return app

    def run(self):

        app.run(self.host, self.port)