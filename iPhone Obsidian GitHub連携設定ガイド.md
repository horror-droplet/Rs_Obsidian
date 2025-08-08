---
tags: [技術/Obsidian, 技術/Git, 技術/モバイル, 技術/自動化, ガイド]
created: 2025-06-27
updated: 2025-06-27
---

# iPhone Obsidian GitHub連携設定ガイド

## 📱 概要

iPhone版ObsidianとGitHub連携の設定手順書です。デスクトップ版とは異なり、iOS特有の制限があるため、外部アプリとの組み合わせが必要です。

## 🚨 重要な制限事項

### iPhone版Obsidianの制限
- **Obsidian Gitプラグインが利用不可**（iOS版では制限されている）
- **自動同期機能が限定的**
- **ファイルシステムへの直接アクセスが制限**
- **手動操作が中心**となる

### 推奨事項
- **`.obsidian`フォルダは分離推奨**（PCとモバイル間で競合回避）
- **定期的な手動同期**が必要
- **Working Copy」アプリの利用が必須**

## 🛠️ 方法1: Working Copy アプリを使用した連携（推奨）

### 前提条件
- iPhone版Obsidianがインストール済み
- GitHubリポジトリが既に作成済み（デスクトップで設定済み）
- App StoreでWorking Copyアプリをダウンロード

### ステップ1: Working Copyの初期設定

1. **Working Copyを起動**
2. **GitHubアカウントと接続**
   - 設定 → Accounts → GitHub
   - GitHubにログインして認証
3. **既存リポジトリをクローン**
   - 「+」→「Clone repository」
   - 自分のObsidian Vaultリポジトリを選択
   - ローカルに保存

### ステップ2: Obsidianとの連携設定

1. **Obsidianを起動**
2. **新しいVaultを作成**
   - 「Create new vault」選択
   - 「Store in iCloud」を**オフ**
3. **Working Copyからファイルをインポート**
   - Working Copy → リポジトリを選択
   - 右上の共有ボタン → 「Copy to Obsidian」
   - または「Files」アプリ経由でコピー

### ステップ3: 同期ワークフロー

#### 📥 Pull（最新を取得）
1. **Working Copyを開く**
2. **リポジトリを選択**
3. **Pull**をタップ
4. **変更があった場合**：
   - 「Files」アプリでファイルをコピー
   - ObsidianのVaultに上書き

#### 📤 Push（変更をアップロード）
1. **ObsidianでMarkdownファイルを編集**
2. **「Files」アプリを開く**
3. **編集したファイルをWorking Copyフォルダにコピー**
4. **Working Copyで変更を確認**
   - Status → 変更されたファイルを確認
5. **コミット＆プッシュ**
   - 変更ファイルを選択 → Commit
   - コミットメッセージを入力
   - Push to origin

## 🛠️ 方法2: Obsidian Sync + GitHub併用（推奨）

### 設定手順
1. **Obsidian Syncサブスクリプション契約**
   - 月額$4-5（学生は40%割引）
   - 公式サイトでアカウント登録
2. **iPhone/iPadでObsidian Sync有効化**
   - 設定 → Sync → アカウントログイン
   - リアルタイム自動同期
3. **Mac/PCでGitHub同期併用**
   - デスクトップのObsidian Gitプラグインでバックアップ
   - 定期的にGitHubにコミット・プッシュ

### メリット・デメリット
- ✅ **メリット**: 最高の利便性、リアルタイム同期、エンドツーエンド暗号化
- ✅ **メリット**: iPhoneで手動操作不要、Working Copy不要
- ✅ **メリット**: GitHubバックアップで長期保存・バージョン管理
- ❌ **デメリット**: 月額費用発生、デュアル管理の複雑性

## 🛠️ 方法3: iCloud + GitHub併用（簡易版）

### 設定手順
1. **ObsidianをiCloudに保存**
   - Vault作成時に「Store in iCloud」を有効化
2. **Mac/PCで定期的にGitHub同期**
   - iCloudでファイルが同期される
   - Mac/PCのObsidianで自動GitHub同期を実行

### メリット・デメリット
- ✅ **メリット**: 設定が簡単、費用無料
- ❌ **デメリット**: Mac/PCが必要、iCloud同期待機時間、リアルタイム同期不可

## 🎯 運用のコツ

### 推奨ワークフロー
1. **朝一番**：Working CopyでPullして最新状態に
2. **編集作業**：iPhone ObsidianでMarkdown編集
3. **終了時**：Working CopyでCommit & Push

### ファイル管理の注意点
- **画像ファイル**：`_resources/`フォルダ内で管理
- **相対パス**を維持してリンク切れを防止
- **大きなファイル**はGitHub容量制限に注意

### 競合回避のベストプラクティス
- **`.obsidian/`フォルダは除外**（.gitignoreで設定）
- **同時編集を避ける**
- **Pull → Edit → Push** の順番を守る

## 📋 トラブルシューティング

### よくある問題

#### 1. ファイルが反映されない
- **原因**: Working CopyとObsidian間のファイル同期漏れ
- **解決**: 手動でファイルをコピー＆ペースト

#### 2. 画像が表示されない
- **原因**: 相対パスの問題
- **解決**: `_resources/`フォルダ構造を維持

#### 3. 競合エラー
- **原因**: 複数デバイスでの同時編集
- **解決**: Working CopyでConflictを手動解決

## 🔍 参考情報

### 関連アプリ
- **Working Copy**（必須）- iOS用Gitクライアント
- **Files**（内蔵）- ファイル間コピーに使用
- **Obsidian**（本体）- Markdown編集

### 有用なリンク
- [Working Copy公式ガイド](https://workingcopyapp.com)
- [Obsidian Sync公式サイト](https://obsidian.md/sync)
- [Obsidian Mobile制限事項](https://help.obsidian.md/Obsidian/Index)

## 📊 同期方法の比較表

| 項目 | Working Copy + GitHub | Obsidian Sync + GitHub | iCloud + GitHub |
|------|----------------------|------------------------|-----------------|
| **初期費用** | $35.99 USD (Working Copy Pro) | 月額$4-5 | 無料 |
| **iPhone操作** | 手動同期必要 | 完全自動 | 完全自動 |
| **設定複雑度** | 高 | 低 | 中 |
| **リアルタイム同期** | ❌ | ✅ | △（iCloud遅延） |
| **バージョン管理** | ✅ | △（Obsidian内） | △（Git側のみ） |
| **学習コスト** | 高（Git知識必要） | 低 | 中 |
| **推奨度** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |

## 🎯 用途別おすすめ

### 🏆 最推奨：Obsidian Sync + GitHub併用
**こんな人におすすめ：**
- 月額$4-5の費用負担が可能
- iPhone/iPadでの編集頻度が高い
- 手動操作を極力避けたい
- 長期的なバックアップも重視

### 📱 技術志向：Working Copy + GitHub
**こんな人におすすめ：**
- Gitの仕組みを理解している
- 手動操作も苦にならない
- 一回の購入で済ませたい（$35.99）
- バージョン管理を重視

### 💰 コスト重視：iCloud + GitHub
**こんな人におすすめ：**
- 費用を抑えたい
- Mac/PCメインで編集する
- iPhone編集は補助的
- 多少の不便は許容できる

## ⚠️ 制限事項まとめ

### Working Copy + GitHub方式
- 🚫 **自動同期不可**（手動操作必須）
- 🚫 **複雑なGit操作不可**（基本的なPull/Pushのみ）
- ✅ **完全なバージョン管理**
- ✅ **買い切りで追加費用なし**

### Obsidian Sync + GitHub方式
- ✅ **完全自動同期**
- ✅ **エンドツーエンド暗号化**
- ❌ **月額費用継続**
- ❌ **デュアル管理の複雑性**

### iCloud + GitHub方式
- ✅ **費用無料**
- ❌ **iCloud同期待機時間**
- ❌ **Mac/PC必須**

