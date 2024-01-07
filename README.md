# Schedulus

Googleカレンダーから当日の予定一覧を取得し、クリップボードでコピーします。

## 環境構築

このプロジェクトはPython 3.7以上を必要とします。

1. まず初めに、このリポジトリをクローンまたはダウンロードしてください。

```
    git clone git@github.com:yourusername/schedulus.git
```

2. Pythonの仮想環境をセットアップします。以下のコマンドで仮想環境を作成し、有効化します：

```
    python3 -m venv env
    source env/bin/activate
```

3. 必要なパッケージをインストールします：

```
    pip install -r requirements.txt
```

4. 設定情報

    config.jsonファイルを作成します。  
    config.example.jsonを参考に、Google Cloudの認証情報と参照するカレンダーIDを含めて必要な情報を記入してください。
    ```
    cp config.example.json config.json
    vi config.json
    ```

## 使用方法

以下のコマンドで実行します：

```
    python main.py
```
