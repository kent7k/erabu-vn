# erabu-vn — 「選ぶ」を主題にした短編ノベルゲーム

『二枚の紙』のソース。放課後の掲示板に紙が二枚あって、どちらかにしか名前を書けない話。計画そのものは作者の手元の doc にあり、ここは器と脚本だけを持つ。

- エンジン: Pixi'VN（`@drincs/pixi-vn`）＋ ink（`@drincs/pixi-vn-ink`）＋ React テンプレ（create-pixi-vn 2.2.0 の `visual-novel-ink`・Web 版）
- 脚本: `ink/*.ink`。エンドの knot は `ending_` で始める（test がエンドとして数える）
- 物差し: 30 分・分岐 2・エンド 2・立ち絵 1 人（表情 3＋基本）・場所 3（背景の画像 9）・BGM 2・全年齢
- テンプレ由来の指示は `AGENTS.md`（エンジンの作法・生成物 `*.gen.*` は手で直さない）。Distribution と VS Code の節は外した `release.yml`・Roves を前提にしたままで、今の構成と合わない（R-13）
- 設計の全体（構成・データ・実行時・配る経路・観測・リスク・runbook）は [`docs/intelligence/`](docs/intelligence/README.md)。コードを静的に読んだ文書で、主張ごとに `path:line` の根拠がある（基準は 2026-11-09・この repo の 2026-11-05 の公開の版）

## 動かす

Node は 22.12 以上（vite 8・vitest 5 の engines の下限。repo では版を固定していない）。

```bash
npm ci --include=optional   # lockfile は Win/Linux/Mac の optional を保ったまま（prebuild の sharp もこれで入る）
npm run dev                 # http://localhost:5173
npm test                    # 脚本の網羅（tests/story.test.ts）と、設定の保存・URL の query の小さな test
npm run check               # biome（lint＋format の検査）
npm run build               # prebuild（アイコン）→ tsc -b → vite build（dist/・base は /・経路は history・PWA あり）
npm run preview             # vite build だけ（tsc なし）→ vite preview
npm run build:itch          # itch.io の配布物 erabu-itch.zip（dist-itch/・相対パス・経路はメモリ・PWA なし・tsc も prebuild も走らない）
```

### 遊ぶ側の仕組み

- キー: F5／Ctrl+S でクイックセーブ（タイトルでは効かない）・F9／Ctrl+L でクイックロード・Esc で設定・K で操作の一覧・H で履歴・Tab でクイックアクション・Enter／Space で送り（押している間はスキップ）・↑↓ で選択肢・F8 で診断（`src/lib/hooks/hotkeys-hooks.ts`）
- 置き場は全部遊ぶ人のブラウザで、サーバーへ送るデータは無い。手動とクイックのセーブは IndexedDB `game_db` の `saves`、ページを隠したときの自動セーブは localStorage `auto_exit_save`（`/` 以外の URL で開いたときだけ戻す・「つづきから」もこれを見る）、音量・テーマ・言語などの設定も localStorage
- セーブに版の確かめは無い。ink の行や knot を直してセーブの互換を壊すときは `package.json` の version を上げる（セーブの gameVersion に入る）
- 不具合の手掛かりは F8 の診断の「コピー」だけ（エラーは作者に届かない）。問い合わせには、遊んでいる所・F8 のコピー・開いた URL の `?` のあと・場面・直前の操作を聞いて、[runbook](docs/intelligence/90-runbooks.md#runbook-の一覧) で切り分ける

## 段

- ✅ P0 器を起こした（2026-11-03）
- ✅ P1 仮の脚本（ink 40 行）で最後まで通る・全分岐の test が緑・2 つの枝ともブラウザでエンドまで通した（2026-11-03）
- ✅ P2 脚本（2026-11-04）— `ink/start.ink` 1 本・1 周 約 10,000 字。声 4 つも本文も Claude の文章（`docs/story/outline.md`）
- ✅ P3 絵と音（2026-11-04）— 生成の絵と自作の BGM に差し替え、テンプレの見本は全部外した。1 本目は生成の絵のまま出して開示する
- P4 出す — Vercel の別プロジェクト＋itch.io。X と note で 1 本知らせる。出す前に決めることと確かめることは下の「出す前に」

## 罠

- itch.io は iframe のサブパスで動く。hash の経路でも URL がルートへ書き換わって相対パスが壊れたので、`--mode itch` の経路はメモリに持つ
- 作者の環境の全体 ignore が `*.jpg` `*.png` を無視する。素材は `.gitignore` の `!` で戻してある。新しい置き場を作ったら `.gitignore` にも足す（無いと clone から build できない）
- 立ち絵は API の透過が効かず、背景が市松の「絵」で返る。切り抜きは `scripts/art/compose.py`。表情は頭だけ差し替えて胸から下は土台のまま（体が動かない）
- 何も出ていない所に最初の背景を `with fade` で出すと描かれない。最初の 1 枚は fade 無しで出し、2 枚目からの差し替えは fade でよい（2026-11-03 にブラウザで確かめた）
- test は ink を直に走らせず、pixi-vn-ink の変換器が理解した label の図を歩く（エンジンが実際に見る形）。条件分岐など歩き方を知らない step が出たら「歩き方を足す」で落ちるので、その時に `tests/story.test.ts` を広げる
- テンプレの `.github/workflows/release.yml`（Roves でタグから desktop・Steam・mobile を作る）は外した。Web と itch.io だけなら要らない。要るようになったら create-pixi-vn のテンプレから持ってくる
- `build:itch` は `tsc -b` を通らない。itch 版だけ出すときも、先に `npm run build` か `npx tsc -b` を 1 回走らせる
- `dist-itch/` と `erabu-itch.zip` は ignore してある。itch の戻しは前の zip を上げ直すしかないので、出した zip は手元に控える
- `vercel.json` の rewrite は素材の path にも効く。無い素材を引くと 404 でなく index.html（200）が返り、Pixi の読み込みが分かりにくい失敗をする（漏れは test が見る）
- `vercel.json` に installCommand が無く、`package.json` に `"latest"` の依存が 9 個ある。Vercel の Install Command は `npm ci --include=optional` に固定する（R-10）
- Service Worker は plugin の既定のまま登録される（`registerSW` を呼ぶコードは無い）。更新を出しても前の版が出続けうるので、確かめるときは全部のタブを閉じて開き直す（R-28）。precache は JS・CSS・HTML・アイコンだけで、絵と音は入れていない（全部の解像度と形式を入れると約 22 MB）。代わりに `/assets/` を実行時に CacheFirst で控えるので、1 度読んだ絵と音はオフラインでも出る（R-09）
- TanStack Query は既定（networkMode "online"）だとオフラインで再取得を止める。画面のデータは全部エンジンの手元の状態なので `src/App.tsx` で `"always"` にしてある。戻すとオフラインでクリックしても台詞が変わらなくなる
- PWA の `start_url` は `/`。Vercel の根に置く前提で、サブパスに置くと合わない

## 出す前に

### 決めること（作者の手）

- Q-01 Vercel の本番のプロジェクト（URL・ドメイン・Build／Install Command・Node の版）
- Q-03 ink を直したあと、古いセーブを戻すとどうなるか（手元の dev で試せる）
- Q-11 出したあと、不具合の報告を誰がどこで受けるか

ほかの未確認（Q-02・Q-12 など。Q-09 は上の罠の precache の行で答えた）は [未確認の事項](docs/intelligence/99-evidence-and-questions.md#未確認の事項全部)。

### 確かめること（P4 の前に 1 回、そのあとは毎回）

1. `npm ci --include=optional`
2. `npm test`・`npm run check`
3. `npm run build` → `npm run preview` で手元で開く
4. はじめから → 左の紙 → エンド。もう 1 回、右の紙 → エンド
5. セーブ → タイトル → ロード。F5 → F9。タブを隠す → 開き直す → つづきから
6. `npm run build:itch` → itch の下書きのページに上げ、iframe の中で 4〜5 をくり返す
7. セーブの互換を壊すときは `package.json` の version を上げる

手順と戻し方は [RB-05](docs/intelligence/90-runbooks.md#rb-05-リリースと戻しvercelitch)。

## 既知の課題（Medium・2026-11-10 に HEAD で確かめた）

直した（2026-11-10）:

- R-01 通信が切れるとゲームが止まる → 原因は 2 つあった。全画面の「オフライン」の表示と、TanStack Query がオフラインで画面のデータの取り直しを止めること（エンジンは進むのに台詞が変わらない）。表示は上に出る閉じられる帯にし、Query は `networkMode: "always"` にした。あわせて絵と音を実行時に控える（R-09）。build して preview で、オフラインに見せかけて（`navigator.onLine` と offline のイベント）帯が出て閉じられ、クリックで進むことと、2 回目の読み込みで絵と音が `game-assets-v1` に入ることを確かめた。本当に回線を切っての確認はまだ

- R-02 オート送りが読み直すとオンに戻る → `=== "true"` で読む。クイックツールの切り替えも保存して設定画面とそろえた（`tests/auto-settings.test.ts`）
- R-27 URL に知らない query が付くと進まない → Q-16 を手元の dev で確かめたら、`/?utm_source=x` から「はじめから」で 1 行目のまま止まり背景も出なかった（High だった）。store に入れる query を `settings`・`settings_tab`・`history`・`saves` の 4 つに絞った（`src/lib/stores/search-param-store.ts`・`tests/search-params.test.ts`）。直したあと、同じ URL で進むことと設定の開け閉めをブラウザで確かめた

残りを直す順は R-03・R-04 → R-11・R-10 → R-05 → R-12。Low の 19 件を含む全部は [リスクの台帳](docs/intelligence/70-reliability.md#リスクの台帳全部)。

| ID | 何が起きるか | 直し方の要旨 |
|---|---|---|
| R-03 | `auto_exit_save` が壊れていると、`/` 以外の URL で開いたときにエラー画面。「つづきから」も押せない | parse を try で囲み、失敗したら鍵を消す |
| R-04 | IndexedDB の失敗の経路で Promise が終わらない／例外が漏れる（保存中の toast が残る） | どの失敗でも reject して return。tx の onerror・onabort も扱う |
| R-11 | CI が無く、test・lint・型の検査は手で走らせるだけ | push ごとに ci → test → check → build の workflow を 1 本足す |
| R-10 | `"latest"` の依存と、Vercel の入れ方が決まっていない | lockfile の版に固定。Install Command を固定する |
| R-05 | セーブの版を確かめないので、ink を直したあとに古いセーブが壊れうる | restore の前に gameVersion を比べて警告する。互換の方針を先に決める |
| R-12 | 出したあと、遊ぶ人の環境で起きたエラーが作者に届かない | 告知に「F8 の診断を貼ってください」と書く。送る仕組みは同意と一緒に考える |

## 素材を作り直す

```bash
python3 scripts/art/gen_art.py --out <dir>          # 絵の原本（OpenAI の画像 API・OPENAI_API_KEY・原本は repo に置かない）
python3 scripts/art/gen_art.py --out <dir> --face   # 先輩の表情 3 つ
python3 scripts/art/compose.py --src <dir> --font <ZenKurenaido-Regular.ttf>   # src/assets と public/icon.png を組む（掲示板の字はここで描く）
python3 scripts/art/gen_bgm.py --out <dir>          # BGM 2 曲（numpy で合成）。mp3 にして src/assets/audio へ
npm run icon                                        # favicon と PWA のアイコン
```

## ライセンス

コードは GPL-3.0（`LICENSE`）で、テンプレ（create-pixi-vn）から引き継いだ。エンジン（`@drincs/pixi-vn`）は LGPL-2.1。
脚本・絵・音楽は GPL の対象外で、転載と再配布は許可していない。
絵は OpenAI の画像生成（`gpt-image-2`）の仮で、BGM は `scripts/art/gen_bgm.py` の合成（サンプル不使用）。掲示板の字のフォントは Zen Kurenaido（SIL OFL）で、ビットマップに焼くだけでフォント自体は入れない。
