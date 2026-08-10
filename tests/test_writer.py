import json
from pathlib import Path

from forexfactory_scraper.writer import save_events


SAMPLE_EVENTS = [
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
        "url": "https://example.com",
        "sessions": ["New York", "London"],
    }
]


class TestSaveEventsJson:
    def test_creates_output_dir_and_json(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        save_events(SAMPLE_EVENTS, "test_out", "json")

        out_file = tmp_path / "output" / "test_out.json"
        assert out_file.exists()

        data = json.loads(out_file.read_text())
        assert len(data) == 1
        assert data[0]["currency"] == "USD"


class TestSaveEventsTxt:
    def test_creates_output_dir_and_txt(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        save_events(SAMPLE_EVENTS, "test_out", "txt")

        out_file = tmp_path / "output" / "test_out.txt"
        assert out_file.exists()

        content = out_file.read_text()
        assert "Non-Farm Employment Change" in content
        assert "USD" in content


class TestSaveEventsMarkdown:
    def test_creates_output_dir_and_md(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        save_events(SAMPLE_EVENTS, "test_out", "md")

        out_file = tmp_path / "output" / "test_out.md"
        assert out_file.exists()

        content = out_file.read_text()
        assert "🔴 High Impact" in content
        assert "Non-Farm Employment Change" in content
        assert "USD" in content
        assert "Friday (jome)" in content

    def test_md_sections_by_impact(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        events = [
            {**SAMPLE_EVENTS[0], "impact": "Medium"},
            {**SAMPLE_EVENTS[0], "title": "CPI", "impact": "Low"},
        ]
        save_events(events, "test_out", "md")

        content = (tmp_path / "output" / "test_out.md").read_text()
        assert "🟡 Medium Impact" in content
        assert "🟢 Low Impact" in content


class TestSaveEventsUnsupportedFormat:
    def test_unsupported_format(self, tmp_path, monkeypatch, capsys):
        monkeypatch.chdir(tmp_path)
        save_events(SAMPLE_EVENTS, "test_out", "csv")
        captured = capsys.readouterr()
        assert "Unsupported" in captured.out