---
tags: [技術/AI, 技術/開発環境, ガイド, クリッピング]
created: 2025-06-28
updated: 2025-06-28
version: 1.1
---

# Claude Code Windows使用ガイド

## 概要

Claude CodeはAnthropicが開発したAIコーディングアシスタントCLIツールです。WindowsではWSL（Windows Subsystem for Linux）を通じて利用可能です。

⚠️ **重要**: Claude CodeはWindows上でネイティブに動作しません。WSLが必須です。

## WSL（Windows Subsystem for Linux）とは

WSLは**Windows Subsystem for Linux**の略で、Windows上でLinux環境を動作させるMicrosoftの機能です。

### WSLの特徴

- **軽量**: 仮想マシンを使わずに直接Linux環境を実行
- **高速**: 従来の仮想マシンより高速で軽い
- **統合**: WindowsとLinuxファイルシステムの相互アクセス可能
- **開発環境**: Linux用ツールをWindows上で使用可能

### WSL 1 vs WSL 2

| 機能 | WSL 1 | WSL 2 |
|------|--------|--------|
| 速度 | 普通 | 高速 |
| カーネル | 変換レイヤー | 実際のLinuxカーネル |
| Docker対応 | 制限あり | 完全対応 |
| ファイルI/O | 高速 | 非常に高速 |

### なぜClaude CodeでWSLが必要？

Claude CodeはLinux/macOS用に開発されており、以下の理由でWSLが必要です：

- **Linux API依存**: Linux固有のシステムコールを使用
- **ファイルシステム**: Unix形式のパス構造が前提
- **Node.js環境**: Linux版Node.jsでの動作を想定
- **シェル環境**: bash/zshなどUnixシェルが必要

## システム要件

### 対応OS
- **Windows**: WSL経由でのみ利用可能
- **推奨**: Ubuntu 20.04+ / Debian 10+ (WSL内)
- **その他**: macOS 10.15+, Linux（ネイティブサポート）

### 前提条件
- Windows 10 version 2004以降 または Windows 11
- WSL 2
- Node.js 16.0+
- npm

## インストール手順

### Step 1: WSLのインストール

1. **管理者権限でPowerShellを開く**
2. **WSLを有効化**
   ```powershell
   wsl --install
   ```
3. **再起動** - システムの再起動が必要
4. **Ubuntu設定** - 再起動後、Ubuntuが自動でセットアップされます

### Step 2: Linux環境でNode.jsをインストール

WSL内で以下のコマンドを実行：

```bash
# システムパッケージを更新
sudo apt update

# Node.jsとnpmをインストール
sudo apt install nodejs npm

# バージョン確認
node --version
npm --version
```

### Step 3: Claude Codeのインストール

```bash
# グローバルインストール
npm install -g @anthropic-ai/claude-code

# インストール確認
claude --version
```

### Step 4: 認証設定

```bash
# Claude Codeを起動
claude

# 初回起動時にAPI키設定が求められます
# Anthropic APIキーを入力してください
```

## 基本的な使用方法

### 起動コマンド

```bash
# 対話モードで起動
claude

# 初期プロンプト付きで起動
claude "コードレビューをお願いします"

# ワンショット実行
claude -p "この関数を説明して"

# 前回の会話を継続
claude --continue

# 特定のモデルを指定
claude --model claude-sonnet-4-20250514
```

### 便利なオプション

```bash
# 作業ディレクトリを追加
claude --add-dir /path/to/project

# 詳細ログを有効化
claude --verbose

# ファイルからクエリを読み込み
cat file.txt | claude -p "このコードを改善して"

# 会話を再開
claude --resume abc123 "このPRを完成させて"
```

## Windows特有の注意点

### ⚠️ 重要な制限事項

1. **WSLが必須**: Windowsネイティブでは動作しません
2. **ファイルシステム**: Linuxファイルシステム（`~/`）での作業を推奨
3. **パフォーマンス**: `/mnt/c/`（Windowsマウント）は避ける

### 権限関連の注意

```bash
# ❌ 使用禁止 - セキュリティリスク
sudo npm install -g @anthropic-ai/claude-code

# ✅ 推奨 - 通常権限でインストール
npm install -g @anthropic-ai/claude-code
```

### よくあるエラーと対処法

#### 1. "Claude Code is not supported on Windows"

**原因**: Windowsのnpmでインストールしようとしている
**解決法**: WSL内でインストールしてください

#### 2. "exec: node: not found"

**原因**: WSLがWindowsのNode.jsを参照している
**解決法**: 
```bash
# パス確認
which npm
which node

# Linux版Node.jsを再インストール
sudo apt remove nodejs npm
sudo apt install nodejs npm
```

#### 3. 権限エラー

**解決法**: npmのグローバルディレクトリを設定
```bash
# npm設定
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'

# .bashrcに追加
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

## 推奨設定

### 環境変数設定

```bash
# デバッグログを有効化
export ANTHROPIC_LOG=debug

# .bashrcに追加
echo 'export ANTHROPIC_LOG=debug' >> ~/.bashrc
```

### WSL最適化

```bash
# WSL設定ファイル作成
sudo nano /etc/wsl.conf

# 以下を追加
[interop]
appendWindowsPath = false

[automount]
enabled = true
root = /mnt/
options = "metadata,umask=077,fmask=11"
```

## トラブルシューティング

### デバッグ情報の確認

```bash
# ステータス確認
claude /status

# システム情報
uname -a
node --version
npm --version
```

### ログの確認

```bash
# 詳細ログで実行
ANTHROPIC_LOG=debug claude

# ログファイル確認
ls ~/.claude/logs/
```

## パフォーマンス最適化

### 推奨事項

1. **作業場所**: `~/projects/`を使用（`/mnt/c/`は避ける）
2. **WSL 2使用**: WSL 1より高速
3. **メモリ設定**: `.wslconfig`でメモリ制限を調整

### WSL設定例

`C:\Users\[username]\.wslconfig`
```ini
[wsl2]
memory=8GB
processors=4
swap=2GB
```

## 関連リンク

### 公式ドキュメント
- [Claude Code公式ドキュメント](https://docs.anthropic.com/en/docs/claude-code)
- [npm パッケージ](https://www.npmjs.com/package/@anthropic-ai/claude-code)
- [GitHub Issues](https://github.com/anthropics/claude-code/issues)
- [WSL公式ドキュメント](https://docs.microsoft.com/en-us/windows/wsl/)

### 関連記事（このVault内）
- [[Clippings/Ollama 単体では速い LLM が、なぜか Dify や Continue から使うと遅い、という時の解決方法]] - LLM最適化のヒント
- [[Clippings/ノーコードで業務フローを自動化できる｢n8n｣。AI連携もかなり便利そう]] - AI開発環境の拡張
- [[Clippings/【Obsidian】2023 年でオススメのプラグイン 66 選]] - 開発環境の効率化

### 技術関連記事
- [[マインクラフト]] - 開発環境でのゲームサーバー構築
- [[Clippings/SynologyNASでのMinecraftサーバー1.20.4起ち上げから自動バックアップまで]] - Linux環境での自動化事例

## 作成日・更新履歴

- **作成日**: 2025-06-28
- **最終更新**: 2025-06-28
- **バージョン**: 1.1 (WSL詳細説明追加)