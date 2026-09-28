"""えいごでいおう の文。{} で囲んだところが、絵で入れかわる語。"""

# 絵だけでは意味が決まらないページ。カードに日本語を小さく添える
LABELED_PAGES = {"あいさつ"}

PHRASE_PAGES = [
    ("あいさつ", [
        ("☀️", "Good morning.", "おはよう"), ("🌙", "Good night.", "おやすみ"),
        ("👋", "Hello!", "こんにちは"), ("🚶", "See you!", "またね"),
        ("🙏", "Thank you.", "ありがとう"), ("😊", "You're welcome.", "どういたしまして"),
        ("🙇", "I'm sorry.", "ごめんなさい"), ("🆗", "That's OK.", "いいよ"),
        ("🍽️", "Let's eat!", "いただきます"), ("❓", "What's this?", "これ何？"),
        ("🆘", "Help me!", "助けて"), ("🎂", "Happy birthday!", "お誕生日おめでとう"),
    ]),
    ("好き I like", [
        ("🍎", "I like {apples}.", "りんごが好き"), ("🍌", "I like {bananas}.", "バナナが好き"),
        ("🐱", "I like {cats}.", "猫が好き"), ("🐶", "I like {dogs}.", "犬が好き"),
        ("🍰", "I like {cake}.", "ケーキが好き"), ("🍦", "I like {ice cream}.", "アイスが好き"),
        ("🚃", "I like {trains}.", "電車が好き"), ("📖", "I like {books}.", "本が好き"),
        ("🎮", "I like {games}.", "ゲームが好き"), ("🏊", "I like {swimming}.", "泳ぐのが好き"),
        ("🎵", "I like {music}.", "音楽が好き"), ("🐧", "I like {penguins}.", "ペンギンが好き"),
    ]),
    ("きらい I don't like", [
        ("🕷️", "I don't like {spiders}.", "クモはきらい"), ("🐛", "I don't like {bugs}.", "虫はきらい"),
        ("🌧️", "I don't like {rain}.", "雨はきらい"), ("🥕", "I don't like {carrots}.", "にんじんはきらい"),
        ("🍅", "I don't like {tomatoes}.", "トマトはきらい"), ("🫑", "I don't like {green peppers}.", "ピーマンはきらい"),
        ("⚡", "I don't like {thunder}.", "雷はきらい"), ("🐍", "I don't like {snakes}.", "ヘビはきらい"),
        ("💉", "I don't like {shots}.", "注射はきらい"), ("🌑", "I don't like {the dark}.", "暗いのはきらい"),
        ("🔊", "I don't like {loud noises}.", "大きい音はきらい"), ("👻", "I don't like {ghosts}.", "おばけはきらい"),
    ]),
    ("気持ち I'm", [
        ("😄", "I'm {happy}.", "うれしい"), ("😢", "I'm {sad}.", "悲しい"),
        ("😠", "I'm {angry}.", "怒ってる"), ("🤤", "I'm {hungry}.", "おなかすいた"),
        ("😪", "I'm {sleepy}.", "眠い"), ("😩", "I'm {tired}.", "疲れた"),
        ("🥵", "I'm {hot}.", "暑い"), ("🥶", "I'm {cold}.", "寒い"),
        ("😱", "I'm {scared}.", "怖い"), ("🤩", "I'm {excited}.", "わくわくする"),
        ("🥱", "I'm {bored}.", "退屈"), ("🤒", "I'm {sick}.", "具合が悪い"),
    ]),
    ("したい I want to", [
        ("🎲", "I want to {play}.", "遊びたい"), ("🍽️", "I want to {eat}.", "食べたい"),
        ("😴", "I want to {sleep}.", "寝たい"), ("🏠", "I want to {go home}.", "家に帰りたい"),
        ("🏊", "I want to {swim}.", "泳ぎたい"), ("📖", "I want to {read a book}.", "本を読みたい"),
        ("🎨", "I want to {draw a picture}.", "絵をかきたい"), ("📺", "I want to {watch TV}.", "テレビを見たい"),
        ("🛝", "I want to {go to the park}.", "公園に行きたい"), ("🛁", "I want to {take a bath}.", "お風呂に入りたい"),
        ("👵", "I want to {see Grandma}.", "おばあちゃんに会いたい"), ("🚲", "I want to {ride a bike}.", "自転車に乗りたい"),
    ]),
    ("ちょうだい Can I have", [
        ("💧", "Can I have {some water}?", "お水ちょうだい"), ("🥛", "Can I have {some milk}?", "牛乳ちょうだい"),
        ("🧃", "Can I have {some juice}?", "ジュースちょうだい"), ("🍵", "Can I have {some barley tea}?", "麦茶ちょうだい"), ("🍪", "Can I have {a cookie}?", "クッキーちょうだい"),
        ("🍌", "Can I have {a banana}?", "バナナちょうだい"), ("🍬", "Can I have {some candy}?", "あめちょうだい"),
        ("🍞", "Can I have {some bread}?", "パンちょうだい"), ("🍚", "Can I have {some rice}?", "ご飯ちょうだい"),
        ("➕", "Can I have {one more}?", "もう一つちょうだい"), ("🤗", "Can I have {a hug}?", "ぎゅってして"),
        ("🤧", "Can I have {a tissue}?", "ティッシュちょうだい"), ("✏️", "Can I have {a pencil}?", "鉛筆ちょうだい"),
    ]),
    ("しよう Let's", [
        ("🎲", "Let's {play a game}!", "ゲームしよう"), ("🚶", "Let's {go}!", "行こう"),
        ("🎤", "Let's {sing}!", "歌おう"), ("💃", "Let's {dance}!", "踊ろう"),
        ("🏃", "Let's {run}!", "走ろう"), ("🍳", "Let's {cook}!", "料理しよう"),
        ("🎨", "Let's {draw}!", "絵をかこう"), ("📸", "Let's {take a picture}!", "写真をとろう"),
        ("🧱", "Let's {build something}!", "何か作ろう"), ("🔍", "Let's {look for it}!", "探そう"),
        ("🍿", "Let's {watch a movie}!", "映画を見よう"), ("🛏️", "Let's {go to bed}!", "寝よう"),
    ]),
    ("できる I can", [
        ("🏊", "I can {swim}.", "泳げる"), ("🏃‍♀️", "I can {run fast}.", "速く走れる"),
        ("🦘", "I can {jump high}.", "高く跳べる"), ("🚲", "I can {ride a bike}.", "自転車に乗れる"),
        ("🍳", "I can {cook}.", "料理できる"), ("🔟", "I can {count to ten}.", "10まで数えられる"),
        ("✍️", "I can {write my name}.", "名前が書ける"), ("🎤", "I can {sing}.", "歌える"),
        ("🤸", "I can {do a cartwheel}.", "側転できる"), ("👟", "I can {tie my shoes}.", "靴ひもが結べる"),
        ("🔤", "I can {read English}.", "英語が読める"), ("🧩", "I can {do puzzles}.", "パズルができる"),
    ]),
    ("どこ Where is", [
        ("🎒", "Where is {my bag}?", "私のかばんどこ？"), ("👟", "Where are {my shoes}?", "私の靴どこ？"),
        ("🐱", "Where is {the cat}?", "猫はどこ？"), ("👩", "Where is {Mom}?", "お母さんはどこ？"),
        ("👨", "Where is {Dad}?", "お父さんはどこ？"), ("🚽", "Where is {the bathroom}?", "トイレはどこ？"),
        ("✏️", "Where is {my pencil}?", "私の鉛筆どこ？"), ("⚽", "Where is {the ball}?", "ボールはどこ？"),
        ("🔑", "Where is {the key}?", "鍵はどこ？"), ("📖", "Where is {my book}?", "私の本どこ？"),
        ("🚉", "Where is {the station}?", "駅はどこ？"), ("🧸", "Where is {my teddy bear}?", "私のくまのぬいぐるみどこ？"),
    ]),
    ("〜だね It's", [
        ("🔥", "It's {hot}.", "暑いね"), ("❄️", "It's {cold}.", "寒いね"),
        ("🐘", "It's {big}.", "大きいね"), ("🐜", "It's {small}.", "小さいね"),
        ("🐰", "It's {cute}.", "かわいいね"), ("😋", "It's {yummy}.", "おいしいね"),
        ("👻", "It's {scary}.", "怖いね"), ("🤣", "It's {funny}.", "おもしろいね"),
        ("🌸", "It's {beautiful}.", "きれいだね"), ("🚀", "It's {fast}.", "速いね"),
        ("🏋️", "It's {heavy}.", "重いね"), ("🌧️", "It's {raining}.", "雨が降ってるね"),
    ]),
]
