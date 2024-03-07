import pytest

from delivery_service import delivery_service as ds


def test_create_delivery(self):
    r = ds.create_delivery()
    assert r.status_code == 200, "delivert service connection failed"

def test_read_delivery(self):
    r = ds.read_delivery()
    assert r.status_code == 200, "delivert service connection failed"
        