import json
from pathlib import Path

from forexfactory_scraper.config import load_config


class TestLoadConfig:
    def test_loads_valid_config(self, tmp_path):
        cfg = tmp_path / "config.json"
        cfg.write_text(json.dumps({"currency": "EUR", "impact": "High"}))

        result = load_config(str(cfg))
        assert result == {"currency": "EUR", "impact": "High"}

    def test_invalid_json_returns_empty_dict(self, tmp_path, capsys):
        cfg = tmp_path / "bad.json"
        cfg.write_text("not json {{{")

        result = load_config(str(cfg))
        assert result == {}
        assert "Error" in capsys.readouterr().out

    def test_file_not_found_returns_empty_dict(self, capsys):
        result = load_config("/nonexistent/config.json")
        assert result == {}
        assert "Error" in capsys.readouterr().out

    def test_md_save_format_is_valid(self, tmp_path):
        cfg = tmp_path / "config.json"
        cfg.write_text(json.dumps({"save_format": "md"}))
        result = load_config(str(cfg))
        assert result == {"save_format": "md"}

    def test_invalid_save_format_returns_empty_dict(self, tmp_path, capsys):
        cfg = tmp_path / "config.json"
        cfg.write_text(json.dumps({"save_format": "csv"}))
        result = load_config(str(cfg))
        assert result == {}
        assert "Invalid save_format" in capsys.readouterr().out
