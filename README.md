# Stock Radar Daily

HTML/CSS/JavaScript だけで動く、注目銘柄スクリーナーです。

## 構成
- `index.html`: 画面
- `styles.css`: デザイン
- `app.js`: スクリーニングロジック

## ローカル起動
`index.html` をブラウザで開くだけで動きます。

## 公開（GitHub Pages）
このリポジトリには Pages デプロイワークフローを追加済みです。

1. GitHub リポジトリ `Settings` → `Pages`
2. `Build and deployment` の `Source` を `GitHub Actions` に変更
3. `main` に push すると自動デプロイ

公開URL例:
- `https://akama-byte.github.io/-demo/`

## 仕様
- スクリーニング条件
  - 最低株価
  - 最低時価総額
  - 最低出来高倍率
  - 上位表示件数
- 「サンプルデータ再生成」で相場変動を擬似生成
- 投資助言ではない旨をUIに明記

## 注意
本アプリの情報は教育・参考用途です。投資判断はご自身で行ってください。
