import json
from pathlib import Path

DEFAULT_OUTPUT_DIR = Path("output")


def _render_markdown(events: list[dict]) -> str:
    """Render events as a visually highlighted Markdown document."""
    lines: list[str] = []
    lines.append("# 📊 Forex Factory Calendar\n")

    high = [e for e in events if e.get("impact") == "High"]
    med = [e for e in events if e.get("impact") == "Medium"]
    low = [e for e in events if e.get("impact") == "Low"]
    lines.append(f"> **{len(high)}** 🔴 High · **{len(med)}** 🟡 Medium · **{len(low)}** 🟢 Low\n")

    hdr = "| Time | Day | Title | Currency | Forecast | Previous | Sessions |"
    sep = "|:----:|:---:|-------|:--------:|:--------:|:--------:|----------|"

    def _cell(val: str, bold: bool = False) -> str:
        return f"**{val}**" if bold else val

    def _row(e: dict, bold: bool = False) -> str:
        day_en = e.get("day_of_week", "")
        day_fa = e.get("day_of_week_persian", "")
        day_col = f"{day_en} ({day_fa})" if day_fa else day_en
        return (
            f"| {_cell(e['time'], bold)} | {day_col} | {_cell(e['title'], bold)} | {_cell(e['currency'], bold)} "
            f"| {e.get('forecast') or '-'} | {e.get('previous') or '-'} "
            f"| {', '.join(e.get('sessions', []))} |"
        )

    if high:
        lines.append("---\n")
        lines.append("## 🔴 High Impact\n")
        lines.extend([hdr, sep])
        for e in high:
            lines.append(_row(e, bold=True))
        lines.append("")

    if med:
        lines.append("---\n")
        lines.append("## 🟡 Medium Impact\n")
        lines.extend([hdr, sep])
        for e in med:
            lines.append(_row(e))
        lines.append("")

    if low:
        lines.append("---\n")
        lines.append("## 🟢 Low Impact\n")
        lines.extend([hdr, sep])
        for e in low:
            lines.append(_row(e))
        lines.append("")

    return "\n".join(lines)


def save_events(events: list[dict], output_file: str, save_format: str = "json", output_dir: str | Path | None = None) -> None:
    """Save events to a file in the specified format."""
    out_dir = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
    out_dir.mkdir(exist_ok=True)
    ext = {"json": ".json", "txt": ".txt", "md": ".md"}.get(save_format)
    if not ext:
        print(f"Unsupported save format: {save_format}")
        return
    output_filename = str(out_dir / f"{output_file}{ext}")

    if save_format == "json":
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(events, f, indent=4)
    elif save_format == "txt":
        with open(output_filename, "w", encoding="utf-8") as f:
            for event in events:
                f.write(
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
    elif save_format == "md":
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(_render_markdown(events))

    print(f"Events saved to {save_format.upper()} file: {output_filename}")