
from requests import request
from requests.exceptions import RequestException

from smsit import SMSGateway, SMSGatewayError


class SMSMagicGateway(SMSGateway):
    """
    SMS-Magic

    Documentation: https://api.sms-magic.com/doc/#api-Send_SMS-Send_SMS___get
    """
    __gateway_name__ = 'sms_magic'
    __config_params__ = ('api_key', 'sender_id')
    _server_url = 'https://api.sms-magic.com/v1/sms/send'

    def send(self, sms):
        payload = {
            'sms_list': []
        }
        for receiver in sms.receiver:
            payload['sms_list'].append({
                'mobile_number': receiver,
                'sms_text': sms.text,
                'sender_id': sms.sender or self.config['sender_id']
            })

        headers = {
            'apiKey': self.config['api_key'],
        }

        try:
            request('GET', self._server_url, headers=headers, params=payload)

        except RequestException:
            raise SMSGatewayError('Cannot send SMS')

        return True
