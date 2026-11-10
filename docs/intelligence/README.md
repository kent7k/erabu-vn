---
title: erabu-vn『二枚の紙』Repository Intelligence（統合版）
tags: [erabu-vn, repository-intelligence]
owner: 未割当（Q-11）
last-reviewed: 2026-11-09
source: erabu-vn-main.zip（sha256 43852b88…8fe4）
---

# erabu-vn『二枚の紙』Repository Intelligence（統合版）

短編ノベルゲーム『二枚の紙』（Pixi'VN＋ink＋React。ブラウザだけで動く）を、コードから読み解いた文書の一式を 1 本にまとめたものです。すべての主張に `path:line` の根拠を付けました。

- 基準：zip の sha256 `43852b88d2d3d72291469920f2c2697c31870ab13f7d8cfbe1af4c6e8ac58fe4`（`.git` が無いので commit は不明）
- 調べた日：2026-11-09
- 確度：Confirmed／Corroborated／Inferred／Unknown（決め方は [根拠の索引（要約）](00-overview.md#根拠の索引要約)）

各文書のリスクと未確認の事項は ID だけを書きました。中身は [リスクの台帳](70-reliability.md#リスクの台帳全部) と [未確認の事項](99-evidence-and-questions.md#未確認の事項全部) に 1 回だけ載せています。

## 目的ごとの読む順

| 目的 | 読む順 |
|---|---|
| 新しく入った人が全体をつかむ | [全体の要約（Executive Summary）](00-overview.md#全体の要約executive-summary) → [システムの全体像](10-architecture.md#システムの全体像) → [シーケンス図](40-runtime.md#シーケンス図) → [エンティティの一覧（ゲームの中身を含む）](30-data.md#エンティティの一覧ゲームの中身を含む) |
| 変更の前に影響を調べる | [変更の影響（代表の 8 つ）](80-change-impact.md#変更の影響代表の-8-つ) → [依存の図](80-change-impact.md#依存の図) → [契約の互換のリスク](20-api-and-auth.md#契約の互換のリスク) → [test とリリースの計画](80-change-impact.md#test-とリリースの計画) |
| 問い合わせ・障害の一次切り分け | [runbook の一覧](90-runbooks.md#runbook-の一覧) → 各 runbook → [障害モードの分析（FMEA）](70-reliability.md#障害モードの分析fmea) |
| 設計のリスクを評価する | [リスクの台帳（全部）](70-reliability.md#リスクの台帳全部) → [未確認の事項（全部）](99-evidence-and-questions.md#未確認の事項全部) |
| 出す（P4）前 | [build と配る経路（デプロイのパイプライン）](50-infrastructure.md#build-と配る経路デプロイのパイプライン) → [RB-05 リリースと戻し（Vercel・itch）](90-runbooks.md#rb-05-リリースと戻しvercelitch) → [環境ごとの違い](50-infrastructure.md#環境ごとの違い) |

## 目次

- **00 Overview**：[全体の要約（Executive Summary）](00-overview.md#全体の要約executive-summary) ・ [調査計画（Discovery Plan）](00-overview.md#調査計画discovery-plan) ・ [根拠の索引（要約）](00-overview.md#根拠の索引要約)
- **10 Architecture**：[システムの全体像](10-architecture.md#システムの全体像) ・ [C4 Context（システムの境界）](10-architecture.md#c4-contextシステムの境界) ・ [C4 Container（実行の単位と置き場）](10-architecture.md#c4-container実行の単位と置き場) ・ [C4 Component（SPA の中の部品）](10-architecture.md#c4-componentspa-の中の部品) ・ [部品の一覧（Component Catalog）](10-architecture.md#部品の一覧component-catalog)
- **20 API and Auth**：[契約の一覧（API Catalog の置き換え）](20-api-and-auth.md#契約の一覧api-catalog-の置き換え) ・ [契約の中身（API Contracts の置き換え）](20-api-and-auth.md#契約の中身api-contracts-の置き換え) ・ [エラーの一覧](20-api-and-auth.md#エラーの一覧) ・ [契約の互換のリスク](20-api-and-auth.md#契約の互換のリスク) ・ [認証と認可（無いことの確認と、信頼の境界）](20-api-and-auth.md#認証と認可無いことの確認と信頼の境界) ・ [セキュリティのリスクの一覧（Auth Risk Register の置き換え）](20-api-and-auth.md#セキュリティのリスクの一覧auth-risk-register-の置き換え)
- **30 Data**：[データのモデル](30-data.md#データのモデル) ・ [エンティティの一覧（ゲームの中身を含む）](30-data.md#エンティティの一覧ゲームの中身を含む) ・ [データの持ち主（誰が読み、誰が書くか）](30-data.md#データの持ち主誰が読み誰が書くか) ・ [データの一生（作る・残す・消す）](30-data.md#データの一生作る残す消す) ・ [データの移行と互換のリスク](30-data.md#データの移行と互換のリスク)
- **40 Runtime**：[実行時の流れ](40-runtime.md#実行時の流れ) ・ [シーケンス図](40-runtime.md#シーケンス図) ・ [イベントの一覧](40-runtime.md#イベントの一覧) ・ [バッチと定期の処理](40-runtime.md#バッチと定期の処理)
- **50 Infrastructure**：[基盤の全体像](50-infrastructure.md#基盤の全体像) ・ [ネットワークと公開の範囲](50-infrastructure.md#ネットワークと公開の範囲) ・ [build と配る経路（デプロイのパイプライン）](50-infrastructure.md#build-と配る経路デプロイのパイプライン) ・ [環境ごとの違い](50-infrastructure.md#環境ごとの違い) ・ [復旧の考え方（RTO・RPO の根拠）](50-infrastructure.md#復旧の考え方rtorpo-の根拠)
- **60 Operations（観測）**：[観測できる所の地図](60-operations.md#観測できる所の地図) ・ [ログの一覧（console）](60-operations.md#ログの一覧console) ・ [metric と alert の一覧](60-operations.md#metric-と-alert-の一覧) ・ [観測の足りない所](60-operations.md#観測の足りない所)
- **70 Reliability**：[障害モードの分析（FMEA）](70-reliability.md#障害モードの分析fmea) ・ [影響の範囲（Blast Radius）](70-reliability.md#影響の範囲blast-radius) ・ [リスクの台帳（全部）](70-reliability.md#リスクの台帳全部)
- **80 Change Impact**：[変更の影響（代表の 8 つ）](80-change-impact.md#変更の影響代表の-8-つ) ・ [依存の図](80-change-impact.md#依存の図) ・ [test とリリースの計画](80-change-impact.md#test-とリリースの計画)
- **90 Runbooks**：[runbook の一覧](90-runbooks.md#runbook-の一覧) ・ [RB-01 起動するとエラー画面になる／「つづきから」が押せない](90-runbooks.md#rb-01-起動するとエラー画面になるつづきからが押せない) ・ [RB-02 セーブとロードができない](90-runbooks.md#rb-02-セーブとロードができない) ・ [RB-03 設定がおかしい（オートが勝手にオン・音が出ない・文字の大きさ）](90-runbooks.md#rb-03-設定がおかしいオートが勝手にオン音が出ない文字の大きさ) ・ [RB-04 itch 版が表示されない（真っ白・素材が出ない）](90-runbooks.md#rb-04-itch-版が表示されない真っ白素材が出ない) ・ [RB-05 リリースと戻し（Vercel・itch）](90-runbooks.md#rb-05-リリースと戻しvercelitch) ・ [RB-06 「オフライン」の全画面で進めない](90-runbooks.md#rb-06-オフラインの全画面で進めない) ・ [RB-07 素材を作り直す（絵・BGM・アイコン）](90-runbooks.md#rb-07-素材を作り直す絵bgmアイコン)
- **99 Evidence and Questions**：[未確認の事項（全部）](99-evidence-and-questions.md#未確認の事項全部) ・ [根拠の索引（全部）](99-evidence-and-questions.md#根拠の索引全部) ・ [用語集](99-evidence-and-questions.md#用語集)
