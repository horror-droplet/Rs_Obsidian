---
title: "Synology NasでGmailをバックアップする"
source: "https://ysand.myds.me/2025/01/04/synology-gmail-backup/"
author:
  - "[[のんびりどこまでも]]"
published: 2025-01-04
created: 2025-05-17
description: "SynologyでGmailなどのメールを保存（バックアップ）したいと思い調べたところ、思ったより簡単だったの…"
tags:
  - "clippings"
---
![[_resources/Synology NasでGmailをバックアップする/4aa1981b7c9efbf6047db6b6da9be346_MD5.jpg]]

[Synology](https://amzn.to/4i1iZFT) でGmailなどのメールを保存（バックアップ）したいと思い調べたところ、思ったより簡単だったので、書き残しておきます。

自分の場合はGmailのみ利用したいので、ここではGmailでのやり方しか記載されていませんので、ご注意ください。

## １．Synology Mail Serverをインストールする。

![[_resources/Synology NasでGmailをバックアップする/cf8beb10bbd4e2f57ca6c2b889a9e0e7_MD5.jpg]]

インストールが終わり、下図のような画面が出ますが、特に何もせず閉じます。

![[_resources/Synology NasでGmailをバックアップする/65314a16827e45099b2447d98fbc9f5f_MD5.jpg]]

## ２．コントロールパネルを開きます。

![[_resources/Synology NasでGmailをバックアップする/0cc5f5824abea23a5b323c4c8ce49e70_MD5.jpg]]

ユーザーとグループを開きます。

![[_resources/Synology NasでGmailをバックアップする/3786edffd7f0d4c248f11bdde3b3cec9_MD5.jpg]]

詳細タブを開いて、ユーザーホームサービスを有効にするにします。

![[_resources/Synology NasでGmailをバックアップする/8dda7074fab233e6ed248eb233401fd9_MD5.jpg]]

## ３．Mail Stationをインストールします。

![[_resources/Synology NasでGmailをバックアップする/c72c17e53896d74f55d07eefe4a9afd4_MD5.jpg]]

インストールが終わったら、開きますが、その前にGmailとGoogleの設定を確認、設定してください。

## ４．Gmailを開きPOP3を有効にする

Gmailを開いて、設定画面を開きます。

![[_resources/Synology NasでGmailをバックアップする/57c33960fd568dd4d6be97e6c8681fd8_MD5.jpg]]

メール転送とPOP/IMAPタブを開きます。

![[_resources/Synology NasでGmailをバックアップする/6cd1fcf9e10b7986805b1ac02d83aa7f_MD5.jpg]]

POPダウンロードの項目で、POPが有効になっていればOKです。

なっていなければ、自分の好みの設定を選択して閉じます。

## ５．Gooogleのアプリパスワードを開き設定します。

Gooogleの機能でアプリパスワードという機能を設定します。

機能の説明や設定などの詳細は、以下のグーグルのリンクから行ってください。

分からない場合、以下の画面の所から設定します。

![[_resources/Synology NasでGmailをバックアップする/0b816a82e0f62328613f1ff7b2cb74ee_MD5.jpg]]

間違えたら何度でも作り直せば良いと思いますので、気軽にやればよいと思います。

## ６．Mail Stationを開きます。

Mail Stationを開くと下図のような画面が開きます。

Synologyのユーザー名とパスワードでログインします。

![[_resources/Synology NasでGmailをバックアップする/5df2041fd2577bf7106cefc028499256_MD5.jpg]]

①　初めにPOP3メールサーバーの設定をします。

下図の①～④を順番に押していくだけです。

![[_resources/Synology NasでGmailをバックアップする/53727d7d24284caff9939f83c3129ec2_MD5.jpg]]

で、下図だと設定タブを選択してる所が抜けてますので、注意してもらって、左の①のPOP3から入って、③メールアドレス、④Gmailを選択、⑤は③と同じメールアドレス、⑥は先に作成したアプリパスワードを入力します。

![[_resources/Synology NasでGmailをバックアップする/3b98f3b93716512163e83ab18384ca4c_MD5.jpg]]

複数のメールアドレスがあったりするならば、分かりやすくフォルダ名を付けたほうが良いと思います。

![[_resources/Synology NasでGmailをバックアップする/3ade8f5244ac2882320f901c06022280_MD5.jpg]]

下図はそのままでOK

![[_resources/Synology NasでGmailをバックアップする/a2b2f26fc0aeaa68abc8c100cbfbca02_MD5.jpg]]

下図の設定は好みで良いですが、バックアップという意味では下図で。

![[_resources/Synology NasでGmailをバックアップする/5a05653b612619ad450f725c2bd20c49_MD5.jpg]]

設定が終わるとメールがバックアップされます。

![[_resources/Synology NasでGmailをバックアップする/ef8fe767fa4203e0916b3e4a91abe492_MD5.jpg]]

これで設定が終わりました。案外、簡単です。

Synologyのアプリに関して、何も設定しないので簡単で良いと思いますよね。

自分の場合、Gmailを五つ持ってまして、ある程度使い分けしているのですが、それでも上図の通りで、あるアカウントに片寄ってます。

参考にしたサイト↓助かりました。[SynoPower Club - Synologyライセンス 24時間365日オンライン配信](https://synopower.club/ja/docs/%F0%9F%A4%94-how-can-i-save-my-business-emails-%F0%9F%93%A5-to-a-synology-nas-for-easy-organization-%F0%9F%93%82-and-retrieval/?srsltid=AfmBOorN34krSNF_nEzs-whdEj3bX1vjP4_M6ehH25_wM4g_YRLqFV4A)

[

![[_resources/Synology NasでGmailをバックアップする/f15e36a504c1fccaf2688ed71c708042_MD5.jpg]]

異なるアカウント（Gmail、Yahoo!...）のメールをSynology NASに保存してバック...

https://synopower.club/ja/docs/-how-can-i-save-my-business-emails--to-a-synology-nas-for-easy-organization--and-retrieval/?srsltid=AfmBOorN34krSNF\_nEzs-whdEj3bX1vjP4\_M6ehH25\_wM4g\_YRLqFV4A
