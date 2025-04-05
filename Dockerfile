# Docker Hubからubuntuのイメージを取得
# Docker HubはDockerの公式レジストリで、イメージを公開・共有できる
# gpuを使うために、nvidiaのcudaイメージを使用
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# 非対話モード（aptでエラー出さないように）
ENV DEBIAN_FRONTEND=noninteractive

# 必要なパッケージをインストール（ここでは簡単にpythonとpipとgitだけ）
# apt cleanでキャッシュを削除
# 容量を小さくするため、基本的にキャッシュは残さない
RUN apt update && apt install -y \
    wget \
    python3 \
    python3-pip \
    git \
&& apt clean

# 作業ディレクトリの指定
WORKDIR /workspace

# ホストのカレントディレクトリをコンテナの作業ディレクトリにコピー
# Docker Desktopは裏でLinuxの仮想マシンを動かしているので、
# 作業ディレクトリはLinuxのファイルシステムで管理される
COPY . /workspace

# 必要なパッケージをインストール
RUN pip install -r requirements.txt
RUN git clone https://github.com/facebookresearch/sam2.git
RUN cd sam2 && pip install . && cd ..

# AIモデルのダウンロード
RUN wget https://dl.fbaipublicfiles.com/segment_anything_2/092824/sam2.1_hiera_tiny.pt -O sam2/checkpoints/sam2.1_hiera_tiny.pt