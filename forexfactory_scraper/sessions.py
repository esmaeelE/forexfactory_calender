from datetime import time as dt_time
from .constants import TRADING_SESSIONS, GOLDEN_TIME_START, GOLDEN_TIME_END

def _parse_time(t: str) -> dt_time:
    h, m = t.split(":")
    return dt_time(int(h), int(m))

# Parse once at import, not on every call
_SESSION_RANGES = [
    (name, _parse_time(t["start"]), _parse_time(t["end"]))
    for name, t in TRADING_SESSIONS.items()
]
_GOLDEN_START = _parse_time(GOLDEN_TIME_START)
_GOLDEN_END = _parse_time(GOLDEN_TIME_END)

def get_trading_sessions(event_time: str) -> list[str]:
    """Determine active trading sessions based on event time, including Golden Time."""
    from .time_utils import convert_to_24h
    event_time_24h = convert_to_24h(event_time)
    try:
        h, m = event_time_24h.split(":")
        et = dt_time(int(h), int(m))
    except (ValueError, AttributeError):
        return ["Invalid Time"]

    sessions = []
    for name, start, end in _SESSION_RANGES:
        if start > end:  # Overnight session
            if et >= start or et < end:
                sessions.append(name)
        elif start <= et < end:
            sessions.append(name)

    if (
        "London" in sessions
        and "New York" in sessions
        and _GOLDEN_START <= et < _GOLDEN_END
    ):
        sessions.append("Golden Time")

    return sessions if sessions else ["After Hours"]