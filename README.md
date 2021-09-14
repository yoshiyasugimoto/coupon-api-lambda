# 概要

下記の要件を満たすよう実装した

1. 登録されている特定のクーポンの画像と QR コードの画像の取得をする API
2. 登録クーポンの ID、タイトル、詳細のリストを返却する API
3. 新規クーポン登録をする API

## 環境構築

```sh
git clone https://github.com/yoshiyasugimoto/coupon-api-lambda.git

npm i && poetry install
```

## デプロイ

```sh
make deploy
```

## localhost:3000 を使って API 検証

```sh
make offline_api

# 概要の1の検証
make local_get

# 概要の2の検証
make local_list
```
