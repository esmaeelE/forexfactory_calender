import pytest
from forexfactory_scraper.time_utils import convert_to_24h, convert_time_to_timezone

def test_convert_to_24h():
    assert convert_to_24h("08:30AM") == "08:30"
    assert convert_to_24h("01:15PM") == "13:15"
    assert convert_to_24h("invalid") == "invalid"

def test_convert_time_to_timezone():
    result = convert_time_to_timezone("08:30AM", from_tz="UTC", to_tz="Asia/Tehran")
    assert result != "08:30"  # Should adjust based on timezone difference