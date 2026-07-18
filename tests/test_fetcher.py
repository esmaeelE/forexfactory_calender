import xml.etree.ElementTree as ET
from unittest.mock import patch, MagicMock

import pytest

from forexfactory_scraper.fetcher import parse_events, fetch_xml


SAMPLE_XML = """<week>
  <event>
    <title>Non-Farm Employment Change</title>
    <country>USD</country>
    <date>07-18-2025</date>
    <time>08:30AM</time>
    <impact>High</impact>
    <forecast>180K</forecast>
    <previous>272K</previous>
    <url>https://example.com/nfp</url>
  </event>
  <event>
    <title>CPI m/m</title>
    <country>USD</country>
    <date>07-18-2025</date>
    <time>02:00PM</time>
    <impact>High</impact>
    <forecast>0.3%</forecast>
    <previous>0.3%</previous>
    <url>https://example.com/cpi</url>
  </event>
  <event>
    <title>GDP m/m</title>
    <country>EUR</country>
    <date>07-18-2025</date>
    <time>09:00AM</time>
    <impact>Medium</impact>
    <forecast>0.2%</forecast>
    <previous>0.1%</previous>
    <url>https://example.com/gdp</url>
  </event>
</week>"""


@pytest.fixture
def sample_root():
    return ET.fromstring(SAMPLE_XML)


class TestParseEvents:
    def test_no_filters_returns_all(self, sample_root):
        events = parse_events(sample_root)
        assert len(events) == 3

    def test_currency_filter(self, sample_root):
        events = parse_events(sample_root, currency_filter="USD")
        assert len(events) == 2
        assert all(e["currency"] == "USD" for e in events)

    def test_impact_filter(self, sample_root):
        events = parse_events(sample_root, impact_filter="High")
        assert len(events) == 2

    def test_title_filter_case_insensitive(self, sample_root):
        events = parse_events(sample_root, title_filter="nfp")
        # "Non-Farm Employment Change" doesn't contain "nfp"
        assert len(events) == 0

        events = parse_events(sample_root, title_filter="non-farm")
        assert len(events) == 1

    def test_combined_filters(self, sample_root):
        events = parse_events(
            sample_root, currency_filter="USD", impact_filter="High"
        )
        assert len(events) == 2

    def test_none_root_returns_empty(self):
        assert parse_events(None) == []

    def test_event_structure(self, sample_root):
        events = parse_events(sample_root, currency_filter="EUR")
        assert len(events) == 1
        event = events[0]
        assert event["title"] == "GDP m/m"
        assert event["day_of_week"] == "Friday"
        assert event["day_of_week_persian"] == "jome"
        assert isinstance(event["sessions"], list)

    def test_timezone_conversion(self, sample_root):
        events = parse_events(
            sample_root,
            currency_filter="USD",
            title_filter="non-farm",
            user_timezone="Asia/Tehran",
        )
        assert len(events) == 1
        # 08:30 UTC -> ~12:00 Tehran (UTC+3:30); exact depends on zoneinfo data
        h, m = map(int, events[0]["time"].split(":"))
        assert (h, m) == (11, 55)


class TestFetchXml:
    @patch("forexfactory_scraper.fetcher.requests.get")
    def test_successful_fetch(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.content = SAMPLE_XML.encode()
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        root = fetch_xml()
        assert root is not None
        assert root.tag == "week"

    @patch("forexfactory_scraper.fetcher.requests.get")
    def test_network_error_returns_none(self, mock_get):
        import requests
        mock_get.side_effect = requests.RequestException("timeout")
        assert fetch_xml() is None

    @patch("forexfactory_scraper.fetcher.requests.get")
    def test_invalid_xml_returns_none(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.content = b"<not valid xml <<>>"
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        assert fetch_xml() is None