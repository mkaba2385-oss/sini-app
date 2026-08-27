from unittest.mock import Mock, patch

from sini.providers.africa_talking import AfricaTalkingSmsGateway


@patch("sini.providers.africa_talking.africastalking")
def test_send_sms_returns_true(
    mock_africastalking: Mock,
) -> None:
    mock_sms = Mock()
    mock_africastalking.SMS = mock_sms

    gateway = AfricaTalkingSmsGateway(
        username="sandbox",
        api_key="fake-api-key",
    )

    mock_sms.send.return_value = {
        "SMSMessageData": {
            "Recipients": [
                {
                    "status": "Success",
                }
            ]
        }
    }

    result = gateway.send_sms(
        "+22370000000",
        "Bonjour depuis Sini",
    )

    assert result is True

    mock_africastalking.initialize.assert_called_once_with(
        username="sandbox",
        api_key="fake-api-key",
    )

    mock_sms.send.assert_called_once_with(
        "Bonjour depuis Sini",
        ["+22370000000"],
    )
