SMSit
=====

A simple wrapper to send SMS through available gateways.


Gateways
--------

- `SMSMagic <https://sms-magic.com/>`_
- `NikSMS <https://niksms.com>`_


Install
-------

.. code-block:: bash

    pip install smsit

Usage
-----

Basic:

.. code-block:: python

    from smsit import SMS
    from smsit.gateways import SMSMagicGateway

    config = {
        'api_key': '0000',
        'sender_id': '1111'
    }
    sms = SMS(
        text='Hi',
        receiver='9893311223344'
    )

    SMSMagicGateway(config).send(sms)


With gateway manager:

.. code-block:: python

    from smsit import SMS, SMSGatewayManager
    from smsit.gateways import SMSMagicGateway, NikSMSGateway

    config = {
        'smsmagic': {
            'api_key': '0000',
            'sender_id': '1111'
        },
        'niksms': {
            'username': '0000',
            'password': '0000',
            'sender': '0000'
        }
    }
    sms = SMS(
        text='Hi',
        receiver='9893311223344'
    )

    manager = SMSGatewayManager()
    manager.register('smsmagic', SMSMagicGateway)
    manager.register('niksms', NikSMSGateway)
    manager.configure(config)
    manager.send('smsmagic', sms)
