import os
import sys
import json

import yt_dlp

CONFIG_PATH = "config.json"
DEFAULT_URLS_FILE = "youtube_urls.txt"
DEFAULT_OUTPUT_DIR = "outputs"


def load_defaults():
    if not os.path.exists(CONFIG_PATH):
        return DEFAULT_URLS_FILE, DEFAULT_OUTPUT_DIR

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    urls_file = data.get("urls_file", DEFAULT_URLS_FILE)
    output_dir = data.get("download_dir", DEFAULT_OUTPUT_DIR)
    return urls_file, output_dir


def load_urls(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"List file not found: {file_path}")

    urls = []
    with open(file_path, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("- "):
                line = line[2:].strip()
            elif line.startswith("* "):
                line = line[2:].strip()
            if line.startswith("http://") or line.startswith("https://"):
                urls.append(line)

    return urls


def download_dj_fast(file_path=DEFAULT_URLS_FILE, output_dir=DEFAULT_OUTPUT_DIR):
    urls = load_urls(file_path)
    if not urls:
        print("Error: No valid URLs found in the list file.")
        return 1

    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "ignoreerrors": True,
        "addmetadata": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
            },
            {
                "key": "FFmpegMetadata",
            },
        ],
    }

    print(f"{len(urls)} items (Destination: {output_dir}/)...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls)
        print("\n🔥 Download Complete 🔥")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


def main():
    default_urls_file, default_output_dir = load_defaults()
    file_path = sys.argv[1] if len(sys.argv) > 1 else default_urls_file
    output_dir = sys.argv[2] if len(sys.argv) > 2 else default_output_dir
    return download_dj_fast(file_path, output_dir)


if __name__ == "__main__":
    raise SystemExit(main())
