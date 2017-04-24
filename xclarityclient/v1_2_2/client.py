import json
import requests
from .power_status import power_status_list, power_status_action
from .boot_order import boot_order_priority


requests.packages.urllib3.disable_warnings()


class Client(object):
    def __init__(self, username=None, password=None,
                 version=None, url=None):

        self._version = version
        self._username = username
        self._password = password
        self._url = url[:-1] if url is not None and url[-1] == '/' \
            else url

    def _get_node_details(self, uuid):
        url = '{url}/node/{node_id}'.format(url=self._url, node_id=uuid)
        try:
            r = requests.get(url,
                             auth=(self._username, self._password),
                             verify=False,
                             timeout=(10, 10))
            result = {
                'status_code': r.status_code,
                'encoding': r.encoding,
                'headers': r.headers,
                'body': r.json()
            }
            return result
        except Exception as ex:
            print("Exception: {ex}".format(ex=ex))

    def get_node_status(self, uuid):
        response = self._get_node_details(uuid)
        if response['status_code'] == 200:
            return response['body']['accessState'].lower()
        else:
            return 'unknown'

    def get_node_power_status(self, uuid):
        response = self._get_node_details(uuid)
        if response['status_code'] == 200:
            return power_status_list[response['body']['powerStatus']]
        else:
            return 'unknown'

    def set_node_power_status(self, uuid, action):
        if action not in power_status_action:
            raise Exception('Bad Request: no such action: %s' % action)

        url = '{url}/node/{node_id}'.format(url=self._url, node_id=uuid)
        data = {'powerState': action}
        r = requests.put(url,
                         auth=(self._username, self._password),
                         data=json.dumps(data),
                         verify=False)

        if r.status_code != 200:
            raise Exception('Failed to set node %s power status %s'
                            % (uuid, action))

    def get_node_boot_info(self, uuid):
        response = self._get_node_details(uuid)
        if response['status_code'] == 200:
            boot_order_list = response['body']['bootOrder']['bootOrderList']

            for boot_order in boot_order_list:
                type_name = boot_order['bootType'].lower()
                for item in boot_order_priority:
                    if item['name'] == type_name:
                        item['value'] = boot_order

            final_boot_order = None
            for item in boot_order_priority:
                if item['value'] is not None:
                    final_boot_order = item['value']
                    break

            return final_boot_order

        else:
            return None
