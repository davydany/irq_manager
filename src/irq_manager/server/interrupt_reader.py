import os

from .constants import PATH_TO_INTERRUPTS
from .exceptions import UnableToStart


class InterruptReader(object):

    def __init__(self, interrupt_file=None):

        if interrupt_file == None:
            if not os.path.exists(PATH_TO_INTERRUPTS):
                raise UnableToStart("Unable to start Poller because Interrupts file (%s) does not exist." % PATH_TO_INTERRUPTS)

    def _load_interrupt_file(self):

        with open(PATH_TO_INTERRUPTS) as interrupt_file:
            contents = interrupt_file.read().strip()
            return contents.split('\n')

    def _get_cpu_count(self, line):

        return len(line.split())

    def _parse_interrupt_line(self, line, cpu_count):
        '''
        Parses a non-header line of a proc file.

        Source: https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/deployment_guide/s2-proc-interrupts
        NOTE: This 
        '''
        line_split = line.split()
        line_size = len(line_split)

        # The first column refers to the IRQ number. 
        try:
            irq_no = int(line_split[0][0:-1])
        except ValueError:
            return

        # Each CPU in the system has its own column and 
        # its own number of interrupts per IRQ.
        cpu_interrupts = {}
        for i in range(1, cpu_count + 1):
            cpu_interrupts[str(i-1)] = int(line_split[i])
        
        # The next column reports the type of interrupt
        interrupt_type = line_split[cpu_count + 1]

        # the last column contains the name of the device that is located at that IRQ
        device_name = line_split[-1]

        return (irq_no, cpu_interrupts, interrupt_type, device_name)

    def get_cpu_count(self):
        '''
        Gets CPU Count without passing any other parameters.
        '''
        contents = self._load_interrupt_file()
        header = contents[0]
        return self._get_cpu_count(header)

    def extract_interrupts(self):

        contents = self._load_interrupt_file()
        cpu_count = self._get_cpu_count(contents[0])
        interrupts = []

        # load each line and parse it
        for line in contents[1:]:
            interrupts.append(
                self._parse_interrupt_line(line, cpu_count)
            )
        return interrupts
            
    def get_irq_for_device(self, device):

        for interrupt in self.extract_interrupts():

            if interrupt:
                irq_no, cpu_interrupts, interrupt_type, device_name = interrupt
                if device_name == device:
                    return irq_no
        
    def set_affinity(self, irq, cpu_affinity):

        path_to_irq_smp_affinity = '/proc/irq/{irq}/smp_affinity'.format(irq=irq)
        with open(path_to_irq_smp_affinity, 'w') as f:
            f.write(cpu_affinity)

    def get_affinity(self, irq):
        
        path_to_irq_smp_affinity = '/proc/irq/{irq}/smp_affinity'.format(irq=irq)
        with open(path_to_irq_smp_affinity) as f:
            return f.read().strip()