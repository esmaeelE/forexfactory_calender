from datetime import datetime
from zoneinfo import ZoneInfo

def convert_to_24h(time_str: str) -> str:
    """Convert time from 12-hour (AM/PM) to 24-hour format."""
    try:
        time_obj = datetime.strptime(time_str, "%I:%M%p")
        return time_obj.strftime("%H:%M")
    except ValueError:
        return time_str

def get_system_timezone() -> str:
    """Get the system's local timezone."""
    import time as _time
    tz = _time.tzname[0]
    # Map common abbreviations to IANA names
    _MAP = {"UTC": "UTC", "EST": "America/New_York", "CST": "America/Chicago", "PST": "America/Los_Angeles"}
    return _MAP.get(tz, "UTC")

def convert_time_to_timezone(time_str: str, from_tz: str = "UTC", to_tz: str = "UTC") -> str:
    """Convert event time from one timezone to another."""
    try:
        from_info = ZoneInfo(from_tz)
        to_info = ZoneInfo(to_tz)
    except (KeyError, ValueError) as e:
        print(f"Invalid timezone: {e}")
        return time_str

    time_24h = convert_to_24h(time_str)
    try:
        naive = datetime.strptime(time_24h, "%H:%M")
        aware = naive.replace(tzinfo=from_info)
        converted = aware.astimezone(to_info)
        return converted.strftime("%H:%M")
    except ValueError as e:
        print(f"Error converting time: {e}")
        return time_str