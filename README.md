# Meta Prompt - GitHub Copilot Chat用プロンプト自動生成システム

## 🎯 プロジェクトの目的・背景

### 解決する課題
GitHub Copilot Chatを効果的に活用するには、適切なプロンプト設計が重要ですが、以下の課題がありました：

- **プロンプト設計の複雑さ**: 効果的なプロンプトを一から作成するのは時間がかかる
- **一貫性の欠如**: プロジェクトごとに異なるプロンプト品質
- **再利用性の低さ**: 類似プロジェクトでもプロンプトを再作成する必要
- **専門知識の要求**: プロンプトエンジニアリングの知識が必要

### 提供する価値
Meta Promptは、これらの課題を解決する**自動化されたプロンプト生成システム**です：

✅ **時間短縮**: 手動でのプロンプト作成時間を90%削減  
✅ **品質向上**: 体系的なワークフローによる高品質なプロンプト生成  
✅ **再利用性**: テンプレート化による効率的な開発  
✅ **標準化**: 一貫したプロンプト形式とベストプラクティス  

## 🏗️ システムアーキテクチャ

### エージェント指向設計
Meta Promptは4つの専門エージェントによる段階的処理を採用しています：

```
[入力] task.md
    ↓
┌─────────────────────┐
│ 1. 要件分析エージェント │ ← 要件の詳細化・質問生成
│ (requirement_analyzer)│
└─────────────────────┘
    ↓
┌─────────────────────┐
│ 2. アーキテクチャ設計  │ ← システム設計・技術選定
│ (architect_designer) │
└─────────────────────┘
    ↓
┌─────────────────────┐
│ 3. プロンプト生成     │ ← エージェント別プロンプト作成
│ (prompt_generator)   │
└─────────────────────┘
    ↓
┌─────────────────────┐
│ 4. README生成       │ ← プロジェクト進行手順書作成
│ (readme_generator)  │
└─────────────────────┘
    ↓
[出力] GitHub Copilot Chat対応プロンプト群
```

### 各エージェントの役割

| エージェント | 役割 | 入力 | 出力 |
|------------|------|------|------|
| **要件分析エージェント** | タスクの詳細分析・質問生成 | task.md | requirement_analysis_report.md |
| **アーキテクチャ設計** | システム設計・技術スタック決定 | 要件分析結果 | architect_design_report.md |
| **プロンプト生成** | 専門エージェント用プロンプト作成 | 設計結果 | {agent_name}_prompt.md |
| **README生成** | プロジェクト進行手順書作成 | 全体設計 | README.md |

## 🔧 必要条件
- GitHub Copilot Chatのアカウント
- VSCode (GitHub Copilot拡張機能付き)
- Python 3.7以上 (オプション機能用)

## 🚀 クイックスタート

### ⚡ ワンクリック実行（推奨）

**統合実行スクリプト**で全プロセスを自動化できます：

#### 使用方法
```bash
# PowerShell版（Windows推奨）
.\run_all.ps1

# Bash版（Linux/Mac）
./run_all.sh

# Python版（クロスプラットフォーム）
python run_all.py
```

#### オプション
```bash
# 前提条件チェックをスキップ
.\run_all.ps1 -SkipChecks

# 確認プロンプトを自動で進める
.\run_all.ps1 -AutoConfirm

# 両方のオプションを使用
python run_all.py --skip-checks --auto-confirm
```

**統合スクリプトが自動実行する処理**:
1. ✅ 前提条件チェック（必須ファイル・環境確認）
2. 📋 GitHub Copilot Chat実行手順の表示
3. ⏳ ユーザー実行待ち（4つのエージェントコマンド）
4. 🔍 生成ファイルの確認
5. 🔄 プロンプトファイルの自動変換
6. 🔗 設定ファイルの自動マージ
7. 🎉 完了報告と次のステップ案内

### 基本的な使い方（3ステップ）

1. **タスクの記述**
   ```bash
   # INPUT/task.mdにプロジェクト要件を記述
   echo "Webアプリケーションを作成したい" > INPUT/task.md
   ```

2. **プロンプト生成実行**
   - VSCodeでGitHub Copilot Chatを開く
   - 以下のコマンドを順番に実行：
     ```
     /requirement_analyzer
     /architect_designer  
     /prompt_generator
     /readme
     ```

3. **プロンプトファイルの設置**
   ```bash
   # 自動処理スクリプトを実行
   .\code\modify_prompt_files.ps1
   .\code\merge_copilot_instructions.ps1
   ```

### 📋 詳細手順

#### ステップ1: 初期設定
1. **リポジトリのクローン**
   ```bash
   git clone [repository-url]
   cd meta_prompt
   ```

2. **タスクの記述**
   - `INPUT\task.md`を編集してプロジェクト要件を記述します

#### ステップ2: 要件分析
1. **要件分析エージェントの実行**
   ```
   /requirement_analyzer
   ```
   
   📝 **生成ファイル**: `sample/requirement_analysis_report.md`
   
   ❓ **追加質問がある場合**:
   - `sample/question{番号}.md` → `sample/answer{番号}.md`で回答
   - または `sample/requirement_analysis_report.md`を直接編集
   - 回答後、再度 `/requirement_analyzer` を実行

#### ステップ3: アーキテクチャ設計
1. **設計エージェントの実行**
   ```
   /architect_designer
   ```
   
   📝 **生成ファイル**: `sample/architect_design_report.md`

#### ステップ4: プロンプト生成
1. **プロンプト生成エージェントの実行**
   ```
   /prompt_generator
   ```
   
   📝 **生成ファイル**: `sample/prompts/{agent_name}_prompt.md`
   
   ⚠️ **注意**: 1回の実行で最大3ファイル生成。必要に応じて複数回実行

#### ステップ5: README生成
1. **README生成エージェントの実行**
   ```
   /readme
   ```
   
   📝 **生成ファイル**: `sample/README.md`

#### ステップ6: ファイル形式の調整
1. **プロンプトファイルの変換** (以下のいずれかを実行)
   ```bash
   # PowerShell
   .\code\modify_prompt_files.ps1
   
   # Bash
   ./code/modify_prompt_files.sh
   
   # Python
   python code/modify_prompt_files.py
   ```
   
   🔄 **処理内容**: 
   - `sample/prompts/` → `sample/.github/prompts/`
   - GitHub Copilot Chat形式に変換（Front Matter追加）

#### ステップ7: 設定ファイルのマージ
1. **設定ファイルの統合** (以下のいずれかを実行)
   ```bash
   # PowerShell  
   .\code\merge_copilot_instructions.ps1
   
   # Bash
   ./code/merge_copilot_instructions.sh
   
   # Python
   python code/merge_copilot_instructions.py
   ```
   
   🔄 **処理内容**: 
   - `variables.yaml` + `copilot-instructions.md` → `.github/copilot-instructions.md`

#### ステップ8: プロジェクトのセットアップ
1. **新しいプロジェクトフォルダの作成**
   ```bash
   mkdir my-new-project
   cd my-new-project
   ```

2. **生成ファイルのコピー**
   ```bash
   # .githubフォルダ全体をコピー
   cp -r ../meta_prompt/sample/.github ./
   
   # READMEもコピー（推奨）
   cp ../meta_prompt/sample/README.md ./
   ```

3. **VSCodeでプロジェクトを開く**
   ```bash
   code .
   ```

#### ステップ9: プロジェクト開発の開始
1. **フォルダ構成の作成**
   - GitHub Copilot Chatで以下を実行：
   ```
   このREADMEの構成になるようにファイルを作成して
   ファイルの中身は必ず空にして！！！
   ```

2. **エージェントプロンプトの実行**
   ```
   /{プロンプトファイル名}
   ```

## 🔧 高度な機能

### 変数システム
プロンプトテンプレートで変数置換を使用できます：

```bash
# 変数置換の実行
python code/process_prompt_templates.py
```

**設定ファイル**: `code/config/paths.json`  
**変数定義**: `sample/variables.yaml`  
**出力先**: `sample/processed/.github/`

## ⚠️ トラブルシューティング

### よくあるエラーと解決方法

#### 1. `ファイルが見つかりません` エラー
```
エラー: sample/requirement_analysis_report.md が見つかりません
```

**原因**: 前のステップが完了していない  
**解決方法**: 
1. `/requirement_analyzer` を実行して要件分析を完了させる
2. `sample/` フォルダが存在することを確認
3. VSCodeでGitHub Copilot Chatが正常に動作することを確認

#### 2. PowerShellスクリプト実行エラー
```
エラー: このシステムではスクリプトの実行が無効になっています
```

**解決方法**: 
```powershell
# 実行ポリシーを変更
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# または、Bypass を使用
powershell -ExecutionPolicy Bypass -File .\code\modify_prompt_files.ps1
```

#### 3. Python環境エラー
```
エラー: 'python' は内部コマンドまたは外部コマンドとして認識されていません
```

**解決方法**: 
1. Python 3.7以上をインストール
2. 環境変数PATHにPythonを追加
3. または `py` コマンドを使用: `py code/modify_prompt_files.py`

#### 4. GitHub Copilot Chat応答なし
**原因**: 
- GitHub Copilot Chatのセッション期限切れ
- プロンプトファイルが正しく読み込まれていない

**解決方法**: 
1. VSCodeを再起動
2. GitHub Copilot拡張機能を再有効化
3. プロンプトファイルのパスを確認

### 実行前チェックリスト

#### 必須事項
- [ ] GitHub Copilot Chatアカウント有効
- [ ] VSCodeにGitHub Copilot拡張機能インストール済み
- [ ] `INPUT/task.md`にタスク記述済み
- [ ] リポジトリを正しくクローン済み

#### 各ステップ後の確認事項
- [ ] **要件分析後**: `sample/requirement_analysis_report.md` 存在確認
- [ ] **設計後**: `sample/architect_design_report.md` 存在確認  
- [ ] **プロンプト生成後**: `sample/prompts/` フォルダ内にファイル存在確認
- [ ] **README生成後**: `sample/README.md` 存在確認
- [ ] **変換後**: `sample/.github/prompts/` フォルダ存在確認

## ❓ FAQ (よくある質問)

### 基本的な質問

**Q: GitHub Copilot Chatがない場合は使用できませんか？**  
A: 本システムはGitHub Copilot Chat専用に設計されています。代替手段として、生成されたプロンプトを他のAIチャットサービスで利用することは可能ですが、最適化はされていません。

**Q: 無料で使用できますか？**  
A: Meta Prompt自体は無料ですが、GitHub Copilot Chatの有料サブスクリプションが必要です。

**Q: 日本語のタスクでも動作しますか？**  
A: はい、日本語でのタスク記述に対応しています。ただし、生成されるプロンプトは英語になる場合があります。

### 技術的な質問

**Q: 生成されるプロンプトはカスタマイズできますか？**  
A: はい、以下の方法でカスタマイズ可能です：
- `sample/variables.yaml` で変数を定義
- `sample/copilot-instructions.md` で基本指示を編集
- 生成後のプロンプトファイルを直接編集

**Q: 複数のプロジェクトで同時に使用できますか？**  
A: はい、プロジェクトごとに別々のフォルダで実行することを推奨します。

**Q: 生成されたプロンプトが期待通りでない場合は？**  
A: 以下を試してください：
1. `INPUT/task.md` の記述をより詳細にする
2. 要件分析段階で追加質問に回答する
3. 生成後のファイルを手動で調整する

### カスタマイズ・拡張

**Q: 新しいエージェントを追加できますか？**  
A: 現在の版では、4つのエージェント（要件分析、設計、プロンプト生成、README生成）が固定されています。将来版で拡張予定です。

**Q: プロンプトテンプレートを変更したい場合は？**  
A: GitHub Copilot Chat内のプロンプトファイル（`.github/prompts/`）を直接編集するか、変数システムを活用してください。

**Q: 他のAIサービス（ChatGPT、Claude等）対応予定は？**  
A: 現在は計画されていませんが、コミュニティからの要望があれば検討いたします。

## 📁 ファイル・フォルダ構成

### 入力ファイル
```
INPUT/
└── task.md                 # プロジェクト要件の記述
```

### 処理用スクリプト
```
code/
├── config/
│   └── paths.json         # パス設定
├── modify_prompt_files.*  # プロンプト形式変換
├── merge_copilot_instructions.*  # 設定ファイル統合
├── process_prompt_templates.py   # 変数置換処理
├── config_loader.py       # 設定読み込み
└── variable_loader.py     # 変数読み込み
```

### 出力ファイル
```
sample/
├── requirement_analysis_report.md    # 要件分析結果
├── architect_design_report.md        # 設計結果  
├── README.md                         # プロジェクト手順書
├── variables.yaml                    # 変数定義
├── copilot-instructions.md           # 基本指示
├── prompts/                          # 生成プロンプト（中間）
│   └── {agent_name}_prompt.md
├── .github/                          # GitHub Copilot Chat用（最終）
│   ├── copilot-instructions.md
│   └── prompts/
│       └── {agent_name}_prompt.prompt.md
└── processed/                        # 変数置換後（オプション）
    └── .github/
```

## 🤝 コントリビューション

### バグ報告・機能要望
GitHubのIssuesでバグ報告や機能要望をお寄せください。

### 開発への参加
1. リポジトリをフォーク
2. フィーチャーブランチを作成
3. 変更をコミット
4. プルリクエストを作成

### ライセンス
このプロジェクトはMITライセンスの下で公開されています。