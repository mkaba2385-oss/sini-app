from sini.services.otp_service import OtpService


def test_generate_code_has_six_digits() -> None:
    service = OtpService()

    code = service.generate_code()

    assert len(code) == 6
    assert code.isdigit()


def test_create_otp_returns_code() -> None:
    service = OtpService()

    code = service.create_otp("+22370000000")

    assert len(code) == 6
    assert code.isdigit()


def test_verify_valid_otp() -> None:
    service = OtpService()

    phone_number = "+22370000000"
    code = service.create_otp(phone_number)

    result = service.verify_otp(phone_number, code)

    assert result is True


def test_verify_invalid_code() -> None:
    service = OtpService()

    phone_number = "+22370000000"
    code = service.create_otp(phone_number)

    invalid_code = "000000" if code != "000000" else "111111"

    result = service.verify_otp(
        phone_number,
        invalid_code,
    )

    assert result is False


def test_otp_can_only_be_used_once() -> None:
    service = OtpService()

    phone_number = "+22370000000"
    code = service.create_otp(phone_number)

    first_result = service.verify_otp(
        phone_number,
        code,
    )

    second_result = service.verify_otp(
        phone_number,
        code,
    )

    assert first_result is True
    assert second_result is False


def test_verify_expired_otp() -> None:
    service = OtpService()

    phone_number = "+22370000000"

    service.create_otp(
        phone_number,
        expires_in_minutes=-1,
    )

    code = service._otps[phone_number][0]

    result = service.verify_otp(
        phone_number,
        code,
    )

    assert result is False
