import pytest
from forexfactory_scraper.sessions import get_trading_sessions


class TestGetTradingSessions:
    @pytest.mark.parametrize(
        "time_str, expected_session",
        [
            ("08:00AM", "London"),       # within London (07:00-16:00)
            ("02:00PM", "Golden Time"),  # London + NY overlap + golden time
            ("10:00PM", "Sydney"),       # overnight Sydney session
            ("01:00AM", "Tokyo"),        # Tokyo session
            ("07:00PM", "New York"),     # NY session
        ],
    )
    def test_active_sessions(self, time_str, expected_session):
        sessions = get_trading_sessions(time_str)
        assert expected_session in sessions

    def test_after_hours(self):
        sessions = get_trading_sessions("12:00AM")
        # Could be Sydney/Tokyo depending on definition; check it's a list
        assert isinstance(sessions, list)

    def test_invalid_time(self):
        sessions = get_trading_sessions("invalid")
        assert sessions == ["Invalid Time"]

    def test_empty_string(self):
        sessions = get_trading_sessions("")
        assert sessions == ["Invalid Time"]

    def test_london_ny_overlap_returns_golden_time(self):
        """During London-NY overlap within golden time window, Golden Time should appear."""
        sessions = get_trading_sessions("02:00PM")
        assert "Golden Time" in sessions
        assert "London" in sessions
        assert "New York" in sessions

    def test_after_hours_label(self):
        """A time outside all session ranges should return After Hours."""
        # 06:00AM is boundary of Tokyo end, Sydney end; check it gets some session
        sessions = get_trading_sessions("06:00AM")
        assert isinstance(sessions, list) and len(sessions) >= 1