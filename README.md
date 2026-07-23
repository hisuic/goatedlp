# 🐐 The GOATED yt-dlp 🐐

The GOATED yt-dlp wrapper for music.

Add song titles to `songs.txt`, and this tool will collect the top YouTube search result for each title and download the audio in one batch. 🔥
You can also run the URL collection and audio download steps separately.

## Requirements

- Python 3.10 or later
- The latest version of yt-dlp (version used during initial development: `2026.03.13`)
- `ffmpeg` / `ffprobe`
- A JavaScript runtime such as Deno (required for full YouTube support)

Install yt-dlp with its standard optional dependencies, including `yt-dlp-ejs`:

```bash
python3 -m pip install -U "yt-dlp[default]"
```

Install `ffmpeg` / `ffprobe` and a JavaScript runtime separately. On macOS with Homebrew, run:

```bash
brew install ffmpeg deno
```

Next, add one song title per line to `songs.txt`:

```txt
Song One
Song Two
```

Adjust `config.json` if needed. The `query_template` setting controls the YouTube search query, and `{title}` is replaced with each song title. In the example below, every song is searched as `<song title> audio`, and the audio from the top result is downloaded.


```json
{
  "query_template": "{title} audio",
  "songs_file": "songs.txt",
  "urls_file": "youtube_urls.txt",
  "download_dir": "outputs"
}
```

## Usage

To collect URLs and download their audio in one command:

```bash
./run_all.sh
```

To collect URLs only:

```bash
python3 fetch_youtube_urls.py
```

To download audio only:

```bash
python3 app.py
```

To clear the song list, collected URLs, and downloaded files:

```bash
./reset.sh
```

This empties `songs.txt` and `youtube_urls.txt` and removes everything inside `outputs` while keeping the directory itself. A confirmation prompt is displayed first, and the reset proceeds only when you enter `y` or `yes`.

To specify the URL file and output directory directly:

```bash
python3 app.py youtube_urls.txt outputs
```


## How It Works

`fetch_youtube_urls.py` reads `config.json` and builds a search query for each song in `songs.txt` using `query_template`. It searches YouTube through `yt-dlp` and writes the top video URL for each song to `youtube_urls.txt`. Failed searches are marked as `ERROR`, and searches with no results are marked as `NOT FOUND`.

`app.py` reads the URL list and downloads audio from lines containing HTTP or HTTPS URLs. It creates the output directory automatically and prefers the `m4a` audio format.

`run_all.sh` is a wrapper that runs the two scripts in sequence. It collects the URLs first, then uses them to download the audio.
