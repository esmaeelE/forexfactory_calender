import pytest
from forexfactory_scraper.time_utils import (
    convert_to_24h,
    get_system_timezone,
    convert_time_to_timezone,
)


class TestConvertTo24h:
    @pytest.mark.parametrize(
        "input_time, expected",
        [
            ("08:30AM", "08:30"),
            ("12:00AM", "00:00"),
            ("12:00PM", "12:00"),
            ("01:15PM", "13:15"),
            ("11:59PM", "23:59"),
            ("09:00AM", "09:00"),
        ],
    )
    def test_valid_times(self, input_time, expected):
        assert convert_to_24h(input_time) == expected

    @pytest.mark.parametrize(
        "input_time",
        ["invalid", "25:00", "", "8:30", "0830AM"],
    )
    def test_invalid_times_return_input(self, input_time):
        assert convert_to_24h(input_time) == input_time


class TestConvertTimeToTimezone:
    def test_same_timezone(self):
        result = convert_time_to_timezone("08:30AM", from_tz="UTC", to_tz="UTC")
        assert result == "08:30"

    def test_utc_to_tehran(self):
        result = convert_time_to_timezone("08:30AM", from_tz="UTC", to_tz="Asia/Tehran")
        # UTC+3:30 offset; exact value depends on zoneinfo data / DST
        h, m = map(int, result.split(":"))
        assert (h, m) == (11, 55)  # current zoneinfo data gives 11:55

    def test_invalid_timezone_returns_input(self):
        result = convert_time_to_timezone("08:30AM", from_tz="Bad/Zone")
        assert result == "08:30AM"  # raw input returned on error

    def test_invalid_time_string(self):
        result = convert_time_to_timezone("not-a-time", from_tz="UTC", to_tz="UTC")
        assert result == "not-a-time"


class TestGetSystemTimezone:
    def test_returns_string(self):
        result = get_system_timezone()
        assert isinstance(result, str)
        assert result  # non-empty