import datetime
import mongoengine as mongo

from mongoengine.queryset.visitor import Q
from .constants import PATH_TO_INTERRUPTS
from .exceptions import UnableToStart, Http404

def now():

    return datetime.datetime.utcnow()

class InterruptRequestQueryset(mongo.QuerySet):

    def get_unique_devices(self):

        return self.distinct('device')

    def get_irq_for_device(self, device):

        all_devices = self.get_unique_devices()
        if device not in all_devices:
            raise Http404()
            
        return self.filter(device=device)

    def get_irq_for_device_with_filters(self, device, start_dt, end_dt):

        all_devices = self.get_unique_devices()
        if device not in all_devices:
            raise Http404()

        if start_dt and end_dt:
            return self.filter(
                Q(device=device) & \
                Q(created_at__gte=start_dt) & \
                Q(created_at__lte=end_dt))
        else:
            return self.get_irq_for_device(device)

class InterruptRequest(mongo.Document):

    meta = {
        'queryset_class': InterruptRequestQueryset
    }

    irq_no = mongo.IntField(db_index=True, required=True)
    cpu_interrupts = mongo.DictField(required=True)
    interrupt_type = mongo.StringField(required=True)
    device = mongo.StringField(db_index=True, required=True)

    created_at = mongo.DateTimeField(required=True, default=now)

    def as_dict(self):

        return {
            'irq_no': self.irq_no,
            'cpu_interrupts': self.cpu_interrupts,
            'interrupt_type': self.interrupt_type,
            'device': self.device,
            'created_at': self.created_at
        }

    
