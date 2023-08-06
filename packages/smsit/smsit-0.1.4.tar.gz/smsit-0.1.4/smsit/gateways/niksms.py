
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
    _server_url = 'https://niksms.com/fa/PublicApi'

    _send_status_map = {
        1: 'Successful',
        2: 'UnknownError',
        3: 'InsufficientCredit',
        4: 'ForbiddenHours',
        5: 'Filtered',
        6: 'NoFilters',
        7: 'PrivateNumberIsDisable',
        8: 'ArgumentIsNullOrIncorrect',
        9: 'MessageBodyIsNullOrEmpty',
        10: 'PrivateNumberIsIncorrect',
        11: 'ReceptionNumberIsIncorrect',
        12: 'SentTypeIsIncorrect',
        13: 'Warning',
        14: 'PanelIsBlocked',
        15: 'SiteUpdating',
        16: 'AudioMessageNotAllowed',
        17: 'AudioMessageFileSizeNotAllowed',
        18: 'PanelExpired',
        19: 'InvalidUserNameOrPass'
    }

    def send(self, sms):
        params = {
            'Username': self.config['username'],
            'Password': self.config['password'],
            'Message': sms.text,
            'Numbers': sms.receiver,
            'SenderNumber': sms.sender or self.config['sender'],
            'SendType': 1  # 1: Normal | 2: Flash
        }

        try:
            result = request(
                'POST', '%s/GroupSms' % self._server_url,
                params=params
            ).json()

            if int(result['Status']) != 1:
                raise SMSGatewayError(result['WarningMessage'])

        except RequestException:
            raise SMSGatewayError('Cannot send SMS')

        except Exception:
            raise SMSGatewayError('Bad SMS gateway')

        return True
