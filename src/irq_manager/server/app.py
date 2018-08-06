from flask import Flask, jsonify

from .constants import PATH_TO_INTERRUPTS
from .exceptions import UnableToStart
from .models import ICQ

app = Flask('irq_manager_server')


class ICQService(object):

    def __init__(self, host, port);

        if not os.path.exist(PATH_TO_INTERRUPTS):
            raise UnableToStart("'%s' does not exist, and so this service cannot start." % (PATH_TO_INTERRUPTS))
        
        self.host = host
        self.port = port

    def configure(self):


        @app.route('/')
        def list_icr():

            return jsonify({
                'icq': 1234
            })