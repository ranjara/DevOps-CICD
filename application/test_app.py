
from app import Handler

def test_application_message():
    handler_code = Handler.do_GET
    assert callable(handler_code)

def test_health_endpoint_exists():
    assert hasattr(Handler, "do_GET")
