# エージェント・アーキテクチャ実行システム

## プロジェクト概要
GitHub Copilot Chatを使用した5つの専門エージェントによるタスク分割・段階実行システムです。
単一責任原則に基づいて設計された各エージェントが順次実行され、複雑なプログラミングタスクを効率的に完遂します。

## システム構成
本システムは以下の5つの専門エージェントで構成されています：

1. **要求分析エージェント** - ユーザー要求の理解と明確化
2. **タスク分割エージェント** - タスクの論理的分割と構造化  
3. **実行計画エージェント** - 実行順序の最適化と計画立案
4. **実行エージェント** - 実際のタスクステップ実行
5. **進捗管理エージェント** - 進捗追跡と完了判定

## 実行手順

### 事前準備
1. プロジェクトディレクトリの作成
2. 必要なフォルダ構造の設定：
```
project_root/
├── input/           # ユーザー入力
├── output/          # エージェント間の中間出力
├── state/           # 実行状態管理
├── logs/            # 実行ログ
└── reports/         # ユーザー向けレポート
```

### ステップ1: 要求分析の実行
GitHub Copilot Chatで以下のプロンプトを実行：
```
/requirements_analyzer
```

**入力ファイル準備:**
- `input/task_input.json` - 実行したいタスクの詳細を記述

**期待される出力:**
- `output/clarified_requirements.json` - 明確化された要求仕様
- `output/questions_for_user.json` - 追加質問（必要時）

**質問がある場合:**
1. `input/user_responses.json`にユーザー回答を記述
2. 再度`/requirements_analyzer`を実行

### ステップ2: タスク分割の実行
```
/task_breakdown
```

**期待される出力:**
- `output/task_breakdown.json` - 分割されたタスクステップ
- `output/step_dependencies.json` - ステップ間依存関係

### ステップ3: 実行計画の立案
```
/execution_planning
```

**期待される出力:**
- `output/execution_plan.json` - 詳細実行計画
- `state/execution_queue.json` - 実行待ちステップキュー

### ステップ4: タスクの実行
```
/execution_agent
```

**期待される出力:**
- `output/execution_results.json` - 実行結果詳細
- `state/execution_state.json` - 更新された実行状態
- `logs/execution_log.json` - 実行ログ

### ステップ5: 進捗管理と完了判定
```
/progress_management
```

**期待される出力:**
- `reports/progress_report.md` - ユーザー向け進捗レポート
- `reports/change_summary.md` - 変更概要サマリー
- `state/completion_status.json` - 完了状態判定

### ループ実行
完了判定で未完了ステップがある場合、自動的にステップ3から再実行されます：
- **継続実行**: ステップ3→4→5の繰り返し
- **終了条件**: 全ステップ完了 または 実行不可能なエラー発生

## ファイル構成と役割

### 入力ファイル
| ファイル | 役割 | 形式 |
|---------|------|------|
| `input/task_input.json` | 初期タスク入力 | JSON |
| `input/user_responses.json` | ユーザー質問回答 | JSON |

### 状態管理ファイル
| ファイル | 役割 | 更新エージェント |
|---------|------|----------------|
| `state/execution_state.json` | 実行状態管理 | 実行エージェント |
| `state/execution_queue.json` | 実行待ちキュー | 実行計画エージェント |
| `state/completion_status.json` | 完了状態判定 | 進捗管理エージェント |

### 出力・レポートファイル
| ファイル | 役割 | 生成エージェント |
|---------|------|----------------|
| `output/clarified_requirements.json` | 明確化された要求 | 要求分析エージェント |
| `output/task_breakdown.json` | タスク分割結果 | タスク分割エージェント |
| `output/execution_plan.json` | 実行計画 | 実行計画エージェント |
| `output/execution_results.json` | 実行結果 | 実行エージェント |
| `reports/progress_report.md` | 進捗レポート | 進捗管理エージェント |
| `reports/change_summary.md` | 変更サマリー | 進捗管理エージェント |
| `logs/execution_log.json` | 実行ログ | 実行エージェント |

## ワークフロー図
```
初回実行フロー:
[1] 要求分析 → [2] タスク分割 → [3] 実行計画 → [4] 実行 → [5] 進捗管理

継続実行フロー:
[3] 実行計画 → [4] 実行 → [5] 進捗管理
    ↑_________________________________↓
              未完了ステップあり

質問対応フロー:
[1] 要求分析 → 質問生成 → ユーザー回答 → [1] 要求分析（再実行）
```

## 実行例

### 初期タスクの設定
`input/task_input.json`の例：
```json
{
    "task_description": "Webアプリケーションに新しいユーザー認証機能を追加する",
    "task_type": "feature",
    "timestamp": "2025-07-23T10:00:00Z"
}
```

### 実行コマンドの順序
1. `/requirements_analyzer` - 要求を分析・明確化
2. `/task_breakdown` - タスクを実行可能な単位に分割
3. `/execution_planning` - 実行順序と手順を計画
4. `/execution_agent` - 実際にコードを実装
5. `/progress_management` - 進捗確認と次のステップ決定

未完了ステップがある場合、手順3-5を繰り返し実行します。

## エラー処理
- **自動修正**: 実行エージェントが最大3回まで自動修正を試行
- **エスカレーション**: 修正失敗時は進捗管理エージェントに報告
- **安全終了**: 致命的エラー時はループを安全に終了

## 設計原則
- **単一責任**: 各エージェントは明確に分離された単一の責任を持つ
- **ファイルベース通信**: エージェント間はJSONファイルで情報を交換
- **状態保持**: 実行状態をファイルで永続化し、中断・再開が可能
- **段階的実行**: 順次実行により処理の透明性と制御性を確保

---
**システム基盤**: GitHub Copilot Chat + ファイルベース状態管理  
**対象スコープ**: 小〜中規模プログラミングタスクの自動分割・実行  
**設計完了日**: 2025年7月23日
