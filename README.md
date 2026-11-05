# erabu-vn — 「選ぶ」を主題にした短編ノベルゲーム

『二枚の紙』のソース。放課後の掲示板に紙が二枚あって、どちらかにしか名前を書けない話。計画そのものは作者の手元の doc にあり、ここは器と脚本だけを持つ。

- エンジン: Pixi'VN（`@drincs/pixi-vn`）＋ ink（`@drincs/pixi-vn-ink`）＋ React テンプレ（create-pixi-vn 2.2.0 の `visual-novel-ink`・Web 版）
- 脚本: `ink/*.ink`。エンドの knot は `ending_` で始める（test がエンドとして数える）
- 物差し: 30 分・分岐 2・エンド 2・立ち絵 1 人（表情 3）・背景 3・BGM 2・全年齢
- テンプレ由来の指示は `AGENTS.md`（エンジンの作法・生成物 `*.gen.*` は手で直さない）

## 動かす

```bash
npm ci --include=optional   # lockfile は Win/Linux/Mac の optional を保ったまま
npm run dev                 # http://localhost:5173
npm test                    # 脚本の網羅（tests/story.test.ts）
npm run build               # tsc -b → vite build（dist/）
npm run build:itch          # itch.io の配布物 erabu-itch.zip（相対パス・経路はメモリ・PWA なし）
```

## 段

- ✅ P0 器を起こした（2026-11-03）
- ✅ P1 仮の脚本（ink 40 行）で最後まで通る・全分岐の test が緑・2 つの枝ともブラウザでエンドまで通した（2026-11-03）
- ✅ P2 脚本（2026-11-04）— `ink/start.ink` 1 本・1 周 約 10,000 字。声 4 つも本文も Claude の文章（`docs/story/outline.md`）
- ✅ P3 絵と音（2026-11-04）— 生成の絵と自作の BGM に差し替え、テンプレの見本は全部外した。1 本目は生成の絵のまま出して開示する
- P4 出す — Vercel の別プロジェクト＋itch.io。X と note で 1 本知らせる

## 罠

- itch.io は iframe のサブパスで動く。hash の経路でも URL がルートへ書き換わって相対パスが壊れたので、`--mode itch` の経路はメモリに持つ
- 作者の環境の全体 ignore が `*.jpg` `*.png` を無視する。素材は `.gitignore` の `!` で戻してある。新しい置き場を作ったら `.gitignore` にも足す（無いと clone から build できない）
- 立ち絵は API の透過が効かず、背景が市松の「絵」で返る。切り抜きは `scripts/art/compose.py`。表情は頭だけ差し替えて胸から下は土台のまま（体が動かない）
- 何も出ていない所に最初の背景を `with fade` で出すと描かれない。最初の 1 枚は fade 無しで出し、2 枚目からの差し替えは fade でよい（2026-11-03 にブラウザで確かめた）
- test は ink を直に走らせず、pixi-vn-ink の変換器が理解した label の図を歩く（エンジンが実際に見る形）。条件分岐など歩き方を知らない step が出たら「歩き方を足す」で落ちるので、その時に `tests/story.test.ts` を広げる
- テンプレの `.github/workflows/release.yml`（Roves でタグから desktop・Steam・mobile を作る）は外した。Web と itch.io だけなら要らない。要るようになったら create-pixi-vn のテンプレから持ってくる

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
