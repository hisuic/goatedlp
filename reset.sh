#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SONGS_FILE="$SCRIPT_DIR/songs.txt"
URLS_FILE="$SCRIPT_DIR/youtube_urls.txt"
OUTPUT_DIR="$SCRIPT_DIR/outputs"

echo "songs.txt、youtube_urls.txt、および outputs/ 内のすべてを削除します。"
if ! read -r -p "本当に実行しますか？ [y/N]: " CONFIRMATION; then
  echo
  echo "リセットをキャンセルしました。"
  exit 0
fi

case "$CONFIRMATION" in
  [yY]|[yY][eE][sS])
    ;;
  *)
    echo "リセットをキャンセルしました。"
    exit 0
    ;;
esac

# 入力・生成済み URL の一覧を空にする（ファイルがなければ作成する）。
: > "$SONGS_FILE"
: > "$URLS_FILE"

# outputs ディレクトリ自体は残し、中身だけを削除する。
mkdir -p "$OUTPUT_DIR"
find "$OUTPUT_DIR" -mindepth 1 -delete

echo "リセットが完了しました。"
