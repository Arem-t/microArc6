import pytest

import delivery_service.delivery_service


def test_create_delivery(self):
    r = delivery_service.delivery_service.create_delivery()
    assert r.status_code == 200, "delivert service connection failed"

def test_read_delivery(self):
    r = delivery_service.delivery_service.read_delivery()
    assert r.status_code == 200, "delivert service connection failed"
        