import click
import datetime
import time

from .constants import PATH_TO_INTERRUPTS
from .exceptions import UnableToStart
from .models import InterruptRequest
from .interrupt_reader import InterruptReader

class Poller(object):

    def __init__(self):

        self.reader = InterruptReader()
        
    def poll(self, interval_secs):

        while True:

            click.secho("Polling '%s' for new data at %s" % (PATH_TO_INTERRUPTS, datetime.datetime.utcnow().isoformat()), fg='green')
            for interrupt in self.reader.extract_interrupts():

                if interrupt:
                    irq_no, cpu_interrupts, interrupt_type, device_name = interrupt
                    irq = InterruptRequest(
                        irq_no=irq_no,
                        cpu_interrupts=cpu_interrupts,
                        interrupt_type=interrupt_type,
                        device=device_name
                    )
                    irq.save()

            click.secho('Sleeping for %s seconds' % (interval_secs), fg='magenta')
            time.sleep(int(interval_secs))
