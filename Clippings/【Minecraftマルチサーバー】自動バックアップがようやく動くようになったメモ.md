---
title: "【Minecraftマルチサーバー】自動バックアップがようやく動くようになったメモ"
source: "https://qiita.com/zawanume/items/17bcb08cbdf2aa90dc11"
author:
  - "[[Qiita]]"
published: 2024-12-01
created: 2025-05-17
description: "cronの仕様がよくわからずに苦戦していたMinecraftマルチサーバーの自動バックアップ実装について、ようやく実現できたのでメモしておく。まずググってそのまま動かしてみる「Minecraft…"
tags:
  - "clippings"
---
cronの仕様がよくわからずに苦戦していたMinecraftマルチサーバーの自動バックアップ実装について、ようやく実現できたのでメモしておく。

## まずググってそのまま動かしてみる

「 [Minecraftサーバをscreenとcronでプラグインを使わずに自動再起動する](https://jyn.jp/minecraft-server-auto-restart/) 」から引用。バックアップ部分を追加。

world\_backup.sh

```bash
#!/bin/bash

WAIT=60
STARTSCRIPT=/home/hoge/Minecraft_server/start.sh
SCREEN_NAME='minecraft'

screen -p 0 -S ${SCREEN_NAME} -X eval 'stuff "say '${WAIT}'秒後にサーバーを再起動します\015"'
screen -p 0 -S ${SCREEN_NAME} -X eval 'stuff "say すぐに再接続可能になるので、しばらくお待ち下さい\015"'

sleep $WAIT
screen -p 0 -S ${SCREEN_NAME} -X eval 'stuff "stop\015"'

cd /mnt/hoge/world_backup
DIR=\`date '+%Y%m%d_%H%M'\`
tar -zcvf $DIR.tar.gz -C /home/hoge/Minecraft_server world

while [ -n "$(screen -list | grep -o "${SCREEN_NAME}")" ]
do
  sleep 1
done

$STARTSCRIPT
```

サーバー起動スクリプトはこのようにした。

start.sh

```bash
#!/bin/bash

screen -S minecraft java -XX:+UseBiasedLocking -XX:+DisableExplicitGC -XX:+UseTLAB -Xms2G -Xmx2G -XX:TargetSurvivorRatio=90 -XX:SurvivorRatio=8 -XX:MaxTenuringThreshold=4 -XX:-UseParallelGC -XX:-UseParallelOldGC -XX:ParallelGCThreads=2 -XX:ConcGCThreads=2 -jar server.jar nogui
```

毎朝6時に実行するよう「crontab -e」で設定する。

```text
0 6 * * * /home/hoge/Minecraft_server/world_backup.sh
```

翌朝、 **動いてない** 。

## cronの環境変数を設定してみる

cronでスクリプトを実行する際に、ユーザーが持つ環境変数を使うのではなくcronデーモンが独自に環境変数を持っている。 `$SHELL` が `/bin/sh` だったり、 `$PATH` が `/bin` と `/usr/bin` にしか通ってなかったりなかなか貧弱であるので、自分で設定する。これも、「crontab -e」で設定できる。

```text
SHELL = /bin/bash
HOME = /home/hoge
PATH = /usr/bin:/bin:/usr/local/bin:/usr/sbin:/sbin:/usr/local/sbin

0 6 * * * $HOME/Minecraft_server/world_backup.sh
10 6 * * * $HOME/Minecraft_server/start.sh
```

ついでに `$HOME` も設定する。また、原因の切り分けのためサーバー起動スクリプトを分離しておく。そのため、 `world_backup.sh` の `$STARTSCRIPT` 行はコメントアウトする。cronの実行結果をメールで受け取るため、postfixをインストールする。とりあえずはLocal onlyでよい。また、Debianではデフォルトでcronのログが出なくなっているので、 `/etc/rsyslog.conf` のcron行のコメントアウトを外し、cronを再起動する。

翌朝、 **動いた形跡はあるが働いていない** 。

## 処理の順序を変え、起動時にscreenにアタッチしない

`/var/spool/mail/hoge` を覗いてみると、「tar: world: file changed as we read it」とある。どうやらサーバーがセーブを終える前にtarが走っているらしい。低スペなのでセーブが遅い。  
そこで、tarでバックアップする処理とwhileでループさせる処理を逆にしてみる。

world\_backup.sh

```bash
#!/bin/bash

WAIT=60
# STARTSCRIPT=$HOME/Minecraft_server/start.sh
SCREEN_NAME='minecraft'

screen -p 0 -S ${SCREEN_NAME} -X eval 'stuff "say '${WAIT}'秒後にサーバーを再起動します\015"'
screen -p 0 -S ${SCREEN_NAME} -X eval 'stuff "say すぐに再接続可能になるので、しばらくお待ち下さい\015"'

sleep $WAIT
screen -p 0 -S ${SCREEN_NAME} -X eval 'stuff "stop\015"'

while [ -n "$(screen -list | grep -o "${SCREEN_NAME}")" ]
do
  sleep 1
done

cd /mnt/hoge/world_backup
DIR=\`date '+%Y%m%d_%H%M'\`
tar -zcvf $DIR.tar.gz -C $HOME/Minecraft_server world

# $STARTSCRIPT
```

また、同じく `/var/spool/mail/hoge` に、「Must be connected to a terminal」とある。検索をかけると、同じ問題に悩む人を多く見つけたが、解決法は見つけられなかった。原因は単純で、screenを起動するとアタッチしたままになってしまい、cronがコマンドの実行に成功したか判断できなくなってしまうためだ。起動時にアタッチしない「-md」オプションを記述して解決した。また、サーバーのjarファイルのパスを丁寧丁寧丁寧に記述した。

start.sh

```bash
#!/bin/bash

screen -md -S minecraft java -XX:+UseBiasedLocking -XX:+DisableExplicitGC -XX:+UseTLAB -Xms2G -Xmx2G -XX:TargetSurvivorRatio=90 -XX:SurvivorRatio=8 -XX:MaxTenuringThreshold=4 -XX:-UseParallelGC -XX:-UseParallelOldGC -XX:ParallelGCThreads=2 -XX:ConcGCThreads=2 -jar $HOME/Minecraft_server/server.jar nogui
```

翌朝、 **バックアップは成功したがサーバーが起動していない** 。

## カレントディレクトリ

原因を探ろうとサーバーにssh接続したら、あることに気づいた。ホームディレクトリ直下にサーバーの設定ファイルが生成されていた。原因は単純で、cronに登録したstart.shはカレントディレクトリ `$HOME=/home/hoge` で作業をする。スクリプトの中で `$HOME/Minecraft_server` の中のjarを起動するが、カレントディレクトリは `$HOME` のままなので、 `$HOME` の直下で設定ファイルを探す。探しても見当たらないため、サーバーは初回起動時と同じ挙動を見せるのだ。 `start.sh` を今一度書き換えて解決した。

start.sh

```bash
#!/bin/bash

cd $HOME/Minecraft_server

screen -md -S minecraft java -XX:+UseBiasedLocking -XX:+DisableExplicitGC -XX:+UseTLAB -Xms2G -Xmx2G -XX:TargetSurvivorRatio=90 -XX:SurvivorRatio=8 -XX:MaxTenuringThreshold=4 -XX:-UseParallelGC -XX:-UseParallelOldGC -XX:ParallelGCThreads=2 -XX:ConcGCThreads=2 -jar server.jar nogui
```

翌朝、 **無事成功** 。

## バックアップは大切だ

`world_backup.sh` の `$STARTSCRIPT` 行のコメントアウトを外し、 `start.sh` をcronから外しておく。  
これで毎朝6時に勝手にバックアップを取るようになった。快適なマイクラライフ、と言いたいところだが、私は受験生なのである。
