# エージェント・アーキテクチャ設計書

## プロジェクト概要
Github Copilot Chatを使用したタスク分割・段階実行システム  
要件分析結果を基に、効率的で保守性の高いエージェント構成を設計

## エージェント構成概要

本システムは**5つの専門エージェント**で構成され、単一責任原則に基づいて設計されています。
各エージェントはファイルベースで情報を受け渡し、順次実行（並列実行なし）によってタスクを完遂します。

### エージェント一覧
1. **要求分析エージェント** (Requirements Analyzer Agent)
2. **タスク分割エージェント** (Task Breakdown Agent) 
3. **実行計画エージェント** (Execution Planning Agent)
4. **実行エージェント** (Execution Agent)
5. **進捗管理エージェント** (Progress Management Agent)

## 各エージェントの役割定義

### 1. 要求分析エージェント (Requirements Analyzer Agent)
**専門領域**: ユーザー要求の理解と明確化

**主要責任**:
- ユーザーからの初期タスク入力を受け取り分析
- 不明点・曖昧な点を特定し、質問項目を生成
- ユーザーの回答を統合し、明確化された要求仕様を出力
- 改善提案機能：より良い代替手法がある場合の提案

**入力ファイル**:
- `input/task_input.json` - ユーザーからの初期タスク
- `input/user_responses.json` - ユーザーの質問回答（2回目以降）

**出力ファイル**:
- `output/clarified_requirements.json` - 明確化された要求仕様
- `output/questions_for_user.json` - ユーザーへの質問項目（必要時）

### 2. タスク分割エージェント (Task Breakdown Agent)
**専門領域**: タスクの論理的分割と構造化

**主要責任**:
- 明確化された要求を実行可能な細かいステップに分割
- ステップ間の依存関係を定義
- 各ステップの実行条件と成功基準を設定
- 分割粒度の最適化（1ファイル修正または小機能追加単位）

**入力ファイル**:
- `output/clarified_requirements.json` - 要求分析エージェントの出力

**出力ファイル**:
- `output/task_breakdown.json` - 分割されたタスクステップ
- `output/step_dependencies.json` - ステップ間依存関係

### 3. 実行計画エージェント (Execution Planning Agent)
**専門領域**: 実行順序の最適化と計画立案

**主要責任**:
- タスクステップの実行順序を決定
- 各ステップの実行方法と手順を詳細化
- エラー時の代替手順を計画
- 実行可能性の事前検証

**入力ファイル**:
- `output/task_breakdown.json` - タスク分割結果
- `output/step_dependencies.json` - 依存関係情報
- `state/execution_state.json` - 現在の実行状態（継続実行時）

**出力ファイル**:
- `output/execution_plan.json` - 詳細実行計画
- `state/execution_queue.json` - 実行待ちステップキュー

### 4. 実行エージェント (Execution Agent)
**専門領域**: 実際のタスクステップ実行

**主要責任**:
- 計画に基づいた各ステップの実行
- コード作成・修正・バグ修正の実装
- エラー検出と自動修正の試行
- 実行結果の検証と記録

**入力ファイル**:
- `output/execution_plan.json` - 実行計画
- `state/execution_queue.json` - 実行キュー
- `state/execution_state.json` - 現在の実行状態

**出力ファイル**:
- `output/execution_results.json` - 実行結果詳細
- `state/execution_state.json` - 更新された実行状態
- `logs/execution_log.json` - 実行ログ

### 5. 進捗管理エージェント (Progress Management Agent)
**専門領域**: 進捗追跡と完了判定

**主要責任**:
- 全体進捗の追跡と管理
- 完了ステップと未完了ステップの管理
- ユーザー向け進捗レポートの生成
- 完了判定とループ継続の決定

**入力ファイル**:
- `output/execution_results.json` - 実行結果
- `state/execution_state.json` - 実行状態
- `logs/execution_log.json` - 実行ログ

**出力ファイル**:
- `reports/progress_report.md` - ユーザー向け進捗レポート
- `reports/change_summary.md` - 変更概要サマリー
- `state/completion_status.json` - 完了状態判定

## ワークフロー図

```
[1] 要求分析エージェント
    ↓ clarified_requirements.json
[2] タスク分割エージェント  
    ↓ task_breakdown.json + step_dependencies.json
[3] 実行計画エージェント
    ↓ execution_plan.json + execution_queue.json
[4] 実行エージェント
    ↓ execution_results.json + 更新されたexecution_state.json
[5] 進捗管理エージェント
    ↓ completion_status.json + progress_report.md

継続判定: 未完了ステップあり？
├─ YES → [3] 実行計画エージェントに戻る (ループ)
└─ NO  → 完了

初回実行時の質問対応:
[1] 要求分析エージェント → questions_for_user.json
↓ (ユーザー回答後)
[1] 要求分析エージェント (user_responses.json使用)
```

## データフロー仕様

### ディレクトリ構造
```
project_root/
├── input/           # ユーザー入力
├── output/          # エージェント間の中間出力
├── state/           # 実行状態管理
├── logs/            # 実行ログ
└── reports/         # ユーザー向けレポート
```

### ファイル仕様詳細

#### 入力ファイル
- **`input/task_input.json`**: ユーザーの初期タスク
  ```json
  {
    "task_description": "string",
    "task_type": "programming|bugfix|feature",
    "timestamp": "ISO8601"
  }
  ```

- **`input/user_responses.json`**: ユーザーの質問回答
  ```json
  {
    "responses": [
      {
        "question_id": "string",
        "answer": "string"
      }
    ],
    "timestamp": "ISO8601"
  }
  ```

#### 状態管理ファイル
- **`state/execution_state.json`**: 実行状態
  ```json
  {
    "current_step": "string",
    "completed_steps": ["string"],
    "failed_steps": ["string"],
    "last_updated": "ISO8601"
  }
  ```

- **`state/execution_queue.json`**: 実行待ちキュー
  ```json
  {
    "queue": [
      {
        "step_id": "string",
        "priority": "number",
        "dependencies": ["string"]
      }
    ]
  }
  ```

#### 出力ファイル
- **`reports/progress_report.md`**: ユーザー向け進捗レポート
- **`reports/change_summary.md`**: 実行した変更の概要
- **`logs/execution_log.json`**: 詳細実行ログ

## ループ実行機能

### 実行順序
1. **初回実行**: [1]→[2]→[3]→[4]→[5]
2. **継続実行**: [3]→[4]→[5] (未完了ステップがある限り継続)
3. **質問対応**: [1]で質問発生時、ユーザー回答後に[1]から再実行

### ループ制御
- **継続条件**: `state/execution_state.json`の未完了ステップ存在
- **終了条件**: 全ステップ完了 または 実行不可能なエラー発生
- **状態保持**: ファイルベースで実行状態を永続化

### エラー処理
- **自動修正**: 実行エージェントが3回まで自動修正を試行
- **エスカレーション**: 修正失敗時は進捗管理エージェントに報告
- **継続判定**: 致命的エラー時はループを安全に終了

## 設計原則の実装

### 単一責任原則
- 各エージェントは明確に分離された単一の責任を持つ
- 責任の重複や曖昧さを排除

### 拡張性
- 新しいタスクタイプは要求分析エージェントの拡張で対応
- 新しい実行方法は実行エージェントの拡張で対応
- ファイルベースの疎結合により、個別エージェントの独立改修が可能

### 保守性
- 標準化されたJSON形式でのデータ交換
- 明確なファイル命名規則とディレクトリ構造
- 包括的なログ記録による問題追跡機能

## 品質基準

### 責任分離の明確性
- ✅ 各エージェントの責任範囲が重複なく定義
- ✅ インターフェース（入出力ファイル）が明確に規定
- ✅ エージェント間の依存関係が最小化

### ワークフローの効率性
- ✅ 不要な処理の重複を排除
- ✅ 並列実行不要な単純なシーケンシャル処理
- ✅ 状態管理によるループ実行の最適化

---

**設計完了日**: 2025年7月23日  
**基盤要件**: Github Copilot Chat + ファイルベース状態管理  
**対象スコープ**: 小～中規模プログラミングタスクの自動分割・実行
