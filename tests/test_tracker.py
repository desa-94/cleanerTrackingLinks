import pytest
from tracker import Tracker

@pytest.fixture
def tracker():
    return Tracker()

def test_detect_carrier_ups(tracker):
    assert tracker.detect_carrier("1Z") == "UPS"

def test_detect_carrier_dhl(tracker):
    assert tracker.detect_carrier("JD") == "DHL"

def test_unknown_carrier(tracker):
    assert tracker.detect_carrier("XXXX") is None

def test_swap_y_to_z(tracker):
    assert tracker.swap("1Y") == "1Z"

def test_fix_keyboard_layout_keeps_Z(tracker):
    assert tracker.fix_UPS_keyboard_layout_error("1Z") == "1Z"

def test_fix_keyboard_layout_swap_Y(tracker):
    assert tracker.fix_UPS_keyboard_layout_error("1Y") == "1Z"

def test_build_link_ups(tracker):
    link = tracker.build_tracking_link("1Z12345")
    assert "ups.com" in link
    assert "1Z12345" in link

def test_build_link_dhl_jd(tracker):
    link = tracker.build_tracking_link("JD123456")
    assert "dhl.de" in link
    assert "JD123456" in link

def test_build_link_dhl_jj(tracker):
    link = tracker.build_tracking_link("JJ123456")
    assert "dhl.de" in link
    assert "JJ123456" in link

def test_build_link_dhl_digit(tracker):
    link = tracker.build_tracking_link("0034123456")
    assert "dhl.de" in link
    assert "0034123456" in link

def test_build_link_unknown_returns_empty(tracker):
    assert tracker.build_tracking_link("XXXX") == ""

def test_build_email_contains_link(tracker):
    email = tracker.build_email("1Z12345")
    assert "ups.com" in email
    assert "1Z12345" in email

def test_build_email_unknown_returns_empty(tracker):
    assert tracker.build_email("XXXX") == ""

def test_build_email_empty_input(tracker):
    assert tracker.build_tracking_link("") == ""

def test_whitespace_input(tracker):
    assert tracker.detect_carrier(" 1Z ".strip()) == "UPS"

def test_lowercase_input(tracker):
    link = tracker.build_tracking_link("1z123")
    assert "1Z123" in link