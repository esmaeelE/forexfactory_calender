import json
from typing import List, Dict

def save_events(events: List[Dict], output_file: str, save_format: str = "json") -> None:
    """Save events to a file in the specified format."""
    if save_format == "json":
        output_filename = f"{output_file}.json"
        with open(output_filename, "w", encoding="utf-8") as json_file:
            json.dump(events, json_file, indent=4)
        print(f"Events saved to JSON file: {output_filename}")
    elif save_format == "txt":
        output_filename = f"{output_file}.txt"
        with open(output_filename, "w", encoding="utf-8") as txt_file:
            for event in events:
                event_str = (
                    f"Title: {event['title']}\n"
                    f"Currency: {event['currency']}\n"
                    f"Date: {event['date']}\n"
                    f"Time: {event['time']}\n"
                    f"Impact: {event['impact']}\n"
                    f"Forecast: {event['forecast']}\n"
                    f"Previous: {event['previous']}\n"
                    f"URL: {event['url']}\n"
                    f"Sessions: {', '.join(event['sessions'])}\n"
                    f"{'-' * 40}\n"
                )
                txt_file.write(event_str)
        print(f"Events saved to TXT file: {output_filename}")
    else:
        print(f"Unsupported save format: {save_format}")