from .sms import SMS


class SMSGateway:
    __gateway_name__ = ''
    __config_params__ = []
    config = None

    def __init__(self, config: dict):  # pragma: nocover
        self.config = config

    def send(self, sms: SMS):  # pragma: nocover
        raise NotImplementedError
