---
title: "ObsidianをSelf-hosted LiveSyncで同期させる簡単な方法"
source: "https://penchi.jp/archives/15829.html"
author:
  - "[[penchi.jp]]"
published:
created: 2025-07-06
description: "Obsidianの同期はあれこれ試しました。ほぼリアルタイムに同期できて快適！ と言われている Self-hosted LiveSyncというプラグインを使った同期はかなりハードルが高く挫折を繰り返しましたが、このたびやっと成功！そこで、その手順をまとめてみます。Self-hosted LiveSyncを使ったObsidianのデータ同期Self-hosted LiveSyncはObsidianのプラグインで、CouchDB（カウチD"
tags:
  - "clippings"
---
![[6033066a1c9bbbd9e964cbe105ac7863_MD5.jpg]]

Obsidianの同期はあれこれ試しました。  
ほぼリアルタイムに同期できて快適！ と言われている Self-hosted LiveSyncというプラグインを使った同期はかなりハードルが高く挫折を繰り返しましたが、このたびやっと成功！  
そこで、その手順をまとめてみます。

## Self-hosted LiveSyncを使ったObsidianのデータ同期

Self-hosted LiveSyncはObsidianのプラグインで、CouchDB（カウチDB）を使って同期するシステムです。  
そのためにCouchDBを用意する必要があり、これがハードルを高くしている要因です。  
今回はこの作業を簡単にできる自動セットアップスクリプトを使って行うことで、成功に至りました。

CouchDBはFly.ioというサービスを利用するので、Fly.ioのアカウントが必要になります。  
Fly.ioのアカウント作成は下記の記事にまとめてあるので、参照ください。

![[dc36771fff03b08b0b86ad234460b09e_MD5.jpg]]

## Fly.ioでCouchDBを作成する

Self-hosted LiveSyncの作者の [きみのぶ](https://x.com/vorotamoroz) さんが自動セットアップスクリプトを用意してくれているのでそれを利用させていただきます。

[setup-flyio-on-the-fly-v2.ipynb](https://github.com/vrtmrz/obsidian-livesync/blob/main/setup-flyio-on-the-fly-v2.ipynb) を開き、 **Open in Cokab** をクリックします。

![[5daf3720c051a04cd031032b4c5c5b03_MD5.png]]

一番上の **Install prerequesties** の表記の前の **\[ \]** をクリックします。

![[05b90fe3bd1b8f6531d6d5019a9f0c73_MD5.png]]

警告ウインドウが表示されるので、 **このまま実行** をクリックします。

![[626a6f87e5467f8524aaebff818d3ca1_MD5.png]]

作業が開始されるのでしばし待ちます。

![[78898f383a5463039cbe36868f0455d7_MD5.png]]

作業が終わったら、Fly.ioにサインアップする手順になりますが、ここではあ **らかじめFly.ioのアカウントを作成しサインインしておくと作業がスムーズ** です。  
下記の記事を参考に、Fly.ioのアカウントを作成しログインしておきましょう。

![[dc36771fff03b08b0b86ad234460b09e_MD5.jpg]]

![[aaa71a7a9f05ac5fe17cafdf9f3a22d6_MD5.png]]

URLが表示されるので、クリックして開きます。

![[767cad421a156a6be3ed8c0fdfb44174_MD5.png]]

Fly.ioにサインインします。  
下記の表示が出たら、中央にあるメールアドレスが表示されているボタンをクリックします。

![[b15ba95790ec3f7969ff16f72dee200c_MD5.png]]

表示が変わります。

![[e0aa745e236f9d3e697f5d6c1424616b_MD5.png]]

上記の表示が出てから、作業しているウインドウに戻ると、 **successFully logged in as ＜メールアドレス＞** の表示があります。

![[dd30cc45ed01a7936745ab180e81f5be_MD5.png]]

ここからCouchDBを作成する作業になります。  
**regionがTokyoになっていることを確認** したら、左にある **\[ \]** をクリックし、作業を実施します。

![[ba29c9ed8f005776e6e3973e11d820d5_MD5.png]]

しばらく待つと作業が完了します。

表示されたデータの上部に下記の表示があるのでメモします。

> \-- YOUR CONFIGRATION --  
> URL: https://\*\*\*\*\*\*\*.fly.dev  
> username: \*\*\*\*\*\*\*\*  
> password: \*\*\*\*\*\*\*\*  
> region: nrt

![[624af1f469ac751dc2f918f97ca2f7d0_MD5.png]]

次に表示の下部にある下記の表示をメモします。

> \--- configured ---  
> database: obsidiannotes  
> E2EE passphrase: \*\*\*\*\*\*\*\*\*\*\*

![[961cd7b7854c4f0c46b0d97fceee64b1_MD5.png]]

さらにその下にある **obsidian:// から始まる文字列（URI）** をメモします。

一番下の項目は、CouchDBを削除する作業になるので、実行しないよう気をつけてください。

![[6d93850adbc6c9765da82fb2f7477e01_MD5.png]]

### メモする項目まとめ

**作業画面に表示されるものは別途保存されるわけではないので、自分で記録しておく必要があります。  
下記の項目は必ず記録して保存してください。**

| URL | https://\*\*\*\*\*\*\*\*\*\*.fly.dev | Fly.ioの自分のURL |
| --- | --- | --- |
| username | \*\*\*\*\*\*\*\*\*\*\*\*\* | CouchDBのユーザー名 |
| password | \*\*\*\*\*\*\*\*\*\*\*\*\* | CouchDBのパスワード |
| database | obsidiannotes | データベース名（決まっているっぽい？） |
| E2EE passphrase | \*\*\*\*\*\*\*\*\*\*\*\*\*\* | URIを使う際のパスフレーズ（パスワード） |
| URI | obsidian://\*\*\*\*\*\*\*\*\*\*\* | 設定を一発でできる値（とても長い文字列） |

URIはCouchDBの設定を一括で設定するためのもので、とても長い文字列です。  
このURIはSelf-hosted LiveSyncで再発行（別な文字列になる）可能なので、わからなくなっても大丈夫です。  
**E2EEE passphraseはURIを使う際に必要** なので、なくさないようにしましょう。

ここで表示されるものはウインドウを閉じると二度と表示されないので、安全のために表示されたデータをまるごとコピーして保存しておくといいです。  
ワタシはNotionに保存用のページを作成し、まるごとコピーしたデータをプレーンテキストのコードブロックに貼り付けて保存しています。

![[60ff64c9c88a0ddb9af201c27d25ea61_MD5.png]]

![[1a223626e8def446dec2b3fbbebea190_MD5.png]]

## ObsidianでSelf-hosted LiveSyncを設定する

作成したCouchDBのデータを記録したら、ObsidianでSelf-hosted LiveSyncの設定をします。

Obsidianの設定からコミュニティプラグインを開き、Self-hosted LiveSyncをインストールします。

![[d547686f11a7e8f993696d368298dbca_MD5.png]]

プラグインを有効化するとウインドウが開きますが、 **Dismiss** ボタンをクリックして閉じます。

※このウインドウにある **Use the copied setup** URI ボタンをクリックすると、先程メモしたURIとパスフレーズで設定できますが、ここではあえて手動でセットアップしていきます。

![[029e4b0f5dd7c13f0ea7bb9181a982da_MD5.png]]

Self-hosted LiveSyncの設定画面で下記の矢印のどちらかをクリックし設定画面を表示します。

![[69bc428d36f40565a7a3d219acb8a369_MD5.png]]

設定画面にあるURIはobsidhian:// で始まる文字れるではなく、 **Fly.ioのURL** です。  
表記がURIになっているので混乱しますが、間違えないようにしましょう。

![[adc406cab5f3122f9e148b8660aae125_MD5.png]]

設定に使うデータは下記のものになります。

| URI | Fly.ioのURL | https://\*\*\*\*\*\*\*\*\*\*.fly.dev | Fly.ioの自分のURL |
| --- | --- | --- | --- |
| Username | username | \*\*\*\*\*\*\*\*\*\*\*\*\* | CouchDBのユーザー名 |
| Password | password | \*\*\*\*\*\*\*\*\*\*\*\*\* | CouchDBのパスワード |
| Database name | database | obsidiannotes | データベース名（決まっているっぽい？） |

入力を終えたら下部にある **Check** ボタンをクリックします。

![[2587ac5eca8233263c3c1af19d04be9e_MD5.png]]

チェックが済むと下部に **Next** ボタンがあるのでクリックして進みます。

![[bd1df4a5d4e07dbb5ccec02763d397ee_MD5.png]]

Sync Setting の設定になるので、 **Presets** の選択肢で **LiveSync** を選び、 **Apply** ボタンをクリックします。

![[3e9966299b97c9c6b1341932ce739f9a_MD5.png]]

これで設定が完了です。

![[ab2ebbdd02853b4b4126cdc3be27d30d_MD5.png]]

Obsidianのノートの右上に同期状態が表示されています。

![[d88fd04808e66a1fb9f1509278938586_MD5.png]]

## Self-hosted LiveSyncの2台目以降の設定

2台目以降の設定ではセットアップ用のURIとパスフレーズを使う方法が簡単でおすすめです。

2台目以降のデバイスのObsidianを開き、Self-hosted LiveSyncプラグインをインストールしセットアップ画面を開きます。  
**Use the copied setup URI** の項目で **Use** ボタンをクリックします。

![[e3a68e5e6d2060b66750ba01531e37c3_MD5.png]]

Easy setup ウインドウが開き、Set up URI を入力する箇所があるので、ここに先に保存してある **obsidian:// から始まる長い文字列** をコピーして貼り付けます。

![[abef522cb1569f6e978f337f80a0b296_MD5.png]]

次にパスフレーズを入力するウインドウになるので、 **E2EEE passphrase** を入力します。

![[4d49a4d2e2d1b115563ac3be1a2efb06_MD5.png]]

設定をインポートするかを聞いてくるので **yes** をクリックします。

![[5c6db955af058817839b2931fce608d2_MD5.png]]

次のウインドウでは一番上の **Set it up as secondary or subsequent device** をクリックします。

![[b7c7b62512a2d52fd192ad90b67f1d3a_MD5.png]]

Hidden file sync のウインドウが表示されるので、 **Fetch** ボタンをクリックします。

![[dd5b005e0f0541b5a520f6bb5aff864a_MD5.png]]

設定をすると、CouchDBの設定値がきちんと入っていることが確認できます。

![[a85aa2b56402afa533b794b386942fb8_MD5.png]]

これが2台目以降のデバイスの設定方法です。  
セットアップ用のURIを使わず、1台目のように手動で設定してもOKですが、やはりセットアップURIを使う方が楽ですね。

ワタシは今回のセットアップ用の全データをNotionに保存しており、2台目以降のデバイス（iPhoneなども含む）では、セットアップURIとパスフレーズを使い、サクッと設定しています。

## Self-hosted LiveSyncの同期時の特徴

テーマやプラグインなどの設定を変えると、同期している他のデバイスで下記のような表示が出ます。  
この表示が出たら HERE をクリックするとObsidianを再読込して設定を反映してくれます。

![[16568a77bbc2aabb03a90968dd944bd0_MD5.png]]

設定して数日、Windows・Mac・Linux・iOSで同期テストをしていますが、ノートのデータはもちろん、Obsidianのテーマやプラグインの設定も同期できています。  
同期のタイミングもほぼリアルタイムに同期されるので快適です。

Self-hosted LiveSync設定後に下記のウインドウが表示されますが、とりあえず **Do not warm** でいいようです。

![[36e20b601113a2e92f79cd378e5fe430_MD5.png]]

## まとめ

Self-hosted LiveSyncの設定はいろいろな方法を試し、挫折を繰り返しました。  
iCloudドライブでの同期も安定してきたので、それでいいかと思いながらも諦めきれず・・・。  
先日、再チャレンジして表示された内容を冷静に見ながら設定してみたら、無事に成功！  
その後、各デバイスを同期しあれこれテストを繰り返し、安定して使えるということで正式導入となりました。

Self-hosted LiveSyncについては様々な情報が点在しているのですが、仕様が変わっていて表示が違うものや、わかっている人向けのさらっとした情報が多く、自分なりに理解するのに試行錯誤しながら時間がかかりました。

そこで、今回自分が行って成功した手順をまとめて記事にしてみました。  
たぶん、Obsidianを同期して使いたいと思うような方なら、理解していただける内容ではないかと思います。

少しでも誰かの役に立てばうれしいです。

また、このような素晴らしいプラグインを作成し公開していただいているきみのぶさんに感謝いたします。
