# Forex Factory Scraper

![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-Apache%202.0-blue)

A Python package to fetch, filter, and save Forex events from [Forex Factory's](https://www.forexfactory.com/) weekly calendar. The package supports filtering events by currency, title, and impact, and saves output in JSON or TXT format. It includes scheduling capabilities, timezone support, and trading session identification.

## Features

- **Automated Fetching**: Fetches Forex events from Forex Factory's weekly calendar.
- **Event Parsing**: Extracts details like title, currency, date, time, impact, forecast, previous value, and URL.
- **Custom Filters**: Filter events by:
  - **Currency** (e.g., USD, EUR)
  - **Title** (case-insensitive search)
  - **Impact** (e.g., High, Medium, Low)
- **Output Formats**: Save events in:
  - **JSON**: Structured and machine-readable.
  - **TXT**: Human-readable, formatted text.
- **Custom File Names**: Specify a custom base name for output files.
- **Scheduling**: Run the script hourly using the `schedule` library.
- **Timezone Support**: Convert event times to a specified or system timezone.
- **Trading Sessions**: Identifies active sessions (e.g., London, New York) and "Golden Time" (London-NY overlap).
- **Configuration File**: Load options from a JSON config file for automation.

## Installation

### From Source
1. Clone the repository:
    ```sh
    git clone https://github.com/abbasi0abolfazl/forexfactory-scraper.git
    cd forexfactory-scraper
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Install the package in editable mode:
    ```sh
    pip install -e .
    ```

## Usage

### Command-Line Interface
Run the package using the CLI:

```sh
forexfactory-scraper --currency USD --impact High --output-file usd_high_impact_events
```

#### Command-Line Options
| Option              | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `--schedule`        | Schedule the script to run every hour.                                      |
| `--currency`        | Filter events by currency (e.g., `USD`, `EUR`).                             |
| `--title`           | Filter events by title (case-insensitive).                                  |
| `--impact`          | Filter events by impact (e.g., `High`, `Medium`, `Low`).                    |
| `--save-format`     | Save format: `json` or `txt` (default: `json`).                             |
| `--output-file`     | Base name for the output file (default: `filtered_events`).                 |
| `--timezone`        | Convert event times to the specified timezone (e.g., `America/New_York`).   |
| `--system-timezone` | Use the system's local timezone for event times.                            |
| `--config`          | Path to a JSON config file to load options from.                            |

#### Examples
1. **Run Once with Default Settings**:
   ```sh
   forexfactory-scraper
   ```
   Output: `filtered_events.json`

2. **Filter by Currency and Save as TXT**:
   ```sh
   forexfactory-scraper --currency USD --save-format txt --output-file usd_events
   ```
   Output: `usd_events.txt`

3. **Schedule Hourly Runs**:
   ```sh
   forexfactory-scraper --schedule
   ```

4. **Use Config File**:
   ```sh
   forexfactory-scraper --config config.json
   ```

### Programmatic Usage
Use the package in your Python code:

```python
from forexfactory_scraper import fetch_and_parse_xml, save_events

# Fetch and filter events
events = fetch_and_parse_xml(
    currency_filter="USD",
    impact_filter="High",
    user_timezone="Asia/Tehran"
)

# Save events
save_events(events, "usd_high_impact_events", save_format="json")
```

## Running as a Background Process
Use `nohup` or a process manager like `systemd`:

```sh
nohup forexfactory-scraper --schedule &
```

## Output Files
- **JSON Format**:
  ```json
  [
      {
          "title": "Nonfarm Payrolls",
          "currency": "USD",
          "date": "10-27-2023",
          "time": "08:30",
          "impact": "High",
          "forecast": "200K",
          "previous": "187K",
          "url": "https://www.forexfactory.com/event/12345",
          "sessions": ["New York", "London", "Golden Time"]
      }
  ]
  ```

- **TXT Format**:
  ```
  Title: Nonfarm Payrolls
  Currency: USD
  Date: 10-27-2023
  Time: 08:30
  Impact: High
  Forecast: 200K
  Previous: 187K
  URL: https://www.forexfactory.com/event/12345
  Sessions: New York, London, Golden Time
  ----------------------------------------
  ```

## Configuration File
Create a `config.json` file to store options:

```json
{
    "schedule": false,
    "currency": "USD",
    "impact": "High",
    "save_format": "json",
    "output_file": "usd_high_impact_events",
    "system_timezone": false,
    "timezone": "Asia/Tehran"
}
```

## License
This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.
