# 🐐 The GOATED yt-dlp 🐐

The GOATED yt-dlp wrapper for musics.

`songs.txt` に曲名を書いておくと、YouTube 検索の先頭動画 URL を集め、その一覧をもとに音声を一括ダウンロードするツールです🔥  
曲名のリスト作成、URL 取得、音声保存を分けて実行することも可能です

## Requirements
最新版のyt-dlp
```bash
python3 -m pip install yt-dlp
```

次に `songs.txt` に曲名を箇条書きで書きます。

```txt
Song One
Song Two
```

必要なら `config.json` を調整します。
`query_template`の部分をいじります。`{title}` の部分に各曲名が入ります。下の例では全ての曲の`曲名 audio`と検索して一番上に出てきた動画の音声をダウンロードする仕組みです。


```json
{
  "query_template": "{title} audio",
  "songs_file": "songs.txt",
  "urls_file": "youtube_urls.txt",
  "download_dir": "outputs"
}
```

## ダウンロードの手順
URL 取得からダウンロードまでを一括で行う場合:

```bash
./run_all.sh
```

URL の取得だけ行う場合:

```bash
python3 fetch_youtube_urls.py
```

音声のダウンロードだけ行う場合:

```bash
python3 app.py
```

URL ファイルや保存先を直接指定する場合:

```bash
python3 app.py youtube_urls.txt outputs
```


## 動作の説明

`fetch_youtube_urls.py` は `config.json` を読み込み、`songs.txt` の各曲名に対して `query_template` を使って検索語を作ります。  
その検索語で YouTube を `yt-dlp` 経由で検索し、先頭の動画 URL を `youtube_urls.txt` に箇条書きで保存します。検索に失敗した曲は `ERROR`、見つからなかった曲は `NOT FOUND` として出力されます。

`app.py` は URL 一覧を読み込み、HTTP/HTTPS の行だけを対象に音声をダウンロードします。保存先ディレクトリは自動で作成され、音声は `m4a` を優先して保存されます。

`run_all.sh` は上の 2 つを順番に実行するだけのラッパーです。最初に URL を作り、その結果を使って音声を保存します。
