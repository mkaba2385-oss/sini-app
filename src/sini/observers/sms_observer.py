from sini.observers.base import Event, Observer
from sini.services.sms import SmsGateway


class SmsNotificationObserver(Observer):
    """Observateur réagissant aux événements d'alerte en émettant un SMS."""

    def __init__(self, sms_gateway: SmsGateway) -> None:
        self.sms_gateway = sms_gateway

    def update(self, event: Event) -> None:
        if event.name == "ALERT_TRIGGERED":
            telephone = event.payload.get("telephone")
            message = event.payload.get("message")

            if isinstance(telephone, str) and isinstance(message, str):
                self.sms_gateway.send_sms(
                    telephone,
                    message,
                )
