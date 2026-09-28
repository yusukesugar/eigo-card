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
    ("どうぶつ", [
        ("🐱", "cat", "ねこ"), ("🐶", "dog", "いぬ"), ("🐰", "rabbit", "うさぎ"),
        ("🐻", "bear", "くま"), ("🦁", "lion", "ライオン"), ("🐘", "elephant", "ぞう"),
        ("🐵", "monkey", "さる"), ("🐷", "pig", "ぶた"), ("🐮", "cow", "うし"),
        ("🐴", "horse", "うま"), ("🐧", "penguin", "ペンギン"), ("🐸", "frog", "かえる"),
    ]),
    ("うみ・むし", [
        ("🐟", "fish", "さかな"), ("🐳", "whale", "くじら"), ("🐬", "dolphin", "いるか"),
        ("🐙", "octopus", "たこ"), ("🦀", "crab", "かに"), ("🦈", "shark", "さめ"),
        ("🐢", "turtle", "かめ"), ("🦋", "butterfly", "ちょうちょ"), ("🐝", "bee", "はち"),
        ("🐜", "ant", "あり"), ("🐌", "snail", "かたつむり"), ("🕷️", "spider", "くも（むし）"),
    ]),
    ("たべもの", [
        ("🍎", "apple", "りんご"), ("🍌", "banana", "バナナ"), ("🍇", "grapes", "ぶどう"),
        ("🍓", "strawberry", "いちご"), ("🍉", "watermelon", "すいか"), ("🍊", "orange", "みかん"),
        ("🍞", "bread", "パン"), ("🍚", "rice", "ごはん"), ("🥚", "egg", "たまご"),
        ("🍰", "cake", "ケーキ"), ("🍦", "ice cream", "アイス"), ("🥛", "milk", "ぎゅうにゅう"),
    ]),
    ("のりもの", [
        ("🚗", "car", "くるま"), ("🚌", "bus", "バス"), ("🚃", "train", "でんしゃ"),
        ("🚲", "bicycle", "じてんしゃ"), ("✈️", "airplane", "ひこうき"), ("🚢", "ship", "ふね"),
        ("🚀", "rocket", "ロケット"), ("🚕", "taxi", "タクシー"), ("🚚", "truck", "トラック"),
        ("🚒", "fire engine", "しょうぼうしゃ"), ("🚑", "ambulance", "きゅうきゅうしゃ"),
        ("🚁", "helicopter", "ヘリコプター"),
    ]),
    ("いろ・かたち", [
        ("🔴", "red", "あか"), ("🔵", "blue", "あお"), ("🟡", "yellow", "きいろ"),
        ("🟢", "green", "みどり"), ("🟠", "orange", "オレンジいろ"), ("🟣", "purple", "むらさき"),
        ("⚫", "black", "くろ"), ("⚪", "white", "しろ"), ("🟤", "brown", "ちゃいろ"),
        ("⭕", "circle", "まる"), ("🔺", "triangle", "さんかく"), ("❤️", "heart", "ハート"),
    ]),
    ("かず 1〜12", [
        ("1", "one", "いち"), ("2", "two", "に"), ("3", "three", "さん"),
        ("4", "four", "よん"), ("5", "five", "ご"), ("6", "six", "ろく"),
        ("7", "seven", "なな"), ("8", "eight", "はち"), ("9", "nine", "きゅう"),
        ("10", "ten", "じゅう"), ("11", "eleven", "じゅういち"), ("12", "twelve", "じゅうに"),
    ]),
    ("かず 13〜100", [
        ("13", "thirteen", "じゅうさん"), ("14", "fourteen", "じゅうよん"),
        ("15", "fifteen", "じゅうご"), ("16", "sixteen", "じゅうろく"),
        ("17", "seventeen", "じゅうなな"), ("18", "eighteen", "じゅうはち"),
        ("19", "nineteen", "じゅうきゅう"), ("20", "twenty", "にじゅう"),
        ("0", "zero", "ゼロ"), ("30", "thirty", "さんじゅう"),
        ("50", "fifty", "ごじゅう"), ("100", "one hundred", "ひゃく"),
    ]),
    ("からだ", [
        ("🙂", "face", "かお"), ("👁️", "eye", "め"), ("👂", "ear", "みみ"),
        ("👃", "nose", "はな"), ("👄", "mouth", "くち"), ("🦷", "tooth", "は"),
        ("✋", "hand", "て"), ("👆", "finger", "ゆび"), ("💪", "arm", "うで"),
        ("🦶", "foot", "あし"), ("🦴", "bone", "ほね"), ("🧠", "brain", "のう"),
    ]),
    ("ひと・かぞく", [
        ("🙋", "I", "わたし"), ("🫵", "you", "あなた"), ("👦", "he", "かれ（おとこのこ）"),
        ("👧", "she", "かのじょ（おんなのこ）"), ("👫", "we", "わたしたち"),
        ("👩", "mother", "おかあさん"), ("👨", "father", "おとうさん"),
        ("👭", "sister", "おねえさん・いもうと"), ("👬", "brother", "おにいさん・おとうと"),
        ("👶", "baby", "あかちゃん"), ("👵", "grandmother", "おばあちゃん"),
        ("👴", "grandfather", "おじいちゃん"),
    ]),
    ("がっこう", [
        ("🏫", "school", "がっこう"), ("✏️", "pencil", "えんぴつ"), ("🖊️", "pen", "ペン"),
        ("🖍️", "crayon", "クレヨン"), ("📓", "notebook", "ノート"), ("📏", "ruler", "じょうぎ"),
        ("✂️", "scissors", "はさみ"), ("🎒", "backpack", "ランドセル"), ("🎨", "paints", "えのぐ"),
        ("🎹", "piano", "ピアノ"), ("⚽", "ball", "ボール"), ("📅", "calendar", "カレンダー"),
    ]),
    ("おうち", [
        ("🏠", "house", "いえ"), ("🚪", "door", "ドア"), ("🛏️", "bed", "ベッド"),
        ("🪑", "chair", "いす"), ("🕐", "clock", "とけい"), ("🔑", "key", "かぎ"),
        ("📖", "book", "ほん"), ("☕", "cup", "カップ"), ("🥄", "spoon", "スプーン"),
        ("☂️", "umbrella", "かさ"), ("👟", "shoes", "くつ"), ("🛁", "bath", "おふろ"),
    ]),
    ("そら・しぜん", [
        ("☀️", "sun", "たいよう"), ("🌙", "moon", "つき"), ("⭐", "star", "ほし"),
        ("🌈", "rainbow", "にじ"), ("☁️", "cloud", "くも（そら）"), ("🌧️", "rain", "あめ"),
        ("❄️", "snow", "ゆき"), ("🌳", "tree", "き"), ("🌸", "flower", "はな"),
        ("⛰️", "mountain", "やま"), ("🏞️", "river", "かわ"), ("🌊", "sea", "うみ"),
    ]),
    ("おとうさんのしごと", [
        ("💻", "computer", "コンピューター"), ("⌨️", "keyboard", "キーボード"),
        ("🖱️", "mouse", "マウス（ねずみとおなじ）"), ("🖥️", "screen", "がめん"),
        ("📱", "smartphone", "スマホ"), ("🤖", "robot", "ロボット"),
        ("🌐", "internet", "インターネット"), ("📧", "email", "メール"), ("🎮", "game", "ゲーム"),
        ("🐛", "bug", "バグ（むしとおなじ）"), ("💡", "idea", "アイデア"), ("🔋", "battery", "でんち"),
    ]),
]

# アルファベットは文字の名前で読ませる。単語と音声が混ざらないよう、読み上げ文を別に持つ
LETTER_NAMES = ("エー ビー シー ディー イー エフ ジー エイチ アイ ジェー ケー エル エム "
                "エヌ オー ピー キュー アール エス ティー ユー ブイ ダブリュー エックス ワイ ズィー").split()
LETTERS = [(f"{c} {c.lower()}", c, name, f"[[char LTRL]]{c}[[char NORM]]")
           for c, name in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", LETTER_NAMES)]
PAGES += [("ABC A〜M", LETTERS[:13]), ("ABC N〜Z", LETTERS[13:])]


def audio_uri(word: str, speech: str) -> str:
    # macOS はファイル名の大文字小文字を区別しないので、文字の音声は別名にする
    name = ("letter_" if speech != word else "") + word.replace(" ", "_")
    m4a = AUDIO_DIR / f"{name}.m4a"
    if not m4a.exists():
        aiff = AUDIO_DIR / f"{name}.aiff"
        subprocess.run(["say", "-v", "Samantha", "-r", "150", "-o", str(aiff), speech], check=True)
        subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", "-b", "64000", str(aiff), str(m4a)], check=True)
    return "data:audio/mp4;base64," + base64.b64encode(m4a.read_bytes()).decode()


WORD_HINTS = {
    "listen": "カードをおすと、英語でしゃべるよ",
    "quiz": "英語でなんていう？ いえたら「こたえ」をおしてね",
    "pick": "おとをきいて、あっている えをえらんでね",
}
PHRASE_HINTS = {
    "listen": "えをおすと、ぶんが かわって しゃべるよ",
    "quiz": "？？？のところを いれて、ぶんを ぜんぶ いってみよう",
    "pick": "ぶんをきいて、あっている えをえらんでね",
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
PWA_HOME = '<a class="home" href="./">🏠 もどる</a>'


def build(title: str, pages_src, hints: dict, notes: dict, name: str, labeled: frozenset = frozenset()) -> None:
    AUDIO_DIR.mkdir(exist_ok=True)
    plain = lambda s: s.replace("{", "").replace("}", "")
    speeches = {plain(x[1]): (x[3] if len(x) > 3 else plain(x[1])) for _, items in pages_src for x in items}
    unknown = set(notes) - set(speeches)
    assert not unknown, f"notes のキーがカードに無い: {unknown}"
    audio = {w: audio_uri(w, s) for w, s in sorted(speeches.items())}
    pages = [{"title": t, "words": [list(x[:3]) for x in items], "labels": t in labeled} for t, items in pages_src]
    data = (
        "const PAGES = " + json.dumps(pages, ensure_ascii=False) + ";\n"
        "const AUDIO = " + json.dumps(audio) + ";\n"
        "const HINTS = " + json.dumps(hints, ensure_ascii=False) + ";\n"
        "const NOTES = " + json.dumps(notes, ensure_ascii=False) + ";\n"
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
    from phrases import LABELED_PAGES, PHRASE_PAGES

    build("えいごカード", PAGES, WORD_HINTS, WORD_NOTES, "words")
    build("えいごでいおう", PHRASE_PAGES, PHRASE_HINTS, PHRASE_NOTES, "phrases", frozenset(LABELED_PAGES))
    build_pwa_shell()
