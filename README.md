# 実行手順

### 1. Dockerのインストール
公式サイトからDocker Desktopをダウンロード。
https://docs.docker.com/get-started/get-docker/

`docker --version`を実行してバージョンが表示されればOK。

### 2. 実行環境の構築
```
docker build -t my-image .
docker run --gpus "device=0" -it --name my-container my-image /bin/bash
```
`my-image`と`my-container`は好きな名前で良い。

### 3. アプリの実行
```
streamlit run main.py
```