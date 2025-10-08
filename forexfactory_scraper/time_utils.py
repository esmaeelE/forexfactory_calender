from datetime import datetime, timedelta
import tzlocal
import pytz

def get_current_monday() -> datetime:
    """Calculate the date of the current week's Monday."""
    today = datetime.now()
    return today - timedelta(days=today.weekday())

def convert_to_24h(time_str: str) -> str:
    """Convert time from 12-hour (AM/PM) to 24-hour format."""
    try:
        time_obj = datetime.strptime(time_str, "%I:%M%p")
        return time_obj.strftime("%H:%M")
    except ValueError:
        return time_str

def get_system_timezone() -> str:
    """Get the system's local timezone."""
    try:
        local_tz = tzlocal.get_localzone()
        return str(local_tz)
    except Exception as e:
        print(f"Could not determine system timezone: {e}. Falling back to UTC.")
        return "UTC"

def convert_time_to_timezone(time_str: str, from_tz: str = "UTC", to_tz: str = "UTC") -> str:
    """Convert event time from one timezone to another."""
    try:
        from_tz_obj = pytz.timezone(from_tz)
        to_tz_obj = pytz.timezone(to_tz)
    except pytz.exceptions.UnknownTimeZoneError as e:
        print(f"Invalid timezone: {e}")
        return time_str

    time_24h = convert_to_24h(time_str)
    try:
        time_obj = datetime.strptime(time_24h, "%H:%M")
        time_obj = from_tz_obj.localize(time_obj)
        time_obj = time_obj.astimezone(to_tz_obj)
        return time_obj.strftime("%H:%M")
    except ValueError as e:
        print(f"Error converting time: {e}")
        return time_str