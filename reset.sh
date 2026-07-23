#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SONGS_FILE="$SCRIPT_DIR/songs.txt"
URLS_FILE="$SCRIPT_DIR/youtube_urls.txt"
OUTPUT_DIR="$SCRIPT_DIR/outputs"

echo "This will clear songs.txt, youtube_urls.txt, and everything inside outputs/."
if ! read -r -p "Continue? [y/N]: " CONFIRMATION; then
  echo
  echo "Reset cancelled."
  exit 0
fi

case "$CONFIRMATION" in
  [yY]|[yY][eE][sS])
    ;;
  *)
    echo "Reset cancelled."
    exit 0
    ;;
esac

# Empty the input and generated URL lists, creating them if needed.
: > "$SONGS_FILE"
: > "$URLS_FILE"

# Keep the outputs directory itself and delete only its contents.
mkdir -p "$OUTPUT_DIR"
find "$OUTPUT_DIR" -mindepth 1 -delete

echo "Reset complete."
