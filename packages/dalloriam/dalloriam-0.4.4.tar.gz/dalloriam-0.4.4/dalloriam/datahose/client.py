import json
import requests
import os


DATAHOSE_CONFIG_PATH = os.path.expanduser('~/.config/dalloriam/datahose.json')


class DatahoseClient:

    """
    The DatahoseClient allows for easy interfacing with the cloud datahose.
    """

    def __init__(self, service_host: str = None, password: str = None) -> None:
        """
        Constructor
        Args:
            service_host (Optional[str]): Datahose endpoint
            password (Optional[str]): Datahose password.
        """
        if not (service_host and password):
            cfg_dict = self._try_get_disk_config()

            if not service_host:
                if 'service_host' not in cfg_dict:
                    raise ValueError(
                        f'Missing service_host, either in params or in config file ([{DATAHOSE_CONFIG_PATH}]).'
                    )
                service_host = cfg_dict['service_host']

            if not password:
                if 'password' not in cfg_dict:
                    raise ValueError(
                        f'Missing password, either in params or in config file ([{DATAHOSE_CONFIG_PATH}]).'
                    )
                password = cfg_dict['password']

        self._push_url = service_host

        self._headers = {
            'Authorization': password
        }

    @staticmethod
    def _try_get_disk_config() -> dict:
        if os.path.isfile(DATAHOSE_CONFIG_PATH):
            with open(DATAHOSE_CONFIG_PATH, 'r') as infile:
                return json.load(infile)
        return {}

    def push(self, key: str, data: dict, time: float = None) -> None:
        """
        Push an event to the datahose.
        Args:
            key (str): The event key.
            data (dict): The event data.
            time (float): The time at which the event occured.
        """
        data = {
            'key': key,
            'body': data
        }
        if time is not None:
            data['time'] = time

        resp = requests.post(self._push_url, json=data, headers=self._headers)

        if resp.status_code != 200:
            raise ValueError(resp.text)

    def notify(self, sender: str, message: str) -> None:
        """
        Send a notification via the datahose.
        Args:
            sender (str): Sender of the notification.
            message (str): Markdown-formatted message to send.
        """
        data = {
            'sender': sender,
            'message': message
        }
        self.push('notification', data=data)
