import json

from requests import request
from requests.exceptions import RequestException

from smsit import SMSGateway, SMSGatewayError


class NikSMSGateway(SMSGateway):
    """
    NikSMS

    Documentation:
        https://niksms.com/fa/main/امکانات-برنامه-نویسی-نیک-اس-ام-اس/Web-Service-API-چیست

    """
    __gateway_name__ = 'niksms'
    __config_params__ = ('username', 'password', 'sender')
    _server_url = 'https://niksms.com/fa/PublicApi/GroupSms'

    def send(self, sms):
        params = {
            'username': self.config['username'],
            'password': self.config['password'],
            'message': sms.text,
            'numbers': sms.receiver,
            'senderNumber': sms.sender or self.config['sender'],
            'sendType': 1
        }

        try:
            result = request('POST', self._server_url, params=params)
            result = json.loads(result)

            if result['status'] != 'ok':
                raise SMSGatewayError(result['error'])

        except RequestException:
            raise SMSGatewayError('Cannot send SMS')

        return True
