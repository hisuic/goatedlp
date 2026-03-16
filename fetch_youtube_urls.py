#!/usr/bin/env python3
"""Fetch the top YouTube search result URL for each song title from songs.txt."""

from __future__ import annotations

import sys
from pathlib import Path
import json

try:
    from yt_dlp import YoutubeDL
except ImportError:
    print(
        "yt-dlp is not installed. Run: python3 -m pip install yt-dlp",
        file=sys.stderr,
    )
    sys.exit(1)


CONFIG_PATH = Path("config.json")


def load_config(config_path: Path) -> dict:
    with config_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    query_template = data.get("query_template")
    songs_file = data.get("songs_file")
    urls_file = data.get("urls_file")

    if not isinstance(query_template, str) or "{title}" not in query_template:
        raise ValueError("'query_template' must be a string containing '{title}'.")

    if not isinstance(songs_file, str) or not songs_file:
        raise ValueError("'songs_file' must be a non-empty string.")

    if not isinstance(urls_file, str) or not urls_file:
        raise ValueError("'urls_file' must be a non-empty string.")

    return data


def fetch_top_result_url(query: str) -> str | None:
    options = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
        "default_search": "ytsearch1",
    }

    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=False)

    entries = info.get("entries") or []
    if not entries:
        return None

    first = entries[0]
    video_url = first.get("url")
    if not video_url:
        return None

    if video_url.startswith("http://") or video_url.startswith("https://"):
        return video_url
    return f"https://www.youtube.com/watch?v={video_url}"


def parse_bullet_text_file(file_path: Path) -> list[str]:
    if not file_path.exists():
        raise FileNotFoundError(f"Missing list file: {file_path}")

    items: list[str] = []
    for raw_line in file_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("- "):
            line = line[2:].strip()
        elif line.startswith("* "):
            line = line[2:].strip()
        items.append(line)

    return items


def build_output_lines(config: dict) -> list[str]:
    query_template = config["query_template"]
    songs = parse_bullet_text_file(Path(config["songs_file"]))
    lines: list[str] = []

    for title in songs:
        query = query_template.format(title=title)
        try:
            url = fetch_top_result_url(query)
        except Exception as exc:  # noqa: BLE001
            lines.append(f"- ERROR: {title} ({exc})")
            continue

        if url:
            lines.append(f"- {url}")
        else:
            lines.append(f"- NOT FOUND: {title}")

    return lines


def main() -> int:
    try:
        config = load_config(CONFIG_PATH)
    except FileNotFoundError:
        print(f"Missing config file: {CONFIG_PATH}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Invalid config: {exc}", file=sys.stderr)
        return 1

    output_path = Path(config["urls_file"])
    lines = build_output_lines(config)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} entries to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
