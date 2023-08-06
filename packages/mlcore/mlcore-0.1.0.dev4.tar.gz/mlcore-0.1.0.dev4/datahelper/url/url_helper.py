import requests
import json
import configparser

class URLHelper():
    def __init__(
        self,
        logger=None,
        config_file='go_servers.ini',
        host_name='DataPlatform_DEV_API'):
        self.logger = logger
        self.config_file = config_file
        self.host_name = host_name

    def get_cipher(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

        refresh_url = self.config[self.host_name]['refresh_url']
        r = requests.get(refresh_url)
        lines = str(r.content).split('\\n')
        lines = [x.strip().replace('<td>','').replace('</td>','') for x in lines]
        ind = lines.index(self.config[self.host_name]['account'])
        return lines[ind+1]


    def post_json(self, url, json_obj, json_option=None):
        self.cipher = self.get_cipher()
        headers = {
                'Go-Client':'stage',
                'Authorization':'Bearer {}'.format(self.cipher),
            }
        r = requests.post(url, headers=headers, json=json_obj)
        if json_option is None:
            json_option = {}
        return json.loads(r.content.decode('utf-8'),**json_option)
