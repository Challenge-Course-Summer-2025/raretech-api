# RareTECH Backend

---

## ディレクトリ構成と設計意図
このリポジトリは **FastAPI + DynamoDB** をベースに構成されており、  
責務ごとにディレクトリを分割して **保守性・拡張性** を高めています。

```css
.
├── app                  # アプリケーション本体
│   ├── api              # APIルーターとエンドポイント管理
│   ├── clients          # DynamoDBや外部APIへのリクエスト処理
│   ├── core             # 環境変数や共通処理の管理
│   ├── schemas          # リクエスト・レスポンスのバリデーション
│   ├── services         # ビジネスロジック
│   └── utils            # 共通処理やユーティリティ関数
├── Dockerfile
├── Dockerfile.prod
├── Makefile
└── docker-compose.yml
```

### 設計意図
- **責務ごとにディレクトリを分割**
  - `api/`: APIルーターやエンドポイントの定義を管理
  - `schemas/`: Pydanticモデルを定義し、入力・出力のバリデーションを行う
  - `services/`: ビジネスロジックを集約し、エンドポイントから切り離す
  - `clients/`: DynamoDBや外部APIのラッパーを置き、インフラ層と分離
  - `core/`: 環境変数や共通処理の管理
  - `utils/`: 汎用的な関数を格納

- **開発と本番環境の分離**
  - `Dockerfile`: 開発用（ホットリロード有効）
  - `Dockerfile.prod`: 本番用
  - `.env`: 環境変数で設定を切替

---

## ブランチ運用ルール
1. main : 本番環境で動いているソースコードを管理する
2. develop：開発中のソースコードを管理する
3. feature：機能実装を行う
    - 命名規則：feature/{機能名}
4. hotfix：バグ修正などの軽微な修正を行う
