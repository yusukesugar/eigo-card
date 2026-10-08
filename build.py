"""単語と文のリストから音声を作り、template.html に埋め込んで2つのアプリを書き出す。

- docs/     GitHub Pages に置くオフライン版（PWA）
- artifact/ claude.ai の Artifact に上げる版

音声は macOS の say で作る。audio/ にキャッシュし、単語を足したときは差分だけ作る。
"""
import base64
import hashlib
import json
import pathlib
import shutil
import subprocess

HERE = pathlib.Path(__file__).parent
AUDIO_DIR = HERE / "audio"
PWA_DIR = HERE / "pwa"
DOCS_DIR = HERE / "docs"
ARTIFACT_DIR = HERE / "artifact"

PAGES = [
    ("動物", [
        ("🐱", "cat", "猫"), ("🐶", "dog", "犬"), ("🐰", "rabbit", "うさぎ"),
        ("🐻", "bear", "熊"), ("🦁", "lion", "ライオン"), ("🐘", "elephant", "象"),
        ("🐵", "monkey", "猿"), ("🐷", "pig", "豚"), ("🐮", "cow", "牛"),
        ("🐴", "horse", "馬"), ("🐧", "penguin", "ペンギン"), ("🐸", "frog", "カエル"),
    ]),
    ("海・虫", [
        ("🐟", "fish", "魚"), ("🐳", "whale", "クジラ"), ("🐬", "dolphin", "イルカ"),
        ("🐙", "octopus", "タコ"), ("🦀", "crab", "カニ"), ("🦈", "shark", "サメ"),
        ("🐢", "turtle", "カメ"), ("🦋", "butterfly", "チョウ"), ("🐝", "bee", "ハチ"),
        ("🐜", "ant", "アリ"), ("🐌", "snail", "カタツムリ"), ("🕷️", "spider", "クモ（虫）"),
    ]),
    ("食べ物", [
        ("🍎", "apple", "りんご"), ("🍌", "banana", "バナナ"), ("🍇", "grapes", "ぶどう"),
        ("🍓", "strawberry", "いちご"), ("🍉", "watermelon", "すいか"), ("🍊", "orange", "みかん"),
        ("🍞", "bread", "パン"), ("🍚", "rice", "ご飯"), ("🥚", "egg", "卵"),
        ("🍰", "cake", "ケーキ"), ("🍦", "ice cream", "アイス"), ("🥛", "milk", "牛乳"),
    ]),
    ("乗り物", [
        ("🚗", "car", "車"), ("🚌", "bus", "バス"), ("🚃", "train", "電車"),
        ("🚲", "bicycle", "自転車"), ("✈️", "airplane", "飛行機"), ("🚢", "ship", "船"),
        ("🚀", "rocket", "ロケット"), ("🚕", "taxi", "タクシー"), ("🚚", "truck", "トラック"),
        ("🚒", "fire engine", "消防車"), ("🚑", "ambulance", "救急車"),
        ("🚁", "helicopter", "ヘリコプター"),
    ]),
    ("色・形", [
        ("🔴", "red", "赤"), ("🔵", "blue", "青"), ("🟡", "yellow", "黄色"),
        ("🟢", "green", "緑"), ("🟠", "orange", "オレンジ色"), ("🟣", "purple", "紫"),
        ("⚫", "black", "黒"), ("⚪", "white", "白"), ("🟤", "brown", "茶色"),
        ("⭕", "circle", "丸"), ("🔺", "triangle", "三角"), ("❤️", "heart", "ハート"),
    ]),
    ("数 1〜12", [
        ("1", "one", "一"), ("2", "two", "二"), ("3", "three", "三"),
        ("4", "four", "四"), ("5", "five", "五"), ("6", "six", "六"),
        ("7", "seven", "七"), ("8", "eight", "八"), ("9", "nine", "九"),
        ("10", "ten", "十"), ("11", "eleven", "十一"), ("12", "twelve", "十二"),
    ]),
    ("数 13〜100", [
        ("13", "thirteen", "十三"), ("14", "fourteen", "十四"),
        ("15", "fifteen", "十五"), ("16", "sixteen", "十六"),
        ("17", "seventeen", "十七"), ("18", "eighteen", "十八"),
        ("19", "nineteen", "十九"), ("20", "twenty", "二十"),
        ("0", "zero", "ゼロ"), ("30", "thirty", "三十"),
        ("50", "fifty", "五十"), ("100", "one hundred", "百"),
    ]),
    ("体", [
        ("🙂", "face", "顔"), ("👁️", "eye", "目"), ("👂", "ear", "耳"),
        ("👃", "nose", "鼻"), ("👄", "mouth", "口"), ("🦷", "tooth", "歯"),
        ("✋", "hand", "手"), ("👆", "finger", "指"), ("💪", "arm", "腕"),
        ("🦶", "foot", "足"), ("🦴", "bone", "骨"), ("🧠", "brain", "脳"),
    ]),
    ("人・家族", [
        ("🙋", "I", "私"), ("🫵", "you", "あなた"), ("👦", "he", "彼（男の子）"),
        ("👧", "she", "彼女（女の子）"), ("👫", "we", "私たち"),
        ("👩", "mother", "お母さん"), ("👨", "father", "お父さん"),
        ("👭", "sister", "姉・妹"), ("👬", "brother", "兄・弟"),
        ("👶", "baby", "赤ちゃん"), ("👵", "grandmother", "おばあちゃん"),
        ("👴", "grandfather", "おじいちゃん"),
    ]),
    ("学校", [
        ("🏫", "school", "学校"), ("✏️", "pencil", "鉛筆"), ("🖊️", "pen", "ペン"),
        ("🖍️", "crayon", "クレヨン"), ("📓", "notebook", "ノート"), ("📏", "ruler", "定規"),
        ("✂️", "scissors", "はさみ"), ("🎒", "backpack", "ランドセル"), ("🎨", "paints", "絵の具"),
        ("🎹", "piano", "ピアノ"), ("⚽", "ball", "ボール"), ("📅", "calendar", "カレンダー"),
    ]),
    ("家", [
        ("🏠", "house", "家"), ("🚪", "door", "ドア"), ("🛏️", "bed", "ベッド"),
        ("🪑", "chair", "いす"), ("🕐", "clock", "時計"), ("🔑", "key", "鍵"),
        ("📖", "book", "本"), ("☕", "cup", "カップ"), ("🥄", "spoon", "スプーン"),
        ("☂️", "umbrella", "傘"), ("👟", "shoes", "靴"), ("🛁", "bath", "お風呂"),
    ]),
    ("空・自然", [
        ("☀️", "sun", "太陽"), ("🌙", "moon", "月"), ("⭐", "star", "星"),
        ("🌈", "rainbow", "虹"), ("☁️", "cloud", "雲"), ("🌧️", "rain", "雨"),
        ("❄️", "snow", "雪"), ("🌳", "tree", "木"), ("🌸", "flower", "花"),
        ("⛰️", "mountain", "山"), ("🏞️", "river", "川"), ("🌊", "sea", "海"),
    ]),
    ("お父さんの仕事", [
        ("💻", "computer", "コンピューター"), ("⌨️", "keyboard", "キーボード"),
        ("🖱️", "mouse", "マウス（ねずみと同じ）"), ("🖥️", "screen", "画面"),
        ("📱", "smartphone", "スマホ"), ("🤖", "robot", "ロボット"),
        ("🌐", "internet", "インターネット"), ("📧", "email", "メール"), ("🎮", "game", "ゲーム"),
        ("🐛", "bug", "バグ（虫と同じ）"), ("💡", "idea", "アイデア"), ("🔋", "battery", "電池"),
    ]),
]

# アルファベットは文字の名前で読ませる。単語と音声が混ざらないよう、読み上げ文を別に持つ
LETTER_NAMES = ("エー ビー シー ディー イー エフ ジー エイチ アイ ジェー ケー エル エム "
                "エヌ オー ピー キュー アール エス ティー ユー ブイ ダブリュー エックス ワイ ズィー").split()
LETTERS = [(f"{c} {c.lower()}", c, name, f"[[char LTRL]]{c}[[char NORM]]")
           for c, name in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", LETTER_NAMES)]
PAGES += [("ABC A〜M", LETTERS[:13]), ("ABC N〜Z", LETTERS[13:])]


def audio_uri(word: str, speech: str, voice: str = "Samantha", prefix: str = "") -> str:
    # macOS はファイル名の大文字小文字を区別しないので、文字の音声は別名にする
    name = prefix + ("letter_" if speech != word else "") + word.replace(" ", "_")
    m4a = AUDIO_DIR / f"{name}.m4a"
    if not m4a.exists():
        aiff = AUDIO_DIR / f"{name}.aiff"
        subprocess.run(["say", "-v", voice, "-r", "150", "-o", str(aiff), speech], check=True)
        subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", "-b", "64000", str(aiff), str(m4a)], check=True)
    return "data:audio/mp4;base64," + base64.b64encode(m4a.read_bytes()).decode()


WORD_HINTS = {
    "listen": "カードを押すと、英語でしゃべるよ",
    "quiz": "英語で何て言う？ 言えたら「答え」を押してね",
    "pick": "音を聞いて、合っている絵を選んでね",
}
PHRASE_HINTS = {
    "listen": "絵を押すと、文が変わってしゃべるよ",
    "quiz": "？？？のところを入れて、文を全部言ってみよう",
    "pick": "文を聞いて、合っている絵を選んでね",
}
def lang_hints(lang: str) -> dict:
    return {
        "listen": f"カードを押すと、{lang}でしゃべるよ",
        "quiz": f"{lang}で何て言う？ 言えたら「答え」を押してね",
        "pick": "音を聞いて、合っている絵を選んでね",
    }


CHINESE_HINTS = {
    "listen": "カードを押すと、中国語でしゃべるよ",
    "quiz": "中国語で何て言う？ 言えたら「答え」を押してね",
    "pick": "音を聞いて、合っている絵を選んでね",
}
KOREAN_HINTS = {
    "listen": "カードを押すと、韓国語でしゃべるよ",
    "quiz": "韓国語で何て言う？ 言えたら「答え」を押してね",
    "pick": "音を聞いて、合っている絵を選んでね",
}


# GitHub Pages 版だけに付ける。claude.ai の Artifact はこの部分を自前で持っている
PWA_HEAD = """<!doctype html>
<html lang="ja">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="えいご">
<meta name="theme-color" content="#2f7fd6">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<style>
  html { background: #2f7fd6; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
  body { margin: 0; }
  [hidden] { display: none !important; }
</style>
"""
PWA_TAIL = """
<script>
  if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js").catch(() => {});
</script>
"""
PWA_HOME = '<a class="home" href="./">🏠 戻る</a>'


def split_reading(card, has_reading: bool) -> list:
    """韓国語・中国語の「アンニョンハセヨ（こんにちは）」を 意味 と 読み に分ける。

    読みは答えそのものなので、テストで伏せているあいだは出さない。
    英語の「クモ（虫）」のような かっこ は補足なので分けない（has_reading の言語だけが対象）。
    """
    pic, word, ja = card
    if not has_reading:
        return [pic, word, ja]
    if ja.endswith("）") and "（" in ja:
        reading, meaning = ja[:-1].split("（", 1)
        return [pic, word, meaning, reading.strip()]
    return [pic, word, ja, ja]


# 場面のページ（飛行機・お店など）では、聞かれる側（偶数番目）を店員さんの声にして会話に聞こえるようにする
STAFF_VOICE = "Reed (English (US))"


def build(title: str, pages_src, hints: dict, notes: dict, name: str, labeled: frozenset = frozenset(),
          voice: str = "Samantha", audio_prefix: str = "", pick_shows_word: bool = False,
          has_reading: bool = False, dialog: frozenset = frozenset()) -> None:
    """pick_shows_word: 選ぶ の選択肢に、その言語の語（ハングル・漢字）を添える。
    has_reading: 日本語欄が「読み（意味）」の形の言語。dialog: 聞かれる→答える が交互に並ぶページ。"""
    AUDIO_DIR.mkdir(exist_ok=True)
    plain = lambda s: s.replace("{", "").replace("}", "")
    speeches = {}
    for t, items in pages_src:
        for k, x in enumerate(items):
            staff = t in dialog and k % 2 == 0
            speeches[plain(x[1])] = (x[3] if len(x) > 3 else plain(x[1]),
                                     STAFF_VOICE if staff else voice,
                                     ("staff_" if staff else "") + audio_prefix)
    unknown = set(notes) - set(speeches)
    assert not unknown, f"notes のキーがカードに無い: {unknown}"
    audio = {w: audio_uri(w, s, v, p) for w, (s, v, p) in sorted(speeches.items())}
    pages = [{"title": t, "words": [split_reading(x[:3], has_reading) for x in items], "labels": t in labeled}
             for t, items in pages_src]
    data = (
        "const PAGES = " + json.dumps(pages, ensure_ascii=False) + ";\n"
        "const AUDIO = " + json.dumps(audio) + ";\n"
        "const HINTS = " + json.dumps(hints, ensure_ascii=False) + ";\n"
        "const NOTES = " + json.dumps(notes, ensure_ascii=False) + ";\n"
        "const PICK_SHOWS_WORD = " + json.dumps(pick_shows_word) + ";\n"
    )
    html = (HERE / "template.html").read_text()
    assert html.count("/*DATA*/") == 1 and html.count("<!--HOME-->") == 1
    html = html.replace("/*DATA*/", data).replace("{{TITLE}}", title)

    ARTIFACT_DIR.mkdir(exist_ok=True)
    (ARTIFACT_DIR / f"{name}.html").write_text(html.replace("<!--HOME-->", ""))
    DOCS_DIR.mkdir(exist_ok=True)
    out = DOCS_DIR / f"{name}.html"
    out.write_text(PWA_HEAD + html.replace("<!--HOME-->", PWA_HOME) + PWA_TAIL)
    print(f"{name}: pages={len(pages)} cards={sum(len(p['words']) for p in pages)} "
          f"audio={len(audio)} size={out.stat().st_size}")


# リバーシとごもく。boardgame.html は Artifact と同じ素の中身。Pages 版にだけ 戻るボタンと PWA の頭を付ける
GAME_HOME = """<style>
  html { background: var(--bg); }
  .home { align-self: flex-start; padding: 6px 14px; border-radius: 999px; background: var(--accent);
          color: var(--accent-fg); font-weight: 700; text-decoration: none; }
</style>
"""


def build_boardgame() -> None:
    src = (HERE / "boardgame.html").read_text()
    assert src.count('<div class="app">\n') == 1
    body = src.replace('<div class="app">\n', '<div class="app">\n  ' + PWA_HOME + "\n")
    (DOCS_DIR / "boardgame.html").write_text(PWA_HEAD + GAME_HOME + body + PWA_TAIL)
    print(f"boardgame: size={(DOCS_DIR / 'boardgame.html').stat().st_size}")


def build_pwa_shell() -> None:
    """ホーム画面・アイコン・manifest を docs/ に写し、sw.js に中身から作った版番号を入れる。"""
    for f in ["index.html", "manifest.webmanifest", "icon-180.png", "icon-192.png", "icon-512.png"]:
        shutil.copyfile(PWA_DIR / f, DOCS_DIR / f)
    h = hashlib.sha256()
    for f in sorted(DOCS_DIR.iterdir()):
        if f.name != "sw.js":
            h.update(f.name.encode() + f.read_bytes())
    sw = (PWA_DIR / "sw.js").read_text().replace("{{VERSION}}", "eigo-" + h.hexdigest()[:12])
    (DOCS_DIR / "sw.js").write_text(sw)
    (DOCS_DIR / ".nojekyll").touch()


if __name__ == "__main__":
    from notes import PHRASE_NOTES, WORD_NOTES
    from phrases import DIALOG_PAGES, LABELED_PAGES, PHRASE_PAGES
    from korean import KOREAN_LABELED_PAGES, KOREAN_NOTES, KOREAN_PAGES
    from chinese import CHINESE_LABELED_PAGES, CHINESE_NOTES, CHINESE_PAGES

    build("英語カード", PAGES, WORD_HINTS, WORD_NOTES, "words")
    build("英語で言おう", PHRASE_PAGES, PHRASE_HINTS, PHRASE_NOTES, "phrases", frozenset(LABELED_PAGES),
          dialog=frozenset(DIALOG_PAGES))
    build("韓国語", KOREAN_PAGES, KOREAN_HINTS, KOREAN_NOTES, "korean", frozenset(KOREAN_LABELED_PAGES),
          voice="Yuna", audio_prefix="ko_", pick_shows_word=True, has_reading=True)
    build("中国語", CHINESE_PAGES, CHINESE_HINTS, CHINESE_NOTES, "chinese", frozenset(CHINESE_LABELED_PAGES),
          voice="Tingting", audio_prefix="zh_", pick_shows_word=True, has_reading=True)

    from thai import THAI_LABELED_PAGES, THAI_NOTES, THAI_PAGES
    from vietnamese import VIETNAMESE_LABELED_PAGES, VIETNAMESE_NOTES, VIETNAMESE_PAGES

    build("タイ語", THAI_PAGES, lang_hints("タイ語"), THAI_NOTES, "thai", frozenset(THAI_LABELED_PAGES),
          voice="Kanya", audio_prefix="th_", pick_shows_word=True, has_reading=True)
    build("ベトナム語", VIETNAMESE_PAGES, lang_hints("ベトナム語"), VIETNAMESE_NOTES, "vietnamese",
          frozenset(VIETNAMESE_LABELED_PAGES), voice="Linh", audio_prefix="vi_", pick_shows_word=True, has_reading=True)
    build_boardgame()
    build_pwa_shell()
