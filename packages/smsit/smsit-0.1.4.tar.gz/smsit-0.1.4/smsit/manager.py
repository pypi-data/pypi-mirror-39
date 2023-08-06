from typing import Type

from smsit import SMSGateway, SMS


class SMSGatewayManager:
    _config = dict()
    _gateways = dict()

    def register(self, alias, gateway: Type[SMSGateway]):
        self._gateways[alias] = gateway
        return self

    def configure(self, config):
        for alias, config in config.items():
            if alias in self._gateways:
                self._gateways[alias] = \
                    self._gateways[alias](config=config)
            else:
                raise ValueError('Gateway %s not registered.' % alias)
        return self

    def get_gateway(self, alias) -> SMSGateway:
        return self._gateways[alias]

    def send(self, alias: str, sms: SMS) -> bool:
        return self.get_gateway(alias).send(sms)
