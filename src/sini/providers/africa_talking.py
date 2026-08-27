import africastalking  # type: ignore[import-untyped]

from sini.services.sms import SmsGateway


class AfricaTalkingSmsGateway(SmsGateway):
    """Gateway SMS utilisant Africa's Talking."""

    def __init__(
        self,
        username: str,
        api_key: str,
    ) -> None:
        africastalking.initialize(
            username=username,
            api_key=api_key,
        )

        self.sms = africastalking.SMS

    def send_sms(
        self,
        telephone: str,
        message: str,
    ) -> bool:
        self.sms.send(
            message,
            [telephone],
        )

        return True
