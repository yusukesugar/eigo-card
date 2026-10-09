# せかいのことば

子ども向けの ことばのアプリ（英語・韓国語・中国語・タイ語・ベトナム語）。オフラインで動く Web アプリ（PWA）として GitHub Pages に置く。

- **えいごカード**（`words.html`）: 絵を押すと英単語をしゃべる。15ページ・182語
- **えいごでいおう**（`phrases.html`）: 「I like ___.」のような文の枠に、絵を押して語を入れかえる。10ページ・120文

どちらも きく／テスト／えらぶ の3モード。

- ホームの世界地図は `map_svg.py` が `map/countries-110m.json`（world-atlas）から作る。話す人の数は `build.py` の `LANGS`

別のアプリとして **リバーシとごもく**（`docs/games/`）も同じ Pages に置く。元は `boardgame.html`、アイコンは `pwa/games/`。iPad のホーム画面には別のアイコンで入る。

## ビルド

```sh
python3 build.py
```

- 単語は `build.py` の `PAGES`、文は `phrases.py` の `PHRASE_PAGES` に書く。文は入れかえる語を `{}` でかこむ
- 音声は macOS の `say`（Samantha）で作り、`audio/` にキャッシュする。足した語の分だけ新しく作る
- 出力は2つ
  - `docs/` GitHub Pages 用。ホーム画面・manifest・Service Worker 付き
  - `artifact/` claude.ai の Artifact 用（git 管理外）
- `sw.js` の版番号は `docs/` の中身から作る。中身が変わると iPad 側のキャッシュが入れかわる

## iPad に入れる

1. Safari で GitHub Pages の URL を開く
2. 共有ボタン →「ホーム画面に追加」
3. 一度開けば、以降はネットがなくても動く

## アイコンを作り直すとき

`pwa/icon.html` を Chrome の headless で 512×512 に撮り、`sips -z` で 192 と 180 を作る。
