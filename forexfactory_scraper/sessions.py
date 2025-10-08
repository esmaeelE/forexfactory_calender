from datetime import datetime
from typing import List
from .constants import TRADING_SESSIONS, GOLDEN_TIME_START, GOLDEN_TIME_END
from .time_utils import convert_to_24h

def get_trading_sessions(event_time: str) -> List[str]:
    """Determine active trading sessions based on event time, including Golden Time."""
    event_time_24h = convert_to_24h(event_time)
    try:
        event_time_obj = datetime.strptime(event_time_24h, "%H:%M").time()
    except ValueError:
        return ["Invalid Time"]

    sessions = []
    golden_start = datetime.strptime(GOLDEN_TIME_START, "%H:%M").time()
    golden_end = datetime.strptime(GOLDEN_TIME_END, "%H:%M").time()

    for session, times in TRADING_SESSIONS.items():
        start = datetime.strptime(times["start"], "%H:%M").time()
        end = datetime.strptime(times["end"], "%H:%M").time()

        if start > end:  # Overnight session
            if event_time_obj >= start or event_time_obj < end:
                sessions.append(session)
        elif start <= event_time_obj < end:
            sessions.append(session)

    if (
        "London" in sessions
        and "New York" in sessions
        and golden_start <= event_time_obj < golden_end
    ):
        sessions.append("Golden Time")

    return sessions if sessions else ["After Hours"]