---
title: Synology NASでminecraft Bedrock Serverを立てます。
source: https://kyoto-hirota.com/synology-nas%E3%81%A7minecraft-bedrock-server%E3%82%92%E7%AB%8B%E3%81%A6%E3%81%BE%E3%81%99%E3%80%82/
author:
  - "[[ひろたの備忘録]]"
published: 2022-08-18
created: 2025-05-17
description: Synology NASのDockerを使ってマインクラフト　ベッドロックサーバーの立て方設定です。
tags:
  - clippings
---
2022-08-18

![[_resources/Synology NASでminecraft Bedrock Serverを立てます。/b41c11399a1f454524864a6d7a8b8382_MD5.jpg]]

Synology NASのDockerをインストールして、Minecraft Bedrock Editionサーバーを立ち上げます。

マイクラのBedrock Editionとはスマホ、タブレット、Swich、Xbox One、Windows10で稼働できるBE版サーバーの説明をします。

このサーバーを立てるとローカルにあるSynology nasのマインクラフトのサーバーに端末からマルチプレイでアクセスできます。

※DSM7.1での設定方法の説明になります。

前提条件  
・パッケージセンターよりクジラのアイコンの「Docker」がインストールされてること。  
・synology DSMに管理者でアクセスできる事。

## 1\. Dockerのディレクトリ（フォルダ）にMinecraftのdataを保存できる場所を作成します。

・DSMの **「File Station」** を起動します。 **「docker」** のディレクトリ（フォルダ）を開いてください。

・上部 **「作成」** をクリックして **「フォルダの作成」** を選択します。

・フォルダ名を入力する画面が出てくるので マイクラのデータだと解るフォルダ名 を付けてください。  
　一例：Minecraft\_Bedrock\_data　など

![[_resources/Synology NASでminecraft Bedrock Serverを立てます。/0db8fff34a2eb636b48035278b0a7dc2_MD5.png]]

・「Minecraft\_Bedrock\_data」フォルダの中に **「data」のフォルダを作成** します。

![[_resources/Synology NASでminecraft Bedrock Serverを立てます。/32c1ea4075a523183ea0af0d30695721_MD5.png]]

## 2\. Dockerを起動させてMinecraft Bedrock Editionイメージをダウンロードします。

１のディレクトリ（作成）までの準備ができたら、いよいよ「docker」のアプリを立ち上げます。

・左のメニューの **「レジストリ」** をクリックします。

・右上の検索キーワードを挿入より **「minecraft」** と入力してEnterを押します。

・ **「itzg/minecraft-bedrock-server」** を選択して上位の **「ダウンロード」もしくはダブルクリックします。**

![[_resources/Synology NASでminecraft Bedrock Serverを立てます。/f36ef905645ebf832a87cd68f4e058c8_MD5.png]]

Minecraftデーモンダウンロード

・「タグを選択してください：」の窓が出てきたら「latest」で **「選択」をクリック** してください。

![[_resources/Synology NASでminecraft Bedrock Serverを立てます。/b03ff43b85a607fbfbb6383cc76b7c2a_MD5.png]]

これでマインクラフトのBedrockサーバーのダウンロードができました。

## 3\. Minecraft Bedrock Editionの設定を行い起動します。

・これからサーバーの設定を行います。

・左メニューのイメージよりダウンロードした「itzg/minecraft-bedrock-server」を選択して上記の **「起動」** をクリックします。

![[_resources/Synology NASでminecraft Bedrock Serverを立てます。/119f60fe1c943953b88a328079b3a20a_MD5.png]]

・最初は「ネットワーク」画面になります。  
　「選択されたネットワークを使用」の **「Bridge」** のにチェックが入ってれば **「次へ」をクリック** します。

・「全般設定」画面よりコンテナ名にダウンロードした「itzg/minecraft-bedrock-server」が入った画面になります。

　画面左下の **「詳細設定」** をクリックします。

・タブの「環境」より **「追加」をクリック** します。

　空白の変数に 「EULA」、その横の値の空白に「TRUE」を入力して「保存」をクリック します。

![[_resources/Synology NASでminecraft Bedrock Serverを立てます。/545ec4443dea1b9dd56b30a2a68c9780_MD5.png]]

・「全般設定」に戻ったら **「自動再起動を有効にする」にチェックを付けて「次へ」をクリック** します。

・「ポート設定」では、デフォルトでは、

ローカルポート　空白（薄字の自動と表示）  
コンテナポート　19132  
タイプ　UDP

になってますが、

下記の設定にします。

**ローカルポート　空白に「19132」を入力  
コンテナポート　そのまま（19132）  
タイプ　そのまま（UDP）**

にします。

画面の様に出来たら **「次へ」** をクリック。

![[_resources/Synology NASでminecraft Bedrock Serverを立てます。/7da834e346e13e445c6227b9cd2cd7c6_MD5.png]]

・「ボリューム設定」の画面では最初の **「FileStation」で作成したディレクトリ（フォルダ）にアクセスできる場所を指定** します。

　作成したのはファイルではなくフォルダなので **「フォルダの追加」** をクリックします。

追加の画面で「docker」を開いて **「Minecraft\_Bedrock\_data」で「選択」をクリック** します。

「ボリューム設定」の画面に戻ったら

　ファイル／フォルダにパスが記述されています。マウントパスに **「/data」を入力** して **「次へ」** を押します。

※「Minecraft\_Bedrock\_data」の中に作ったディレクトリ（フォルダ）を指定します。

![[_resources/Synology NASでminecraft Bedrock Serverを立てます。/75da1fe2d215970a6be3fc9ac4065c88_MD5.png]]

![[_resources/Synology NASでminecraft Bedrock Serverを立てます。/eedf3ac0c173af935a5015a9eb3947a8_MD5.png]]

・「要約」の画面になり、上記で設定してきた内容が表示されています。

![[_resources/Synology NASでminecraft Bedrock Serverを立てます。/7fbffd5d9a6b051c205065774ae6bb28_MD5.png]]

問題がなければ「ウィザード終了後、このコンテナを実行」にチェックが入ってるので、 **そのまま「完了」を押すとマイクラベッドロックサーバーが立ち上がります。**

お疲れ様でした。

※上記内容より、何らかの影響で不具合が生じても全て自己責任でお願いします。

