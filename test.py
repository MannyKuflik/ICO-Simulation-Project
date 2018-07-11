import pytest
from app import round_sig, btctrans, ethtrans, connect, hello

def test_round_sig():
    assert round_sig(1234560, 4) == 1235000
    assert round_sig(0.000456, 2) == 0.00046

def test_btctrans():
    pass