from app.services.pii_service import mask_pii


def test_mask_email():
    result = mask_pii("Contact test@example.com")
    assert "[EMAIL]" in result
    assert "test@example.com" not in result


def test_mask_phone():
    result = mask_pii("Call 9876543210")
    assert "[PHONE]" in result
    assert "9876543210" not in result


def test_mask_id():
    result = mask_pii("ID 123456789012")
    assert "[ID]" in result
    assert "123456789012" not in result
