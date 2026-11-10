> [erabu-vn『二枚の紙』Repository Intelligence](README.md) の一部。基準は 2026-11-09 の zip（README の source）で、`path:line` はその時点の行。

# 99 Evidence and Questions

## 未確認の事項（全部）

コードと設定だけでは決められなかったことです。それぞれに、なぜ大事か・どう確かめるか・判断への影響（High・Medium・Low）を付けました。High の 2 つ（Q-01・Q-03）は、出す（P4）前に確かめてください。

<!-- BEGIN:questions -->
| ID | Question | Why it matters | How to verify | 判断への影響 | 関連 |
|---|---|---|---|---|---|
| Q-01 | Vercel の本番のプロジェクト（URL・独自ドメイン・Build/Install Command・Node の版）はもうあるか | デプロイとロールバックの runbook（RB-05）の前提。P4 はまだ済んでいない（README:26） | Vercel のダッシュボードで、Project Settings の General と Build & Development を見る | High | R-10, RB-05 |
| Q-02 | itch.io のページの設定（Embed のサイズ・全画面ボタン・itch のアプリで遊べるか） | iframe での動き（README:30）とオフライン表示（R-01）の影響の範囲が決まる | itch の Edit game の Embed options を見る。itch のアプリでオフラインのとき起動してみる | Medium | R-01, RB-04 |
| Q-03 | ink を直したあとに古いセーブを restoreGameState するとどうなるか | 更新のたびに遊ぶ人のセーブが壊れるかが決まる（R-05） | v0.1.0 でセーブ → ink の途中に行を足す → 同じセーブをロードし、画面と console を見る | High | R-05, 82 |
| Q-04 | Assets.backgroundLoadBundle("start") など、無い bundle の名前を渡すと警告や例外が出るか | R-21 の重さが決まる | npm run dev で「はじめから」を押し、DevTools の console を見る | Low | R-21 |
| Q-05 | isNativeBuild = !ROVES_BUILD は意図どおりか（テンプレの元でも同じか） | Web 版の素材の重さと画質が決まる（R-08） | create-pixi-vn 2.2.0 の visual-novel-ink の .assetpack.ts と見比べる | Low | R-08 |
| Q-06 | @tanstack/hotkeys の "K" は Ctrl+K でも発火するか | R-14 の直し方が決まる | npm run dev で Ctrl+K と K を押して比べる（devtools の Hotkeys パネルでも見られる） | Low | R-14 |
| Q-07 | ホイールの向き（上で進む・下で戻る）は意図どおりか | 遊ぶ人の感覚と合うか。テンプレの既定かどうか | 作者に聞く。テンプレの quick-tools-hooks と見比べる | Low | R-15 |
| Q-08 | エンドまで読んだあと、auto_exit_save を消すべきか | エンドのあとの「つづきから」の振る舞いが決まる（R-24） | 作者に聞く | Low | R-24 |
| Q-09 | build した dist/sw.js の precache に、public/assets の webp・jpg・mp3 が入っているか | PWA でオフラインのとき遊べるかが決まる（R-09） | npm run build のあと、dist/sw.js の precacheAndRoute の一覧を見る | Medium | R-09, R-01 |
| Q-10 | 物語の英語版を出す予定はあるか（en を選べるのに narration が空） | 言語の切り替えを残すか消すかが決まる | 作者に聞く。予定が無ければ supportedLngs から en を外すかを決める | Low | i18n |
| Q-11 | 出したあと、遊ぶ人からの不具合の報告を誰がどこで受けるか | runbook の Escalation と、観測の足りない所（R-12）の埋め方が決まる | 作者に聞く（README:26 では X と note で知らせる予定） | Medium | R-12, 90 |
| Q-12 | Vercel の build で prebuild（pwa-assets-generator の sharp）と optional の依存が入るか | Vercel の build が通るかが決まる（R-10） | Vercel の Preview で 1 回 build し、ログを見る | Medium | R-10, RB-05 |
| Q-13 | Roves・Steam の機能（achievement・roves のセーブ・終了ボタン）を残すか | 使っていないコード（ink から # unlock achievement を呼んでいない）を保守し続けるかが決まる | 作者に聞く。出すのが Web と itch だけなら外すかを決める | Low | hashtag-commands |
| Q-14 | 生成した絵であることを、作品ページとエンドのあとでどう開示するか | README の方針（README:25,51）を出すときに満たせるか | 作品ページの文案を確かめる。エンドのあとの画面に開示の文があるか、ink で確かめる | Low | R-25 |
| Q-15 | 1 周したときの auto_exit_save は何 KB になるか | localStorage の容量（ふつう 5MB）に収まるか（R-07） | 遊んでから DevTools の Application → Local Storage で、auto_exit_save の長さを見る | Low | R-07 |
| Q-16 | /?utm_source=x のように知らない query を付けて開き、「はじめから」を押したあとに、クリックで進めるか | R-27 が本当に起きるか。出すときの告知の link に効く | npm run dev で http://localhost:5173/?utm_source=x を開き、はじめから → クリック。devtools の Router パネルで search を見る | High | R-27 |
<!-- END:questions -->

### 確かめ方の種類

| 種類 | 当たる ID |
|---|---|
| 作者に聞く | Q-07・Q-08・Q-10・Q-11・Q-13・Q-14 |
| 手元で `npm run dev`／`build` して見る | Q-03・Q-04・Q-06・Q-09・Q-15 |
| 配る所の画面を見る | Q-01・Q-02・Q-12 |
| テンプレの元と見比べる | Q-05・Q-07 |

## 根拠の索引（全部）

`tools/check.py` が、各行の範囲に決めた文字列（needle）があることを確かめています。行番号は zip（sha256 43852b88…8fe4）の中身に対してだけ正しいです。同じ中身は `.system-intelligence/evidence.jsonl` にもあります。

（数は [根拠の索引（要約）](00-overview.md#根拠の索引要約) を見てください）

<!-- BEGIN:evidence -->
| ID | Claim | Evidence | Confidence |
|---|---|---|---|
| E-001 | Pixi'VN の canvas を 1920x1080・contain で body に作る | `src/main.tsx:21-27` | Confirmed |
| E-002 | canvas に UI レイヤー、sound に bgm/sfx チャンネルを足し、音量を localStorage から戻す | `src/main.tsx:29-36` | Confirmed |
| E-003 | React は Pixi'VN の HTML レイヤー（#root）に描く | `src/main.tsx:44-49` | Confirmed |
| E-004 | ゲームの終わり（END）で Game.clear() して / に戻る | `src/main.tsx:52-55` | Confirmed |
| E-005 | エラーは canvas への描画、toast、console.error だけで、外部への送信はない | `src/main.tsx:57-61` | Confirmed |
| E-006 | label を読み込むたびに label id と同じ名前の bundle を裏で読み込もうとする | `src/main.tsx:63` | Confirmed |
| E-007 | itch モードでは経路をメモリ（createMemoryHistory）に持つ | `src/App.tsx:9-12` | Confirmed |
| E-008 | router.tsx の getRouter は App.tsx から使われていない（App.tsx は自前で createRouter） | `src/router.tsx:10-21` | Confirmed |
| E-009 | root の loader で content・IndexedDB・素材・i18n を並べて初期化する | `src/routes/__root.tsx:26-30` | Confirmed |
| E-010 | / 以外で始まり、まだ 1 step も進んでいなければ auto-exit セーブを戻す | `src/routes/__root.tsx:31-36` | Confirmed |
| E-011 | root で設定ダイアログとオフライン表示を常に重ねる | `src/routes/__root.tsx:52-56` | Confirmed |
| E-012 | URL の search param をそのまま SearchParams store に入れる | `src/routes/__root.tsx:23` | Confirmed |
| E-013 | 経路は / ・ /game ・ /game/narration の 3 つ | `src/routeTree.gen.ts:50` | Confirmed |
| E-014 | content/ 以下の ts/tsx を全部 eager import して、登録の副作用を起こす | `src/content/index.ts:2-4` | Confirmed |
| E-015 | 登場人物は mc・senpai・kaikei・mio・shisho の 5 人 | `src/content/characters.ts:26` | Confirmed |
| E-016 | ink のタグ命令 # navigate を足している | `src/content/ink/hashtag-commands.ts:9-23` | Confirmed |
| E-017 | ink のタグ命令 # rename を足している（characterId は zod の enum で検証） | `src/content/ink/hashtag-commands.ts:25-42` | Confirmed |
| E-018 | ink のタグ命令 # unlock achievement を Roves 経由で足している | `src/content/ink/hashtag-commands.ts:44-58` | Confirmed |
| E-019 | Pixi'VN の基本タグ命令を bundle と alias の一覧付きで登録する | `src/content/ink/hashtag-commands.ts:7` | Confirmed |
| E-020 | [characterId] を、翻訳のあとで人物名に置き換える | `src/content/ink/text-replaces.ts:4-10` | Confirmed |
| E-021 | 脚本は ink/start.ink の 1 本で、-> start から始まる | `ink/start.ink:6-8` | Confirmed |
| E-022 | 唯一の分岐は choice の knot にある 2 択 | `ink/start.ink:240-243` | Confirmed |
| E-023 | エンド 1：ending_write が END で終わる | `ink/start.ink:540-561` | Confirmed |
| E-024 | エンド 2：ending_read が END で終わる | `ink/start.ink:851-877` | Confirmed |
| E-025 | start の最初に senpai の bundle を lazyload し、最初の背景を fade 無しで出す | `ink/start.ink:9-11` | Confirmed |
| E-026 | 生成された label の一覧（choice の枝 _\|_c-0/_\|_c-1 を含む） | `src/pixi-vn.keys.gen.ts:13-25` | Confirmed |
| E-027 | bundle は audio・bg・images・senpai の 4 つ | `src/pixi-vn.keys.gen.ts:72` | Confirmed |
| E-030 | itch モードは base を相対パス ./ にする | `vite.config.ts:27` | Confirmed |
| E-031 | Pixi'VN の vite プラグインが worker・keys の生成ファイルと、素材 manifest の読み込みを持つ | `vite.config.ts:39-53` | Confirmed |
| E-032 | ink の vite プラグイン：ink/**/*.ink を public/ink-json/*.gen.json に変換する | `vite.config.ts:54-58` | Confirmed |
| E-033 | PWA は itch モードでは切る。manifest の start_url は / | `vite.config.ts:59-70` | Confirmed |
| E-034 | Service Worker の runtimeCaching は raw.githubusercontent.com だけを対象にする | `vite.config.ts:22` | Confirmed |
| E-035 | runtimeCaching は CacheFirst で 7 日 | `vite.config.ts:91-107` | Confirmed |
| E-036 | 出力先は通常 dist、itch モードは dist-itch | `vite.config.ts:126` | Confirmed |
| E-037 | AssetPack は serve では watch し、build では 1 回だけ走らせる | `vite.config.ts:160-167` | Confirmed |
| E-038 | ROVES_BUILD を build 時の定数として埋め込む | `vite.config.ts:123` | Confirmed |
| E-039 | isNativeBuild = !ROVES_BUILD（ROVES_BUILD が無い Web の build で true になる） | `.assetpack.ts:6` | Confirmed |
| E-040 | isNativeBuild のとき 0.5x の画像を作らず、WebP を quality 88 にする（コメントはネイティブ向けの意図） | `.assetpack.ts:94-99` | Confirmed |
| E-041 | AssetPack は src/assets を public/assets に出し、manifest.gen.json を書く | `.assetpack.ts:84-103` | Confirmed |
| E-042 | npm scripts：build は tsc -b → vite build、prebuild でアイコンを作り直す | `package.json:11-15` | Confirmed |
| E-043 | build:itch は rm と zip（POSIX のコマンド）で erabu-itch.zip を作る | `package.json:13` | Confirmed |
| E-044 | TanStack 系などの依存が "latest" の指定になっている | `package.json:31-34` | Confirmed |
| E-045 | devDependencies にも "latest" がある（biome・router-plugin など） | `package.json:63-71` | Confirmed |
| E-046 | vercel.json は SPA の rewrite だけで、headers・installCommand・buildCommand は無い | `vercel.json:1-3` | Confirmed |
| E-047 | vitest は vite.config を使わず、node 環境で tests/**/*.test.ts だけを走らせる | `vitest.config.ts:3-8` | Confirmed |
| E-048 | README：依存は npm ci --include=optional で入れる | `README.md:13` | Confirmed |
| E-049 | README：P4（Vercel＋itch.io で出す）はまだ済んでいない | `README.md:26` | Confirmed |
| E-050 | README：テンプレの release.yml は外した | `README.md:35` | Confirmed |
| E-051 | AGENTS.md：.vscode/ がある前提で書かれている | `AGENTS.md:42` | Confirmed |
| E-052 | AGENTS.md：release.yml でタグから release を作る前提で書かれている | `AGENTS.md:80` | Confirmed |
| E-053 | .gitignore：作者の全体 ignore に対して素材の jpg/png を ! で戻している | `.gitignore:10-13` | Confirmed |
| E-054 | 素材の生成は OpenAI の画像 API（鍵は環境変数 OPENAI_API_KEY） | `scripts/art/gen_art.py:62-66` | Confirmed |
| E-055 | BGM は numpy で合成して wav に書く | `scripts/art/gen_bgm.py:134-137` | Confirmed |
| E-056 | 素材を組むスクリプトが src/assets/bg に jpg を書く（夕方の版は色を変えて作る） | `scripts/art/compose.py:265-269` | Confirmed |
| E-060 | IndexedDB の名前は game_db、版は 2 | `src/lib/utils/db-utility.ts:4-5` | Confirmed |
| E-061 | saves の object store：keyPath は id（autoIncrement）、index は id・date・name・gameVersion | `src/lib/utils/db-utility.ts:12-22` | Confirmed |
| E-062 | putRow：store が無ければ reject() するが return せず、そのまま transaction に進む | `src/lib/utils/db-utility.ts:42-47` | Confirmed |
| E-063 | putRow：open の onerror で reject しない（Promise が終わらない） | `src/lib/utils/db-utility.ts:57-59` | Confirmed |
| E-064 | deleteRow：open の onerror で reject しない | `src/lib/utils/db-utility.ts:110-112` | Confirmed |
| E-065 | getList：limit に達して resolve したあとも cursor.continue() で最後まで歩く | `src/lib/utils/db-utility.ts:146-160` | Confirmed |
| E-066 | セーブの中身：Game.exportGameState()・gameVersion・date・name・image | `src/lib/utils/save-utility.ts:10-19` | Confirmed |
| E-067 | image を渡されなければ canvas.extractImage() のスクショを入れる | `src/lib/utils/save-utility.ts:27` | Confirmed |
| E-068 | Roves の中なら Roves のセーブ、そうでなければ IndexedDB に書く | `src/lib/utils/save-utility.ts:33-39` | Confirmed |
| E-069 | id が 0（偽）のときは save.getLast() の結果を返す | `src/lib/utils/save-utility.ts:40-43` | Confirmed |
| E-070 | 最新のセーブ：auto-exit のセーブの方が新しければそれを返す | `src/lib/utils/save-utility.ts:56-75` | Confirmed |
| E-071 | ファイルからの読み込み：JSON.parse を try で囲まず、形も版も確かめずに restore する | `src/lib/utils/save-utility.ts:109-118` | Confirmed |
| E-072 | restore は Game.restoreGameState だけで、gameVersion を見ない | `src/lib/utils/save-utility.ts:128-130` | Confirmed |
| E-073 | クイックセーブは -2〜-7 の 6 枠。空きが無ければいちばん古い枠に上書きする | `src/lib/utils/save-utility.ts:150-172` | Confirmed |
| E-074 | auto-exit のセーブは localStorage の auto_exit_save に置く | `src/lib/utils/save-utility.ts:199-209` | Confirmed |
| E-075 | autoExit.load：JSON.parse が Promise の外にある。戻せたら消し、戻せなければ Game.clear() | `src/lib/utils/save-utility.ts:212-230` | Confirmed |
| E-076 | autoExit.peek：JSON.parse を try で囲まない | `src/lib/utils/save-utility.ts:233-239` | Confirmed |
| E-077 | Roves のセーブの鍵：クイックセーブは quicksave-N、それ以外は数値の文字列 | `src/lib/utils/roves-utility.ts:14-20` | Confirmed |
| E-078 | 手動セーブの画面は 10 ページ × 6 枠（id 0〜59） | `src/components/menus/save-menu/index.tsx:16-18` | Confirmed |
| E-079 | auto-exit のセーブは beforeunload と visibilitychange(hidden) で書く。/ では書かない | `src/lib/hooks/save-hooks.tsx:177-199` | Confirmed |
| E-080 | オート送りの状態を Boolean(文字列) で戻す（"false" も true になる） | `src/lib/stores/auto-settings-store.ts:15-18` | Confirmed |
| E-081 | toggleEnabled は localStorage に "true"/"false" を書く | `src/lib/stores/auto-settings-store.ts:23-28` | Confirmed |
| E-082 | setEnabled は localStorage に書かない | `src/lib/stores/auto-settings-store.ts:33-35` | Confirmed |
| E-083 | 設定画面のスイッチは toggleEnabled を使う | `src/components/menus/settings/dialogues-controls.tsx:66` | Confirmed |
| E-084 | クイックツールのトグルは setEnabled を使う | `src/components/quick-tools.tsx:93` | Confirmed |
| E-085 | チャンネルごとの音量・ミュートを <alias>_volume / <alias>_muted に置く | `src/lib/stores/channel-sound-stores.ts:29-35` | Confirmed |
| E-086 | 全体の音量・ミュートを master_volume / master_muted に置く | `src/lib/stores/master-sound-storage.ts:16-19` | Confirmed |
| E-087 | 文字の速さと文字の大きさを localStorage に置く | `src/lib/stores/text-display-settings-store.ts:23-31` | Confirmed |
| E-088 | テーマを vite-ui-theme に置く | `src/components/providers/theme-provider.tsx:26-30` | Confirmed |
| E-089 | 言語は localStorage だけから決める。fallback は ja、対応は ja/en | `src/lib/i18n.ts:25-36` | Confirmed |
| E-090 | goNext：メニューが開いていたら何もしない。narration.continue のあと画面のデータを全部 invalidate | `src/lib/hooks/narration-hooks.ts:39-63` | Confirmed |
| E-091 | 長押し 700ms でスキップを始める | `src/lib/hooks/narration-hooks.ts:167-168` | Confirmed |
| E-092 | スキップは 100ms ごとの setInterval で goNext する | `src/lib/hooks/narration-hooks.ts:305-310` | Confirmed |
| E-093 | オート送りは autoTime 秒の debounce で goNext する | `src/lib/hooks/narration-hooks.ts:312-326` | Confirmed |
| E-094 | invalidateInterfaceData は queryClient の全 query を invalidate する | `src/lib/hooks/props-hooks.ts:18-21` | Confirmed |
| E-095 | マウスホイール：上で continue、下で back。メニューが開いているかは見ない | `src/lib/hooks/quick-tools-hooks.ts:58-66` | Confirmed |
| E-096 | ホイールは #ui か #canvas の中の操作だけを拾う | `src/lib/hooks/quick-tools-hooks.ts:41-48` | Confirmed |
| E-097 | /game でメニューが開いている間は音と canvas を止める | `src/lib/hooks/pause-game-hooks.ts:23-43` | Confirmed |
| E-098 | search param の変更を 10ms の debounce で navigate にまとめる | `src/lib/hooks/navigation-hooks.ts:12-31` | Confirmed |
| E-099 | ブラウザの戻るを打ち消す（iframe の中では何もしない） | `src/lib/hooks/navigation-hooks.ts:47-70` | Confirmed |
| E-100 | セーブのホットキー：F5・Ctrl+S でクイックセーブ、F9・Ctrl+L で最新をロード | `src/lib/hooks/hotkeys-hooks.ts:112-157` | Confirmed |
| E-101 | 操作一覧は K、診断は F8（修飾キーなし）で開く | `src/lib/hooks/hotkeys-hooks.ts:189-210` | Confirmed |
| E-102 | 履歴は H、クイックアクションの輪は Tab（修飾キーなし） | `src/lib/hooks/hotkeys-hooks.ts:239-260` | Confirmed |
| E-103 | Enter/Space を押している間はスキップ、離すと次へ | `src/lib/hooks/hotkeys-hooks.ts:343-392` | Confirmed |
| E-104 | 設定画面のキー表示は Ctrl+K | `src/components/menus/settings/quick-menus.tsx:54-57` | Confirmed |
| E-105 | 設定画面のキー表示は Ctrl+H | `src/components/menus/settings/quick-menus.tsx:129-132` | Confirmed |
| E-106 | タイトルへ戻る：確認のあと Game.clear() して / へ（セーブはしない） | `src/components/menus/settings/quick-menus.tsx:94-103` | Confirmed |
| E-107 | オフライン表示：navigator.onLine が false の間、画面全体（z-120）を覆う | `src/components/modals/error-allerts.tsx:14-21` | Confirmed |
| E-108 | オンラインかどうかは navigator.onLine と online/offline のイベントで決める | `src/lib/hooks/network-hooks.ts:8-34` | Confirmed |
| E-109 | はじめから：/game/narration に移ってから label start で Game.start する | `src/components/menus/main-menu.tsx:146-158` | Confirmed |
| E-110 | つづきから：最新が auto-exit（id -1）なら autoExit.load、そうでなければ restore | `src/components/menus/main-menu.tsx:236-252` | Confirmed |
| E-111 | タイトルの背景は images_main-menu を canvas の UI レイヤーに出す | `src/components/menus/main-menu.tsx:117-134` | Confirmed |
| E-112 | 台詞は MarkdownTypewriter に allowHtml で描く | `src/components/screens/narration/narration-cards.tsx:123-136` | Confirmed |
| E-113 | RootProvider は描画のたびに Game.onNavigate を登録する | `src/components/providers/root-provider.tsx:11-13` | Confirmed |
| E-114 | 開発の build でだけ TestingBridge を差し込む | `src/components/providers/root-provider.tsx:25` | Confirmed |
| E-115 | 診断画面：WebGL・ブラウザの機能・メモリ・FPS を読み、テキストか JSON で書き出す | `src/lib/utils/device-diagnostics-utility.ts:439-534` | Confirmed |
| E-116 | 診断はクリップボードにも写せる | `src/components/menus/settings/menus/diagnostics.tsx:75` | Confirmed |
| E-117 | 翻訳用 JSON のダウンロードは本番以外でだけ出る | `src/components/menus/settings/system-controls.tsx:187-205` | Confirmed |
| E-118 | 翻訳用 JSON は ink-manifest のパスを fetch して作る | `src/lib/i18n.ts:60-64` | Confirmed |
| E-119 | ink-manifest は絶対パス /ink-json/start.gen.json を持つ | `src/assets/ink-manifest.gen.json:1-3` | Confirmed |
| E-120 | 素材の根を BASE_URL と document.baseURI から決める（相対の base でも動く） | `src/lib/utils/assets-utility.ts:14-17` | Confirmed |
| E-121 | 起動前に images の bundle だけ待ち、audio は裏で読む | `src/lib/utils/assets-utility.ts:21-25` | Confirmed |
| E-122 | ゲームの終了ボタンは Roves の中でだけ出る | `src/lib/hooks/quit-hooks.ts:11-20` | Confirmed |
| E-123 | en.json・ja.json とも narration は空（物語の翻訳は無い） | `src/locales/en.json:1-2` | Confirmed |
| E-130 | test：全 .ink を pixi-vn-ink の変換器で label の図にする | `tests/story.test.ts:34-45` | Confirmed |
| E-131 | test：歩き方を知らない step の形が出たら落ちる | `tests/story.test.ts:24-32` | Confirmed |
| E-132 | test：参照先の label が全部ある・全経路が END で終わる・ending_ が全部届く・エンド 2 以上 | `tests/story.test.ts:129-155` | Confirmed |
| E-133 | test：脚本が指す絵・音・bundle が src/assets にある | `tests/story.test.ts:157-187` | Confirmed |
| E-134 | test：ja と en の ui の鍵が揃っている | `tests/story.test.ts:189-196` | Confirmed |
| E-140 | README の物差し：背景 3・表情 3 | `README.md:7` | Confirmed |
| E-141 | 骨子：背景は 3 枚、表情 3 | `docs/story/outline.md:22` | Confirmed |
| E-142 | README の罠：最初の背景を with fade で出すと描かれない | `README.md:33` | Confirmed |
| E-143 | README の罠：itch.io は iframe のサブパスで動く | `README.md:30` | Confirmed |
| E-144 | README：脚本・絵・音楽は GPL の対象外で、転載と再配布は許可していない | `README.md:49-51` | Confirmed |
| X-001 | @drincs/pixi-vn-ink@1.3.0 の vite プラグインは、ink JSON を virtual:pixi-vn-ink（import.meta.glob の eager と inkJsons の文字列）として bundle に埋め込む。実行時に /ink-json を fetch しない | npm: @drincs/pixi-vn-ink@1.3.0 dist/vite.mjs（load() の virtual:pixi-vn-ink）・dist/vite-listener.mjs（setupInkHmrListener） | Corroborated |
<!-- END:evidence -->

## 用語集

| 用語 | 意味（このリポジトリで） | 関連 |
|---|---|---|
| Pixi'VN | ビジュアルノベルのエンジン（`@drincs/pixi-vn`）。canvas・語り・音・状態の保存を持つ | [システムの全体像](10-architecture.md#システムの全体像) |
| ink | inkle の脚本の言語。`ink/*.ink` に書き、build で JSON にする | [エンティティの一覧（ゲームの中身を含む）](30-data.md#エンティティの一覧ゲームの中身を含む) |
| pixi-vn-ink | ink を Pixi'VN の label に変える層と、vite の plugin | X-001 |
| knot | ink の場面の単位（`=== name ===`）。Pixi'VN では label になる | [エンティティの一覧（ゲームの中身を含む）](30-data.md#エンティティの一覧ゲームの中身を含む) |
| label | Pixi'VN の場面。step の並び。選択肢の枝は `knot_|_c-N` の名前になる | `src/pixi-vn.keys.gen.ts:13-25` |
| step | label の中の 1 歩（台詞・選択肢・命令） | [実行時の流れ](40-runtime.md#実行時の流れ) |
| タグ命令（hashtag command） | ink の `# show image ...` のような行。Pixi'VN の命令になる | [契約の一覧（API Catalog の置き換え）](20-api-and-auth.md#契約の一覧api-catalog-の置き換え) |
| bundle | 素材のまとまり。`src/assets` の直下のフォルダごとに 1 つ（audio・bg・images・senpai） | `.assetpack.ts:20-46` |
| alias | 素材の呼び名。`<フォルダ>_<名前>` と `<名前>` | `.assetpack.ts:58-82` |
| AssetPack | 素材を変換して manifest を作る道具（`@assetpack/core`） | [build と配る経路（デプロイのパイプライン）](50-infrastructure.md#build-と配る経路デプロイのパイプライン) |
| auto-exit のセーブ | ページを隠すか閉じたときに localStorage の `auto_exit_save` へ書く自動のセーブ。id は -1 として扱う | [データの一生（作る・残す・消す）](30-data.md#データの一生作る残す消す) |
| クイックセーブ | F5 などで作るセーブ。id -2〜-7 の 6 枠 | `src/lib/utils/save-utility.ts:150-192` |
| つづきから | 最新のセーブ（auto-exit が新しければ auto-exit）を戻すボタン | `src/components/menus/main-menu.tsx:223-300` |
| スキップ | 100ms ごとに進む。長押し・Enter・Space を押している間 | [バッチと定期の処理](40-runtime.md#バッチと定期の処理) |
| オート送り | N 秒ごとに進む | R-02 |
| Roves | Pixi'VN のネイティブの殻（デスクトップ・Steam・スマホ）。今は使っていない | `README.md:35` |
| itch モード | `vite build --mode itch`。相対の base・メモリの経路・PWA なし | [環境ごとの違い](50-infrastructure.md#環境ごとの違い) |
| P0〜P4 | 作者の段。P4 は「出す」（まだ） | `README.md:22-26` |
| 物差し | 作者が決めた作品の大きさの決まり（30 分・分岐 2・エンド 2 など） | `README.md:7` |
| TanStack Router／Query／Store | 経路・画面のデータのキャッシュ・状態の入れ物 | [C4 Component（SPA の中の部品）](10-architecture.md#c4-componentspa-の中の部品) |
| invalidateInterfaceData | 全部の query を無効にして、画面を描き直させる関数 | `src/lib/hooks/props-hooks.ts:18-21` |
| 診断（Diagnostics） | F8 で開く、端末と描画の情報の画面 | [観測できる所の地図](60-operations.md#観測できる所の地図) |
| 確度（Confirmed など） | 根拠の強さ。[根拠の索引（要約）](00-overview.md#根拠の索引要約) を見てください | — |
