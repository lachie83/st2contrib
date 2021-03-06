from lib.actions import SingleVMAction

__all__ = [
    'ListVMsAction'
]

NODE_ATTRIBUTES = [
    'id',
    'name',
    'state',
    'public_ips',
    'private_ips'
]


class ListVMsAction(SingleVMAction):
    description = 'List VMs'

    def run(self, credentials):
        driver = self._get_driver_for_credentials(credentials=credentials)
        vms = driver.list_nodes()
        result = []

        for vm in vms:
            values = vm.__dict__
            item = dict([(k, v) for k, v in values.items()
                         if k in NODE_ATTRIBUTES])
            result.append(item)

        return result
