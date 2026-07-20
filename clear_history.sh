#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.json"

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "Missing config file: $CONFIG_FILE" >&2
  exit 1
fi

TARGET_FILES=()
while IFS= read -r target_file; do
  TARGET_FILES+=("$target_file")
done < <(
  python3 - <<'PY'
import json
from pathlib import Path

config = json.loads(Path("config.json").read_text(encoding="utf-8"))
print(config.get("songs_file", "songs.txt"))
print(config.get("urls_file", "youtube_urls.txt"))
print(config.get("download_dir", "outputs"))
PY
)

for file_name in "${TARGET_FILES[@]:0:2}"; do
  : > "$SCRIPT_DIR/$file_name"
  echo "Cleared $file_name"
done

OUTPUT_DIR="$SCRIPT_DIR/${TARGET_FILES[2]}"
if [[ -d "$OUTPUT_DIR" ]]; then
  find "$OUTPUT_DIR" -mindepth 1 -delete
  echo "Cleared ${TARGET_FILES[2]}/"
fi
