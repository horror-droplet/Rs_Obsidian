---
title: "SynologyNASでのMinecraftサーバー1.20.4起ち上げから自動バックアップまで"
source: "https://clannzs.games/pages/blog/2024/02/02/pages.html"
author:
published:
created: 2025-05-17
description:
tags:
  - "clippings"
---
![[_resources/NZs │ Blog/030e3a47e3718a9e29090f13873b90a9_MD5.jpg]]

Minecraft

一年に一回くらい無性にマイクラがやりたくなって三日で飽きる。  
そんなんだから久し振りにサーバー起ち上げたらなんか動かないし当時の知識が通用しないってのを繰り返している。  
  
毎度毎度「Synology NAS マイクラサーバー」で検索しながら進めるのも疲れてきたので一度ここにまとめることにした。  
慣れると所要時間30分くらいで全部終わる。

1. [Ubuntuの導入](https://clannzs.games/pages/blog/2024/02/02/#20240202_01)
2. [Minecraft Serverの起ち上げ](https://clannzs.games/pages/blog/2024/02/02/#20240202_02)
1. [Dockerコンテナに入る](https://clannzs.games/pages/blog/2024/02/02/#20240202_02-1)
	2. [Minecraft Serverの起ち上げ](https://clannzs.games/pages/blog/2024/02/02/#20240202_02-2)
4. [自動でバックアップされるようにする](https://clannzs.games/pages/blog/2024/02/02/#20240202_03)
1. [screenをインストールしてscreen内でサーバー起動](https://clannzs.games/pages/blog/2024/02/02/#20240202_03-1)
	2. [起動スクリプトとバックアップスクリプトの作成](https://clannzs.games/pages/blog/2024/02/02/#20240202_03-2)
	3. [cronで自動化する](https://clannzs.games/pages/blog/2024/02/02/#20240202_03-3)
6. [おわりに](https://clannzs.games/pages/blog/2024/02/02/#20240202_04)

###### Ubuntuの導入

NASでのマイクラサーバー起ち上げと言えば 「itzg/docker-minecraft-server」 が有名だしこれなら一瞬で起ち上げられるのだが、 Ubuntu上で動かした方が何かと都合が良い ので今回はこちらを採用する。  
  
まず、File Stationから 「./docker/ubuntu/server」フォルダ を先んじて作成しておく。

[![[_resources/NZs │ Blog/f9ce2a227611e6df2c51193e7ca9b096_MD5.jpg]]](https://clannzs.games/contents/img/news/2024/02/02/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202024-02-02%20142816.jpg)

Container Manager（Dockerと同義）から 「ubuntu」 をダウンロードしてイメージから実行。  
執筆時点での最新バージョンは 「Ubuntu 22.04.3 LTS」 だった。  
  
リソースの制限を有効にし、CPU優先度を「高」メモリ制限を「4096」MGくらいにしてあげるとよい（ウチのNASの搭載メモリは8GB）  
実際に遊んでみてカクつくようであればメモリ制限を徐々に開放していく。

[![[_resources/NZs │ Blog/870b769528d9d7ebc974c8f044fa0343_MD5.png]]](https://clannzs.games/contents/img/news/2024/02/02/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202024-02-02%20142532.png) [![[_resources/NZs │ Blog/9e78b9a0a6c78727a11201d00904661b_MD5.png]]](https://clannzs.games/contents/img/news/2024/02/02/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202024-02-02%20142840.png)

ボリューム設定で先んじて作成しておいた「./docker/ubuntu/server」を指定「/data」フォルダをマッピングする（/dataなのはitzgサーバーを使っていた頃の名残）ネットワークを「host」へ。他は特に弄らない。

[![[_resources/NZs │ Blog/96b67ed7f2e2da3c8d24d3399b778cd4_MD5.png]]](https://clannzs.games/contents/img/news/2024/02/02/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202024-02-02%20142936.png) [![[_resources/NZs │ Blog/26ed365217dcfabf0b162f164f210b54_MD5.png]]](https://clannzs.games/contents/img/news/2024/02/02/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202024-02-02%20142954.png)

最終的にこんな感じの設定でubuntuコンテナ起ち上げ。

[![[_resources/NZs │ Blog/6a280cb31f16b59974be2a6173ca9b82_MD5.png]]](https://clannzs.games/contents/img/news/2024/02/02/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202024-02-02%20143527.png)

###### Minecraft Serverの起ち上げ

ここからは今さっき起ち上げたubuntuコンテナ内で作業するためターミナルソフトが必要になる。  
基本どれでも良いが、今回は定番ソフトの一つ「Tera Term」で作業を進めていく。  
  
Tera Term  
[https://github.com/TeraTermProject/teraterm/releases](https://github.com/TeraTermProject/teraterm/releases)

1）Dockerコンテナに入る

Tera Termを起動したらホスト名に NASのローカルIPアドレス を入力。 ユーザー名とパスフレーズはDSMと同じもの を入力してログイン。  
NASにアクセスできたら管理者権限でsuコマンドを実行。パスワードの入力を求められるので DSMにログインする時と同じもの を入力（ログは残らない）

$ sudo su -  
password

先ほど起ち上げたubuntuコンテナに入りたいのでコンテナIDを調べる。  

$ docker container ls  

CONTAINER IDってとこに記載されているIDをメモるかコピって下記コマンドでコンテナ内に入る。IDの部分をNAMESの「ubuntu（コンテナの名前）」に書き換えてもよい。

$ docker exec -it xxxxxxxxxxx bash  

[![[_resources/NZs │ Blog/bc2a873e9ef33f665bdb06f73fb8b0a4_MD5.jpg]]](https://clannzs.games/contents/img/news/2024/02/02/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202024-02-02%20143844.jpg)

2）Minecraft Serverの起ち上げ

コンテナに入ることができたがコマンドも何もインストールされていない真っ新なubuntuなので、必要に応じて都度コマンドをインストールしていく。 ~~まずは「sudo」から。~~ 最後までやってから気付いたんですが今回は必要なかったです。

$ apt update  
~~$ apt install sudo~~

今回起ち上げるのはNASのスペックと負荷を考慮して軽量の Paper1.20.4サーバー にすることにした。  
このバージョンには Java 21 が必要なのでインストールする。

$ apt install openjdk-21-jdk-headless  
y

とりあえず日本語にする（飛ばしてもヨシ）

$ apt-get install language-pack-ja  
y  
$ update-locale LANG=ja\_JP.UTF-8  
$ echo 'export LANG=ja\_JP.UTF-8' >> ~/.bashrc  
$ source ~/.bashrc

タイムゾーンを東京にする。先ほどマッピングした 「./data」 に移動してからPaperMCをダウンロード。 以降全ての作業は基本このディレクトリで行う。  
[PaperMCのダウンロードページ](https://papermc.io/downloads/paper) へ飛び、起動したいバージョン（今回は1.20.4）のダウンロードリンクをコピーする。  

[![[_resources/NZs │ Blog/95b064e451d42201decab0890a5809b7_MD5.jpg]]](https://clannzs.games/contents/img/news/2024/02/02/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202024-02-02%20230752.jpg)

$ cd data  
$ apt install curl  
y  
$ curl -OL https://api.papermc.io/v2/projects/paper/versions/1.20.4/builds/405/downloads/paper-1.20.4-405.jar

ダウンロードできたか一応確認してからjar実行。

$ ls  
$ java -jar paper-1.20.4-405.jar

[![[_resources/NZs │ Blog/0141cae2fc90a12d74bc3654464bd295_MD5.jpg]]](https://clannzs.games/contents/img/news/2024/02/02/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202024-02-02%20144758.jpg)

初回起動時は 「eula.txt」に同意しろ ってエラー文が出て処理が終了する。エディタをインストールして「eula.txt」の編集画面へ。

$ apt-get update  
$ apt-get install vim  
y  
$ vi eula.txt

\[i\]で挿入モードになるので「eura= true 」に書き換えて、\[Esc\]→\[:wq\]→\[Enter\]で保存して退出（ミスったら\[Esc\]→\[:q!\]→\[Enter\]で破棄して退出）  
改めてjarを実行すると今度こそサーバーが起動する。

[![[_resources/NZs │ Blog/626ad9d2a4f8ec6ad73a148de120de43_MD5.jpg]]](https://clannzs.games/contents/img/news/2024/02/02/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202024-02-02%20145036.jpg)

Minecraftサーバーをrootとして実行すんなカス みたいな警告文が出るけど今回は無視する。しないと進めない。  
ちなみに誘導されるページは [ここ。](https://madelinemiller.dev/blog/root-minecraft-server/)  
  
マイクラを起動してサーバーアドレスにNASのローカルIPアドレス XXX.XXX.XX.XX を入力して起ち上がっているか確認する。  

[![[_resources/NZs │ Blog/34cddc98d68c569c9d72e659268a61a3_MD5.jpg]]](https://clannzs.games/contents/img/news/2024/02/02/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202024-02-02%20145154.jpg) [![[_resources/NZs │ Blog/2375adfb94cf957cec19db41c77c8082_MD5.jpg]]](https://clannzs.games/contents/img/news/2024/02/02/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202024-02-02%20145313.jpg)

おｋ  
ターミナルに「stop」を入力して一旦サーバーを閉じる。  
  

###### 自動でバックアップされるようにする

手動でバックアップするのは骨が折れるので screenとcronを用いて自動化する。 ここが一番苦労した。

1）screenをインストールしてscreen内でサーバー起動

$ apt install screen  
y  
$ screen  
Enter  
$ screen java -jar paper-1.20.4-405.jar

screenを起動して、その中でもう一度jarを走らせてサーバーが起ち上がっているか改めて確認する。  
確認できたら「stop」でサーバーを閉じて、\[ctrl\]+\[a\]→\[k\]で一旦screenを終了。

2）起動スクリプトとバックアップスクリプトの作成

予めバックアップディレクトリを作成しておく。以降も 「./data（jarファイルがあるディレクトリ）」 で作業すること。

$ mkdir backup

zipが必要になるのでインストール。

$ apt update && apt install -y zip

起動スクリプトを作成する。  
エディタに入ってから\[gg\]→\[Shift\]+\[v\]→\[Shift\]+\[g\]→\[x\]→\[i\]→\[右クリ\]でクリップボードを全部貼り付けられる。

$ vi start.sh  
[これをコピペして保存  
](https://clannzs.games/contents/download/start.sh)$ sh start.sh

一見なにも起こらないが、既に裏側でscreenが起動していてその中でマイクラサーバーが動いている。下記で確認できる。

$ screen -ls  
$ screen -r  
\[ctrl\]+\[a\]→\[d\]

バックアップスクリプトを作成して動かしてみる。  
下記先駆者様のスクリプトを引用させていただいております。  
  
- Minecraftサーバをscreenとcronでプラグインを使わずに自動再起動する | なうびるどいんぐ  
	[https://jyn.jp/minecraft-server-auto-restart/](https://jyn.jp/minecraft-server-auto-restart/)
  
- 【Minecraftマルチサーバー】自動バックアップがようやく動くようになったメモQiita  
	[https://qiita.com/zawanume/items/17bcb08cbdf2aa90dc11](https://qiita.com/zawanume/items/17bcb08cbdf2aa90dc11)

$ vi restart.sh  
[これをコピペして保存  
](https://clannzs.games/contents/download/restart.sh)$ sh restart.sh

[![[_resources/NZs │ Blog/dcafceeab99734151106d92f39d8d300_MD5.jpg]]](https://clannzs.games/contents/img/news/2024/02/02/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202024-02-02%20150036.jpg) [![[_resources/NZs │ Blog/c1a8513078841fc153d862529ada8ab9_MD5.jpg]]](https://clannzs.games/contents/img/news/2024/02/02/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202024-02-02%20150122.jpg) [![[_resources/NZs │ Blog/65ce3088f0e992ca49813eacb1f1138c_MD5.png]]](https://clannzs.games/contents/img/news/2024/02/02/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202024-02-02%20221820.png)

おｋ

3）cronで自動化する

cronをインストールしてcrontabの編集（毎日午前5時にサーバーが再起動されてバックアップされるように記述してある）

$ apt update && apt install -y cron  
$ crontab -e  
59 4 \* \* \* /data/restart.sh

cronを起動して確認する （大事！）

$ service cron start  
$ service cron status  
$ crontab -l

これで NASのDockerで起ち上げたubuntuコンテナ内でマイクラサーバーが自動でバックアップされる ようになった。  
もうターミナル閉じていいですよ。  
  

###### おわりに

起動スクリプトとか細かいところ詰めてないし前述の警告文は気になるけど取り敢えずこれでヨシとする。  
後はルーターの25565ポート（変更してなければ）を開放すればお友達と遊べます。  
  
僕の周りはみんな Palworld に行っちゃったんで一人で遊ぶんですけどね。  
  

---

  
参考にさせていただいた偉大なる先駆者様方  
  
- Ubuntu 20.04でMinecraftサーバー構築  
	[https://zenn.dev/de\_teiu\_tkg/articles/1b9025d3a6db71](https://zenn.dev/de_teiu_tkg/articles/1b9025d3a6db71)
  
- マイクラサーバーがssh接続を切っても動くようにする\[screen\]  
	[https://gafuburo.net/screen-minecraft-server/](https://gafuburo.net/screen-minecraft-server/)
  
- Debian/Ubuntuのロケールを日本語にする方法 Qiita  
	[https://qiita.com/valzer0/items/db7639d8231bf5121297](https://qiita.com/valzer0/items/db7639d8231bf5121297)
  
- Minecraftサーバをscreenとcronでプラグインを使わずに自動再起動する | なうびるどいんぐ  
	[https://jyn.jp/minecraft-server-auto-restart/](https://jyn.jp/minecraft-server-auto-restart/)
  
- 【Minecraftマルチサーバー】自動バックアップがようやく動くようになったメモ Qiita  
	[https://qiita.com/zawanume/items/17bcb08cbdf2aa90dc11](https://qiita.com/zawanume/items/17bcb08cbdf2aa90dc11)