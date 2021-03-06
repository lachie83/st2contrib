import time

from lib.sensorbase import EC2ConnectMixin


class EC2InstanceStatusSensor(EC2ConnectMixin):
    def __init__(self, container_service, config=None):
        super(EC2InstanceStatusSensor, self).__init__(config)
        self._container_service = container_service
        self._interval = config.get('interval', 20)
        self._trigger_name = 'instance_status'
        self._trigger_pack = 'aws'
        self._trigger_ref = '.'.join([self._trigger_name, self._trigger_pack])

    def start(self):
        while True:
            data = self._ec2.get_instance_details()
            for i in data:
                trigger = self._trigger_ref
                payload = data[i]
                payload['event_id'] = 'ec2-instance-check-' + str(int(time.time()))
                payload['instance_id'] = i
                try:
                    self._container_service.dispatch(trigger, payload)
                except Exception as e:
                    self._log.exception('Exception %s handling st2.ec2.instance_status', e)
            time.sleep(self._interval)

    def get_trigger_types(self):
        return [
            {
                'name': self._trigger_name,
                'pack': self._trigger_pack,
                'description': 'EC2 Instance Status Sensor',
                'payload_schema': {
                    'type': 'object',
                    'properties': {
                        'instance_id': {},
                        'instance_type': {},
                        'launch_time': {},
                        'tags': {},
                        'image_id': {},
                        'ip_address': {},
                        'state': {},
                        'state_code': {}
                    }
                }
            }
        ]
