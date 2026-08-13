from abc import ABC, abstractmethod


class SmsGateway(ABC):
    @abstractmethod
    def send_sms(self, telephone: str, message: str) -> bool:
        pass


class ConsoleSmsGateway(SmsGateway):
    def send_sms(self, telephone: str, message: str) -> bool:
        print(f"[SMS STUB -> {telephone}] : {message}")
        return True
