import xml.etree.ElementTree as ET
import requests
from datetime import datetime
from .time_utils import convert_time_to_timezone
from .sessions import get_trading_sessions
from .constants import FOREX_FACTORY_URL

_PERSIAN_DAYS = {
    "Saturday": "shanbe",
    "Sunday": "yekshanbe",
    "Monday": "doshanbe",
    "Tuesday": "seshanbe",
    "Wednesday": "chaharshanbe",
    "Thursday": "panjshanbe",
    "Friday": "jomeh",
}

def fetch_xml(timeout: int = 10) -> ET.Element | None:
    """Fetch XML from FOREX_FACTORY_URL and return the parsed ElementTree root, or None on error."""
    try:
        response = requests.get(FOREX_FACTORY_URL, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch XML: {e}")
        return None

    try:
        return ET.fromstring(response.content)
    except ET.ParseError as e:
        print(f"Failed to parse XML: {e}")
        return None

def parse_events(
    root: ET.Element | None,
    currency_filter: str | None = None,
    title_filter: str | None = None,
    impact_filter: str | None = None,
    user_timezone: str | None = None,
) -> list[dict]:
    """Parse an ElementTree root into a list of event dicts, applying filters and timezone conversion."""
    if root is None:
        return []

    events = []
    for event in root.findall("event"):
        title = (event.findtext("title") or "")
        currency = (event.findtext("country") or "")
        date = (event.findtext("date") or "")
        time_str = (event.findtext("time") or "")
        impact = (event.findtext("impact") or "")

        event_data = {
            "title": title,
            "currency": currency,
            "date": date,
            "day_of_week": "",
            "day_of_week_persian": "",
            "time": time_str,
            "impact": impact,
            "forecast": event.findtext("forecast"),
            "previous": event.findtext("previous"),
            "url": event.findtext("url") or "",
        }

        event_data["sessions"] = get_trading_sessions(time_str)

        # parse day of week from date (fixed MM-DD-YYYY format)
        if date:
            try:
                day = datetime.strptime(date, "%m-%d-%Y").strftime("%A")
                event_data["day_of_week"] = day
                event_data["day_of_week_persian"] = _PERSIAN_DAYS.get(day, "")
            except ValueError:
                pass

        if user_timezone and time_str:
            try:
                event_data["time"] = convert_time_to_timezone(time_str, to_tz=user_timezone)
            except Exception as e:
                print(f"Time conversion failed for '{time_str}' -> {user_timezone}: {e}")

        # Apply filters
        if (
            (not currency_filter or currency == currency_filter)
            and (not title_filter or title_filter.lower() in title.lower())
            and (not impact_filter or impact == impact_filter)
        ):
            events.append(event_data)

    return events

def fetch_and_parse_xml(
    currency_filter: str | None = None,
    title_filter: str | None = None,
    impact_filter: str | None = None,
    user_timezone: str | None = None,
) -> list[dict]:
    """Wrapper: fetch XML then parse events with provided filters."""
    return parse_events(
        fetch_xml(),
        currency_filter=currency_filter,
        title_filter=title_filter,
        impact_filter=impact_filter,
        user_timezone=user_timezone,
    )
