# Forexfactory Calendar

A Python CLI tool and library to fetch, filter, and save **Forex Factory** economic calendar events in JSON, TXT, or Markdown format.

## Features

- Fetches live events from the Forex Factory XML feed
- Filters by **currency**, **impact**, and **title**
- Outputs to **JSON**, **TXT**, or **Markdown** (with color-coded impact sections)
- Converts event times to any IANA timezone or the system's local timezone
- Detects active **trading sessions** (London, New York, Tokyo, Sydney, Golden Time)
- Includes English day names and romanized Persian day names
- Optional **hourly scheduling** mode
- JSON config file support
- 47 unit tests

## Installation

```bash
# Using uv (recommended)
uv sync

# Or with pip
pip install -e .
```

## Quick Start

```bash
# Run with default config (USD High Impact, Asia/Tehran)
forexfactory-scraper

# Filter USD High Impact events, save as Markdown
forexfactory-scraper --currency USD --impact High --save-format md

# Use a config file
forexfactory-scraper --config config.json

# Auto-detect system timezone
forexfactory-scraper --system-timezone
```

## CLI Options

| Option | Description |
|--------|-------------|
| `--currency` | Filter by currency code (e.g., USD, EUR) |
| `--impact` | Filter by impact level (High, Medium, Low) |
| `--title` | Filter by event title (case-insensitive substring) |
| `--save-format` | Output format: `json`, `txt`, or `md` (default: json) |
| `--output-file` | Base filename for output (default: filtered_events) |
| `--timezone` | Convert times to IANA timezone (e.g., Asia/Tehran) |
| `--system-timezone` | Use system's local timezone for event times |
| `--config` | Path to a JSON config file |
| `--schedule` | Run every hour |

## Config File

Create a `config.json`:

```json
{
    "currency": "USD",
    "impact": "High",
    "save_format": "md",
    "output_file": "usd_high_impact_events",
    "timezone": "Asia/Tehran",
    "system_timezone": false,
    "schedule": false
}
```

Any CLI option can be set via config. CLI flags always take precedence.

## Output Formats

### Markdown (`--save-format md`)

Produces a structured document with:
- Event count summary by impact level
- Separate tables per impact category (🔴 High, 🟡 Medium, 🟢 Low)
- Bold formatting for high-impact events
- English + romanized Persian day names
- Active trading sessions per event

### JSON (`--save-format json`)

```json
[
    {
        "title": "Non-Farm Employment Change",
        "currency": "USD",
        "date": "07-18-2025",
        "day_of_week": "Friday",
        "day_of_week_persian": "jome",
        "time": "08:30",
        "impact": "High",
        "forecast": "180K",
        "previous": "272K",
        "url": "...",
        "sessions": ["New York", "London", "Golden Time"]
    }
]
```

### TXT (`--save-format txt`)

Plain text with labeled fields separated by dashes.

## Output Directory

All output files are saved to the `output/` directory by default.

## Trading Sessions

Times are evaluated against these session windows (FOREX_FACTORY_TZ = America/New_York):

| Session | Start | End |
|---------|-------|-----|
| Sydney | 5:00 PM | 2:00 AM |
| Tokyo | 7:00 PM | 4:00 AM |
| London | 3:00 AM | 12:00 PM |
| New York | 8:00 AM | 5:00 PM |
| Golden Time | 8:00 AM | 12:00 PM (London+NY overlap) |

## Development

```bash
# Run tests
python -m pytest tests/ -v

# Run with default config
forexfactory-scraper
```

## Project Structure

```
forexfactory_calender/
├── forexfactory_scraper/
│   ├── __init__.py        # Package version
│   ├── cli.py             # Click CLI interface
│   ├── config.py          # JSON config loader
│   ├── constants.py       # URLs, session definitions, timezone
│   ├── fetcher.py         # XML fetch + event parsing/filtering
│   ├── sessions.py        # Trading session detection
│   ├── time_utils.py      # Timezone conversion utilities
│   └── writer.py          # Output writers (JSON, TXT, Markdown)
├── tests/
│   ├── test_config.py
│   ├── test_fetcher.py
│   ├── test_sessions.py
│   ├── test_time_utils.py
│   └── test_writer.py
├── config.json
├── pyproject.toml
└── README.md
```

## License

MIT