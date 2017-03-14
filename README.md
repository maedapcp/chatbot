# chatworkbot (for android)

## コマンド一覧
### ヘルスチェック
```
[To:XXXX] hello
```

### APK 作成
```
[To:XXXX] build android origin/master
```

## スタートガイド
### 1. Python 3 インストール
お手元の環境に[インストール](https://www.python.org)ください。

### 2. venv 準備
```
$ python3 -m venv .venv/chatbot
$ . .venv/chatbot/bin/activate
```

### 3. chatwork クライアントをインストール
```
$ pip install git+https://github.com/maedapcp/chatwork-for-python.git
```

### 4. chatbot 本体を配置
```
$ git clone https://github.com/maedapcp/chatbot.git
```

### 5. 必要な情報を設定
```
$ vi chatbot.ini
[chatwork]
key = アクセスキー
room = 待ち受ける部屋

[git]
repo = リポジトリのパス

[publishing]
port = 8000
```

### 6. 一旦 venv を抜ける
```
$ deactivate
```

### 7. 次から一発で起動
```
$ . ~/.venv/chatbot/bin/activate && cd ~/chatbot && python chatbot.py &
```

### 8. kill で停止
本体を停止すると一緒に HTTP サーバーも停止します。
```
$ kill `ps -ef | grep -e chatbot | grep -v grep | awk '{print $2;}'`
```
