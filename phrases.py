"""えいごでいおう の文。{} で囲んだところが、絵で入れかわる語。"""

# 絵だけでは意味が決まらないページ。カードに日本語を小さく添える
LABELED_PAGES = {"あいさつ", "アニメでよく聞く", "ディズニーの歌", "歌の形で言おう", "体の動き", "物を動かす",
                 "場面 飛行機", "場面 ハンバーガー屋", "場面 タクシー・お店"}

# 場面のページ。聞かれる（店員さんの声）→ 答える が交互に並ぶ
DIALOG_PAGES = {"場面 飛行機", "場面 ハンバーガー屋", "場面 タクシー・お店"}

PHRASE_PAGES = [
    ("あいさつ", [
        ("☀️", "Good morning.", "おはよう"), ("🌙", "Good night.", "おやすみ"),
        ("👋", "Hello!", "こんにちは"), ("🚶", "See you!", "またね"),
        ("🙏", "Thank you.", "ありがとう"), ("😊", "You're welcome.", "どういたしまして"),
        ("🙇", "I'm sorry.", "ごめんなさい"), ("🆗", "That's OK.", "いいよ"),
        ("🍽️", "Let's eat!", "いただきます"), ("❓", "What's this?", "これ何？"),
        ("🆘", "Help me!", "助けて"), ("🎂", "Happy birthday!", "お誕生日おめでとう"),
    ]),
    ("アニメでよく聞く", [
        ("😱", "Oh no!", "しまった！"), ("🤕", "Are you OK?", "大丈夫？"),
        ("😮", "What happened?", "どうしたの？"), ("👀", "Look!", "見て！"),
        ("✋", "Wait!", "待って！"), ("👉", "Come on!", "ほら、行こう！"),
        ("⚠️", "Watch out!", "危ない！"), ("💡", "I got it!", "わかった！"),
        ("👍", "Good job!", "よくできたね！"), ("🙋", "Me too.", "私も。"),
        ("😲", "Really?", "ほんと？"), ("🤷", "I don't know.", "わからない。"),
    ]),
    # 曲名がそのまま英語の言い回しになっているもの。歌詞は著作権があるので入れない（曲名だけ）
    ("ディズニーの歌", [
        ("❄️", "Let it go.", "もういいの・手放そう"), ("⛄", "Do you want to build a snowman?", "雪だるま つくらない？"),
        ("🍂", "Into the unknown", "知らない世界へ"), ("🧞", "A whole new world", "まったく新しい世界"),
        ("🐠", "Under the sea", "海の中"), ("🤠", "You've got a friend in me.", "ぼくが友だちだよ"),
        ("🌟", "When you wish upon a star", "星に願いをかけるとき"), ("🌊", "How far I'll go", "どこまで行けるかな"),
        ("🎸", "Remember me.", "私をおぼえていて"), ("🌹", "Beauty and the Beast", "美女と野獣"),
        ("🤫", "We don't talk about Bruno.", "ブルーノの話はしないの"), ("🏰", "Someday my prince will come.", "いつか王子様が来る"),
    ]),
    # 上の曲名と同じ形で、ふだん使う文にしたもの。{} が 曲名から入れかえたところ
    ("歌の形で言おう", [
        ("⚽", "Do you want to {play soccer}?", "サッカーしない？"),
        ("🎈", "Let {the balloon} go.", "風船を はなして"),
        ("🌲", "Let's go into {the forest}.", "森の中に 入ろう"),
        ("🍕", "A whole {pizza}!", "ピザ まるごと！"),
        ("🛏️", "It's under {the bed}.", "ベッドの下に あるよ"),
        ("🧸", "I've got {a new friend}.", "新しい友だちが できたよ"),
        ("🦅", "I wish I could {fly}.", "飛べたら いいのに"),
        ("🚉", "How far is {the station}?", "駅まで どのくらい？"),
        ("📝", "Remember {your homework}.", "宿題を わすれないでね"),
        ("📚", "We don't talk {in the library}.", "図書館では しゃべらないよ"),
        ("🚀", "Someday I will {go to space}.", "いつか 宇宙に行く"),
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
        ("🤧", "Can I have {a tissue}?", "ティッシュちょうだい"),
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
    # 場面: 外国で 聞かれること と その答え。左が 聞かれる、右が 答える
    ("場面 飛行機", [
        ("🍗", "Beef or chicken?", "聞かれる：牛肉と鶏肉、どっち？"), ("🐔", "Chicken, please.", "答える：鶏肉をください"),
        ("🥤", "Something to drink?", "聞かれる：何か飲む？"), ("🧃", "Apple juice, please.", "答える：りんごジュースをください"),
        ("🪟", "Window or aisle?", "聞かれる：窓側と通路側、どっち？"), ("💺", "Window, please.", "答える：窓側をください"),
        ("🛂", "Passport, please.", "聞かれる：パスポートを見せてください"), ("🤲", "Here you are.", "答える：はい、どうぞ"),
        ("❓", "What's the purpose of your visit?", "聞かれる：旅行の目的は？"), ("📸", "Sightseeing.", "答える：観光です"),
        ("📅", "How long will you stay?", "聞かれる：何日いますか？"), ("🗓️", "One week.", "答える：1週間です"),
    ]),
    ("場面 ハンバーガー屋", [
        ("🧑‍🍳", "Can I help you?", "聞かれる：ご注文は？"), ("🍔", "A hamburger, please.", "答える：ハンバーガーをください"),
        ("🥤", "What size?", "聞かれる：サイズは？"), ("📏", "Medium, please.", "答える：Mサイズをください"),
        ("🍟", "Would you like fries?", "聞かれる：ポテトはいかが？"), ("👍", "Yes, please.", "答える：はい、お願いします"),
        ("🏠", "For here or to go?", "聞かれる：ここで食べる？持ち帰る？"), ("🛍️", "To go, please.", "答える：持ち帰ります"),
        ("➕", "Anything else?", "聞かれる：ほかには？"), ("🙆", "That's all.", "答える：それで全部です"),
        ("💵", "That's five dollars.", "聞かれる：5ドルです"), ("💰", "Here you go.", "答える：はい、どうぞ"),
    ]),
    ("場面 タクシー・お店", [
        ("🚕", "Where to?", "聞かれる：どちらまで？"), ("🏨", "To the hotel, please.", "答える：ホテルまでお願いします"),
        ("📍", "Here we are.", "聞かれる：着きましたよ"), ("🙏", "Thank you very much.", "答える：ありがとうございました"),
        ("👀", "Are you looking for something?", "聞かれる：何かお探しですか？"), ("🙂", "I'm just looking.", "答える：見ているだけです"),
        ("👗", "Do you want to try it on?", "聞かれる：試着しますか？"), ("🙋", "Yes, I do.", "答える：はい、します"),
        ("🛍️", "Do you need a bag?", "聞かれる：袋はいりますか？"), ("🙅", "No, thank you.", "答える：いいえ、けっこうです"),
        ("💳", "Cash or card?", "聞かれる：現金とカード、どっち？"), ("💴", "Cash, please.", "答える：現金で"),
    ]),
    # 動詞＋小さい言葉。反対どうしを となりに置いて、up / down・on / off の感じをつかむ
    ("体の動き", [
        ("🧍", "stand up", "立つ"), ("🪑", "sit down", "座る"),
        ("🌅", "get up", "起きる"), ("🛌", "lie down", "寝ころぶ"),
        ("⏰", "wake up", "目を覚ます"), ("😴", "go to sleep", "寝る"),
        ("🚪", "come in", "入る"), ("🏃", "go out", "出かける"),
        ("🔙", "come back", "戻ってくる"), ("👋", "go away", "あっちへ行く"),
        ("⏩", "hurry up", "急ぐ"), ("😌", "calm down", "落ち着く"),
    ]),
    ("物を動かす", [
        ("🧥", "put on", "着る・つける"), ("👕", "take off", "脱ぐ・外す"),
        ("💡", "turn on", "（電気を）つける"), ("🌑", "turn off", "（電気を）消す"),
        ("🫴", "pick up", "拾う"), ("⬇️", "put down", "置く"),
        ("👀", "look at", "見る"), ("🔍", "look for", "探す"),
        ("🧹", "clean up", "片づける"), ("🗑️", "throw away", "捨てる"),
        ("🤲", "give back", "返す"), ("👗", "try on", "試着する"),
    ]),
]
