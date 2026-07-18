import click
import schedule as sched
import time
from .fetcher import fetch_and_parse_xml
from .writer import save_events
from .time_utils import get_system_timezone
from .config import load_config

@click.command()
@click.option("--schedule", is_flag=True, help="Schedule the script to run every hour.")
@click.option("--currency", type=str, help="Filter events by currency (e.g., USD, EUR).")
@click.option("--title", type=str, help="Filter events by title (case-insensitive).")
@click.option("--impact", type=str, help="Filter events by impact (e.g., High, Medium, Low).")
@click.option("--save-format", type=click.Choice(["json", "txt", "md"]), default="json", help="Save format: json, txt, or md.")
@click.option("--output-file", type=str, default="filtered_events", help="Base name for the output file.")
@click.option("--timezone", type=str, default=None, help="Convert event times to the specified timezone.")
@click.option("--system-timezone", is_flag=True, help="Use the system's local timezone for event times.")
@click.option("--config", type=click.Path(exists=True), default=None, help="Path to a JSON config file.")
def main(
    schedule: bool,
    currency: str | None,
    title: str | None,
    impact: str | None,
    save_format: str,
    output_file: str,
    timezone: str | None,
    system_timezone: bool,
    config: str | None,
) -> None:
    """Fetch and parse Forex Factory events with optional filters."""
    if config:
        config_data = load_config(config)
        if config_data:
            if "currency" in config_data:
                currency = config_data["currency"]
            if "title" in config_data:
                title = config_data["title"]
            if "impact" in config_data:
                impact = config_data["impact"]
            if "save_format" in config_data:
                save_format = config_data["save_format"]
            if "output_file" in config_data:
                output_file = config_data["output_file"]
            if "timezone" in config_data:
                timezone = config_data["timezone"]
            if "system_timezone" in config_data:
                system_timezone = config_data["system_timezone"]
            print(f"Loaded configuration from {config}")

    if system_timezone and not timezone:
        timezone = get_system_timezone()
        print(f"Using system timezone: {timezone}")

    def fetch_and_save() -> None:
        """Helper function to fetch and save events."""
        events = fetch_and_parse_xml(currency, title, impact, timezone)
        if events:
            save_events(events, output_file, save_format)
        else:
            print("No events to save.")

    if schedule:
        print("Scheduling the script to run every hour...")
        fetch_and_save()
        sched.every(1).hours.do(fetch_and_save)
        while True:
            sched.run_pending()
            time.sleep(1)
    else:
        fetch_and_save()

if __name__ == "__main__":
    main()