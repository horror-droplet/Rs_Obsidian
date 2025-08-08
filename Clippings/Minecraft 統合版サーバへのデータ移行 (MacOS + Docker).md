---
title: "Minecraft 統合版サーバへのデータ移行 (MacOS + Docker)"
source: "https://qiita.com/wyetea/items/0dea7688e8ceb9756445"
author:
  - "[[Qiita]]"
published: 2021-07-25
created: 2025-05-17
description: "(2021.07.25 バージョンアップについて追記)#はじめにWindows 10 Minecraft 統合版 (Redblock 版) （以下マイクラ）で遊んでいたワールドを自前サーバに移行…"
tags:
  - "clippings"
---
(2021.07.25 バージョンアップについて追記)

## はじめに

Windows 10 Minecraft 統合版 (Redblock 版) （以下マイクラ）で遊んでいたワールドを自前サーバに移行する（ほぼ自分用の）メモです。サーバは MacOS 上で Docker を利用して稼働させてます。確かめていませんが、Linux でサーバを動かしている場合もほぼ同様だと思います。

マイクラは一緒に遊んでいればマルチプレイができますので、わざわざサーバを建てる必要はないのですが、自分が不在の時にも同じワールドで遊びたい、と自分の子供に言われ、調べたところ自宅で電源入れっぱなしにしている Mac でマイクラサーバを建てられるのを知りました。Realms というサービスを使うと同じことができますが、それなりな金額です（マイクラのためにその額は毎月払えない）。で、サーバは簡単に構築でき、ワールドの移行が必要になったのでやってみた、というのが背景です。

MacOS + Docker でのマイクラサーバ構築は Qiita の 「 [Minecraft PE統合版サーバをDocker for Macで起動、バックアップ、レストア](https://qiita.com/kawanet/items/d212429836e7944ef36b) 」を参考にし、ほぼその通りに稼働させました。もし、同じことをやりたい方でまだサーバを建てていない方は、そちらを参考にしてください。特に難しい点はありません。利用した Docker image は [https://hub.docker.com/r/itzg/minecraft-bedrock-server](https://hub.docker.com/r/itzg/minecraft-bedrock-server) です。ちなみにこれまで Singularity は仕事で使ったことがありましたが Docker はこのマイクラサーバ建てで初めて触りました（で、一部ハマりました。それについては最後に書いておきました）。

## データ移行

## データのエクスポートと転送

まず移行したいマイクラのワールドをエクスポートします。ワールド一覧の鉛筆アイコンをクリックして、下の方にスクロールすると「エクスポート」ボタンがありますので、適当な場所に保存します。ワールドのファイルは `.mcworld` という拡張子のファイルになります。このファイルは Zip ファイルなので、拡張子を `.zip` に変更すれば解凍（展開）できます。ファイルをサーバの動いているマシンにコピーして解凍しておきます。解凍すると `world` というディレクトリができます。自分はファイルの移動が面倒なのでエクスポートする際に OneDrive に保存して MacOS 側では Web 版 OneDrive 経由でダウンロードしました。USB メモリなどでコピーしてももちろん良いでしょう。

## サーバの停止

ワールドデータの移行前にサーバを停止します。上述の Docker イメージを利用している場合は、 `docker-composer.yml` のあるディレクトリで

```text
docker-compose stop
```

を実行すれば停止します。以下、同じディレクトリで作業することを仮定します。

## ファイルの準備

サーバの (Docker コンテナ内の) ディレクトリ `/data/worlds/Redblock level/` が、ワールドのデータですので、エクスポートしたワールドデータを解凍した際にできたディレクトリ (`world`) を同名のディレクトリとしてコピーすればデータ移行は OK です。ただしサーバは Docker で動いていますのでローカルのファイルを Docker 内にコピーする必要があります。これには何通りか方法があります。ここでは２通りの方法を書いておきます。

### 方法１: docker cp を利用

`docker cp` コマンドを使うとローカル環境にあるファイルを Docker コンテナ内にコピーできます。このコマンドの使用方法は

```sh
docker cp コピーしたいファイル コンテナ名:コピー先ディレクトリ
```

です。コピーの手間を減らすために、ローカルに `worlds` というディレクトリを作成し、エクスポートしたワールドデータのディレクトリ (`world`) をこの下に移動し、そのディレクトリ名を `Redblock level` に変更します。ディレクトリ構成としては下記のようになります。

```text
worlds/
  Redblock level/
    db/
    level.dat
    levelname.txt
    world_icon.jpg
```

そして `docker cp` で `worlds` ごとコンテナ内にコピーしてしまいます。コンテナ名は `プロジェクト名_bds_1` とかになっていると思います。上述の Qiita 記事に従っていれば `minecraft-bedrock-server_bds_1` です。

```sh
docker cp worlds minecraft-bedrock-server_bds_1:/data/
```

これでワールドデータをコンテナ内にコピーできます。

### 方法２: docker run 経由

一時的に必要なディレクトリをマウントしたコンテナを `docker run --it -rm` で実行してファイルをコピーする方法です。 `-v` オプションで、ローカルファイルや、Docker ボリュームをマウントできます。上述の Qiita 記事に従っていれば、 `minecraft-bedrock-server_bds` というボリュームが作られて、それがコンテナ内では `/data` としてマウントされます。上記方法１と同じようにファイルを用意しておけば

```sh
docker run -it --rm -v minecraft-bedrock-server_bds:/data -v ${PWD}:/dump \
 debian cp -r /dump/worlds /data/
```

でワールドのデータをサーバ用コンテナのボリュームにコピーできます。 `-v ${PWD}:/dump` オプションで、カレントディレクトリがコンテナ内の `/dump` にマウントされますので `/dump/worlds` で、上で用意したワールドのデータが入ったディレクトリにアクセスできます。これを `/data/` にコピーしています。

## サーバー起動

コピーができたら、

```sh
docker-compose restart
```

で、サーバを起動すれば移行完了です。

## ハマりポイント

自分は Docker をちゃんと理解していなかったため、 `docker-composer.yml` を置くディレクトリ名を上述の Qiita の記事から変更してしまって、記事通りにファイルコピーがうまくいかなくて時間を溶かしました。このディレクトリ名が Docker の「プロジェクト名」として使われます。サーバのデータの保存される Docker ボリューム名は `プロジェクト名_bds` に、コンテナ名は `プロジェクト名_bds_1` になります。

Docker ボリュームを覗くには

```sh
docker run -it --rm -v minecraft-bedrock-server_bds:/data debian ls /data
```

でできますが、 `worlds` ディレクトリがちゃんとあれば、ボリューム名はあっています。  
ちなみにボリュームの一覧は

```sh
docker volume ls
```

で、できます。存在しないボリューム名を指定すると空のボリュームができてしまいますので注意してください（自分はボリューム名が最初わからず大量に空ボリュームを作ってしまいました）。また `docker volume inspect ボリューム名` で、ボリュームを確認できます。以下、実行結果の例です（一部伏せています）。（最初の `$` はプロンプト）

```sh
$ docker volume inspect minecraft-bedrock-server_bds
[
    {
        "CreatedAt": "2021-XX-XXTXX:XX:XXZ",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.project": "minecraft",
            "com.docker.compose.version": "1.27.4",
            "com.docker.compose.volume": "bds"
        },
        "Mountpoint": "/var/lib/docker/volumes/minecraft-bedrock-server_bds/_data",
        "Name": "minecraft-bedrock-server_bds",
        "Options": null,
        "Scope": "local"
    }
]
```

## バージョンアップ

Minecraft 本体がバージョンアップしたりすると古いバージョンのサーバに接続できなくなってしまいます。その時は 一旦 `docker-compose stop` で停止し `docker-compose start` でスタートさせれば、サーバ起動時に自動的にサーバ最新版をチェックし、最新版があればアップデートされます。

## エラー対応

今の時点で出会ったエラー（ワーニング）とその対応方法（１つだけですが）をメモしておきます。

## アップデートに失敗する

```text
WARN Minecraft download page failed, so using existing download of X.X.X.X
```

これが出る時は、サーバのダウンロードサイトの URL が変わるなどして、最新版のサーバパッケージをダウンロードできないときに表示されるようです（ダウンロードサイトが落ちていることもありました）。その場合は Docker イメージが古くなっていますので、最新イメージにアップデートしてから起動するとうまく行くようです。イメージのアップデートには `docker pull` コマンドを使用します。

```sh
$ docker pull itzg/minecraft-bedrock-server
```

以上になります。

## 参考サイト

- [Qiita「Minecraft PE統合版サーバをDocker for Macで起動、バックアップ、レストア」](https://qiita.com/kawanet/items/d212429836e7944ef36b)
- [Qiita 「dockerコンテナにファイルを転送する」](https://qiita.com/buntafujikawa/items/04c3bdd93ac3520c53eb)
- [Docker Compose入門 (4) ～ネットワークの活用とボリューム～](https://knowledge.sakura.ad.jp/26522/)
- [docker-composeでプロジェクト名を変更する](https://incrementleaf.net/articles/docker-compose-change-project-name/)
- [Minecraft Server Docker Image by itzg](https://hub.docker.com/r/itzg/minecraft-bedrock-server)

[0](https://qiita.com/wyetea/items/#comments)

新規登録して、もっと便利にQiitaを使ってみよう

1. あなたにマッチした記事をお届けします
2. 便利な情報をあとで効率的に読み返せます
3. ダークテーマを利用できます
[ログインすると使える機能について](https://help.qiita.com/ja/articles/qiita-login-user)

[新規登録](https://qiita.com/signup?callback_action=login_or_signup&redirect_to=%2Fwyetea%2Fitems%2F0dea7688e8ceb9756445&realm=qiita) [ログイン](https://qiita.com/login?callback_action=login_or_signup&redirect_to=%2Fwyetea%2Fitems%2F0dea7688e8ceb9756445&realm=qiita)

[2](https://qiita.com/wyetea/items/0dea7688e8ceb9756445/likers)

2