---
title: "【マイクラ統合版】Switchから外部サーバーへ接続する方法"
source: "https://www.radical-dreamer.com/game/minecraft_bedrockconnect/"
author:
  - "[[ケイのゲーム＆ガジェット部屋]]"
published: 2023-08-06
created: 2025-05-17
description: "Switch版Minecraft(マイクラ)は基本的には特集サーバー以外の外部サーバーへアクセスできません。 しかし、裏技的な方法(BedrockConnect)を使うことで、指定した外部サーバーへアクセスすることができます。 ここではその方法を画像を交えて詳細に解説します。"
tags:
  - "clippings"
---
1. [ホーム](https://www.radical-dreamer.com/)
2. 【マイクラ統合版】Switchから外部サーバーへ接続する方法

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/0524a94229e27d9fc81ef95b1fb79ff7_MD5.png]]

Switch版のMinecraft(マイクラ)は、Realmsや公式が公開しているサーバー（「The Hive」や「CubeCraft」など）にしか接続できません。

しかし、自宅サーバーやレンタルサーバーに構築した統合版サーバー(Bedrock版サーバー)に接続したいという場面もあると思います。

あわせて読みたい

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/b922b7c227ebf436651052ccbcf4d5af_MD5.png]]

[【マイクラ統合版】自宅サーバーの構築方法(サーバー設定とアップデート方法も含む)](https://www.radical-dreamer.com/game/minecraft_howto_bedrock_server_build/) Minecraft(マイクラ)統合版のサーバーといえば、公式サーバーの『Realms』、レンタルサーバーの『ConoHa VPS』や『Xserver VPS』等を使うことが一般的です。 しかし、こ...

ここではちょっとした **裏技的な方法(BedrockConnect)** を使って、外部サーバーへ接続する方法を紹介します。

Switch版マイクラは基本的に **公式サーバー以外へのアクセスをサポートしていません** 。  
ご利用は自己責任でお願いします。  
(といっても、アクセス経路を変えるだけなので問題ないはずですが)

目次
1. [概略説明](https://www.radical-dreamer.com/game/minecraft_bedrockconnect/#index_id0)
2. [外部サーバーへの接続手順](https://www.radical-dreamer.com/game/minecraft_bedrockconnect/#index_id1)
3. [BedrockConnectのその他情報](https://www.radical-dreamer.com/game/minecraft_bedrockconnect/#index_id2)
	1. [保存したサーバーの設定を変えたい](https://www.radical-dreamer.com/game/minecraft_bedrockconnect/#index_id3)
	2. [BedrockConnectに繋がりにくい](https://www.radical-dreamer.com/game/minecraft_bedrockconnect/#index_id4)
4. [まとめ](https://www.radical-dreamer.com/game/minecraft_bedrockconnect/#index_id5)

## 概略説明

接続するための手順を紹介します…が、DNSの設定やIPアドレスの設定とか出てくるので、

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/63a4828e0b641dc0e34af0d625e3086e_MD5.png]]

**これって本当に大丈夫なの？**

と感じる方もいると思います。

そのため、これからどんなことをするのかを簡単にイメージを載せておきます。少しでも安心できるかと。

設定を変える前は以下のような状態でマイクラは公式サーバーへアクセスしています。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/7f638f3db9eb720ac163bed569411045_MD5.png]]

今回の変更を行うと以下のようになります。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/ca732634d660c394089674a71c90c382_MD5.png]]

上記のように特殊なDNSサーバーでBedrockConnectサーバー（踏み台サーバー）へ誘導し、そこから自分で指定したIPアドレスへ転送させることにより、公式サーバー以外のサーバーへの接続を実現しています。

では、上記の状態にするための手順を解説します。

## 外部サーバーへの接続手順

接続方法の概略を理解したところで、実際にそうなるようにする設定を解説します。

ここでは自宅に構築したマイクラサーバー（192.168.1.10）へのアクセス方法を例にして手順を解説します。

STEP

Switchのネットワーク設定(DNS)

Switchの優先DNSと代替DNS設定を以下のように変更します。

| 優先DNS | 104.238.130.180（Bedrockサーバーを提供しているDNS） |
| --- | --- |
| 代替DNS | 008.008.008.008（Google Public DNS） |

まずは設定を開いて、

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/9f271be76035cc7146b98c377f7be402_MD5.jpg]]

インターネット設定を開きます。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/29697d5a871e925951cef9413c0b8eba_MD5.jpg]]

インターネット設定を開いたら、接続しているネットワークを選択して、

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/37f78a19fc8ebf91ba2ae4f55ea01d1f_MD5.jpg]]

「設定の変更」を選択します。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/f23b4d379c176d28107aa94371640e81_MD5.jpg]]

設定画面が開くとDNS設定の項目があります。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/1de2606298d7b5e07df882e7a0b1de88_MD5.jpg]]

デフォルトは「自動」となっているので、ここを「手動」に変更します。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/8036ef110be973e36fefde9c8137bd6a_MD5.jpg]]

すると、「優先DNS」と「代替DNS」の設定項目が現れるので、それぞれ冒頭に記載したIPアドレスを設定します。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/a15c4effa595fa0046b220bf5e544325_MD5.jpg]]

設定が完了したら「保存する」を選択して、設定を保存しましょう。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/d94984946db4e60f9e8f2dae79404e08_MD5.jpg]]

以上でDNSの設定は完了です。

STEP

BedrockConnect（踏み台サーバー）へのアクセス

DNSの設定が完了したら、マイクラを起動します。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/c051ab029cd6c6a3b7315a6da7833c33_MD5.jpg]]

マイクラが起動したら、公式の特集サーバーへアクセスします。

どの特集サーバーでも良いのですが、ここの例では「The Hive」へアクセスすることにします。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/db9f7aaa94bb0774d47f1371b25b0d24_MD5.jpg]]

するとBedrockConnectサーバーにアクセスして、以下のような画面が出てきます。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/2ee442bdc5736f007a72a9c7093f3d45_MD5.jpg]]

以上でBedrockConnectへアクセスできました。

STEP

外部サーバーへのアクセス

最後にBedrockConnectから外部サーバーへ転送してもらう手順となります。

BedrockConnectの画面が開いたら、「Connect to a Server」を選択します。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/ebbe9ab116af208930d912bdabe917d4_MD5.jpg]]

すると以下のような画面が出てきます。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/830f1e8ed4190f820ba0c9cd2bbbd512_MD5.jpg]]

各項目の説明は以下の通り。

| Server Address | 接続するサーバーのIPアドレスを入力します |
| --- | --- |
| Server Port | 接続するサーバーのポート番号を入力します   マイクラサーバーのデフォルトは「19132」です |
| Display Name on Server List   (オプション設定) | 接続サーバーの情報を保存する際の名前を入力します   必須ではありません |
| Add to server list | オンにすると今回接続するサーバー情報を保存することができます   次回以降の接続が楽になるので、基本的にはオン推奨 |

今回の接続例に合わせて設定すると、以下のようになります。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/af828d23f721e8095e413ffabd3d9d0c_MD5.jpg]]

最後に送信を押すと、設定したサーバーへの接続が始まります。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/1be6c0486df0686dbf5f74061f18d67d_MD5.jpg]]

無事接続できました。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/8576ec22cc9ff418003ccd5197091e52_MD5.jpg]]

なお、「Add to server list」をオンにしていると、以下のようにServerListに保存したサーバー（MyServer）が表示されます。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/808ef9e2eb40ed4fe8fce7ca3b67f10d_MD5.jpg]]

次回以降はこちらを選択するとサーバーへの接続が開始されます。IPアドレスやポート番号の入力を省略できるので楽ですね。

## BedrockConnectのその他情報

ここからはBedrockConnectを使う上で知っておくと便利な情報を紹介します。

### 保存したサーバーの設定を変えたい

BedrockConnectに保存したサーバー情報を変更したい場合は、「Manage Server List」の「Edit a Server」を使います。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/31bffe07ef2dad8c4cb70194f76008a9_MD5.jpg]]

「Manage Server List」を開くと以下の画面が表示されます。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/0ab5c49eb25d64f8ed98face804c88f0_MD5.jpg]]

「Edit a Server」を選択すると、以下の画面が表示されます。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/4751fc38a797008939c99af535157181_MD5.jpg]]

プルダウンリストがあるので、ここで設定変更したサーバーを選択して「送信」を押します。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/95e3e349948d81114237d0225abc3fd4_MD5.jpg]]

選んだサーバーの設定情報が表示されるので、変えたい設定を変更して「送信」を押しましょう。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/e71975cdc1aaa117e214db8189fdbac2_MD5.jpg]]

以上で保存しているサーバー情報の変更ができました。

### BedrockConnectに繋がりにくい

BedrockConnectは有志によって公開されているサーバーであり、しかも海外にサーバーがあるため接続が不安定になりやすい傾向にあります。

そんなときは接続するBedrockConnectサーバーを変えてみると良いです。

2023年4月時点で公開されているBedrockConnectサーバーは以下となります。

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/8d533de482dbf8413b16d1e9be55d023_MD5.gif]]

インターネット設定の優先DNSを上記のいずれかを選択して設定してください。

なお、公開されている最新のサーバー情報はBedcorkConnectのGitHubページを参照してください。

GitHub

![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/08fce67b689e33e02e8702ea223c1f08_MD5.png]]

[GitHub - Pugmatt/BedrockConnect: Join any Minecraft Bedrock Edition server IP on Xbox One, Nintendo...](https://github.com/Pugmatt/BedrockConnect)Join any Minecraft Bedrock Edition server IP on Xbox One, Nintendo Switch, and PS4/PS5 - Pugmatt/BedrockConnect

## まとめ

Switchから公式以外の外部サーバーへ接続する方法を解説しましたが、仕組みを理解してしまえば簡単なことだと思います。

なお、このBedrockConnectは自分でサーバーを立てることもできます。

- **海外接続は不安**
- **BedrockConnect接続が不安定で繋がらない**
- **サーバーリストがサーバー上に残るのが怖い**

と感じる方は、ローカルネットワーク内にBedrockConnectサーバー（併せてDNSサーバー）を立てると良いでしょう。

ちなみに私は接続が不安定だったので、持っていたRaspberry Pi上にBedrockConnectサーバーを構築しました。

BerockConnectサーバーの構築手順については、現在まとめ中なのでしばしお待ちください。

- [【Windows】LANのIPアドレスを固定する方法](https://www.radical-dreamer.com/pc/static_ipaddress_windows/)

## 関連記事

- [
	![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/b922b7c227ebf436651052ccbcf4d5af_MD5.png]]
	【マイクラ統合版】自宅サーバーの構築方法(サーバー設定とアップデート方法も含む)
	](https://www.radical-dreamer.com/game/minecraft_howto_bedrock_server_build/)
- [
	![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/36819c9e4b90bfa95261a6c9b7822ebe_MD5.png]]
	【マイクラ】マルチプレイを快適にする方法【Switch版】
	](https://www.radical-dreamer.com/game/minecraft_multiplay/)
- [
	![[_resources/【マイクラ統合版】Switchから外部サーバーへ接続する方法/af1a493b6ee5bcbade983328045aa7d6_MD5.png]]
	【マイクラ】Nintendo Switchでマルチプレイする方法と手順
	](https://www.radical-dreamer.com/game/minecraft_on_switch/)
