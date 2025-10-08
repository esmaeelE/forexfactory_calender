import xml.etree.ElementTree as ET
import requests
from typing import List, Dict, Optional
from .time_utils import convert_time_to_timezone
from .sessions import get_trading_sessions
from .constants import FOREX_FACTORY_URL

def fetch_xml(timeout: int = 10) -> Optional[ET.Element]:
    """Fetch XML from FOREX_FACTORY_URL and return the parsed ElementTree root, or None on error."""
    try:
        response = requests.get(FOREX_FACTORY_URL, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch XML: {e}")
        return None

    try:
        root = ET.fromstring(response.content)
        return root
    except ET.ParseError as e:
        print(f"Failed to parse XML: {e}")
        return None

def parse_events(
    root: ET.Element,
    currency_filter: Optional[str] = None,
    title_filter: Optional[str] = None,
    impact_filter: Optional[str] = None,
    user_timezone: Optional[str] = None
) -> List[Dict]:
    """Parse an ElementTree root into a list of event dicts, applying filters and timezone conversion."""
    events: List[Dict] = []
    if root is None:
        return events

    for event in root.findall("event"):
        # handle missing elements
        def _text(node_name: str) -> Optional[str]:
            node = event.find(node_name)
            return node.text if node is not None else None

        title = _text("title") or ""
        currency = _text("country") or ""
        date = _text("date") or ""
        time_str = _text("time") or ""
        impact = _text("impact") or ""
        forecast = _text("forecast")
        previous = _text("previous")
        url = _text("url") or ""

        event_data: Dict = {
            "title": title,
            "currency": currency,
            "date": date,
            "time": time_str,
            "impact": impact,
            "forecast": forecast,
            "previous": previous,
            "url": url,
        }

        # sessions may accept empty or None time; preserve original time for sessions before conversion
        event_data["sessions"] = get_trading_sessions(time_str)

        # convert time if requested
        if user_timezone and time_str:
            try:
                event_data["time"] = convert_time_to_timezone(time_str, to_tz=user_timezone)
            except Exception as e:
                # If conversion fails, keep original time and optionally log
                print(f"Time conversion failed for '{time_str}' -> {user_timezone}: {e}")

        # Apply filters
        if (
            (not currency_filter or event_data["currency"] == currency_filter)
            and (not title_filter or title_filter.lower() in event_data["title"].lower())
            and (not impact_filter or event_data["impact"] == impact_filter)
        ):
            events.append(event_data)

    return events

def fetch_and_parse_xml(
    currency_filter: Optional[str] = None,
    title_filter: Optional[str] = None,
    impact_filter: Optional[str] = None,
    user_timezone: Optional[str] = None
) -> List[Dict]:
    """Wrapper: fetch XML then parse events with provided filters."""
    root = fetch_xml()
    if root is None:
        return []
    return parse_events(
        root,
        currency_filter=currency_filter,
        title_filter=title_filter,
        impact_filter=impact_filter,
        user_timezone=user_timezone,
    )
