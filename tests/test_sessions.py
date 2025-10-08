from forexfactory_scraper.sessions import get_trading_sessions

def test_get_trading_sessions():
    assert "London" in get_trading_sessions("08:00AM")
    assert "Golden Time" in get_trading_sessions("02:00PM")  # During London-NY overlap