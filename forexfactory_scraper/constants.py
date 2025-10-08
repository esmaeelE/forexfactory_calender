"""Constants for the Forex Factory Scraper package."""

FOREX_FACTORY_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"

TRADING_SESSIONS = {
    "Sydney": {"start": "21:00", "end": "06:00"},
    "Tokyo": {"start": "00:00", "end": "09:00"},
    "London": {"start": "07:00", "end": "16:00"},
    "New York": {"start": "13:00", "end": "22:00"},
}

GOLDEN_TIME_START = "13:00"
GOLDEN_TIME_END = "16:00"