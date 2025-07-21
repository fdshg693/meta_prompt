# エージェント・アーキテクチャ設計書

## エージェント構成概要

スイス語学習支援システムを実現するため、6つの専門エージェントによる循環型ワークフローを設計しました。各エージェントは単一責任の原則に基づき、明確に分離された役割を持ちます。

## エージェント構成一覧

### 1. 学習レベル評価エージェント (Level Assessment Agent)
### 2. 学習コンテンツ生成エージェント (Content Generator Agent)
### 3. テスト作成エージェント (Test Creator Agent)
### 4. 採点評価エージェント (Scoring Agent)
### 5. 学習履歴管理エージェント (Learning History Manager Agent)
### 6. 学習パス決定エージェント (Learning Path Optimizer Agent)

## 各エージェントの役割定義

### 1. 学習レベル評価エージェント
**責任範囲**: ユーザーの現在の知識レベルを評価・判定
**専門性**: スイス語能力の測定とレベル判定
**処理内容**:
- 学習履歴の分析
- 現在の知識レベルの判定
- 学習強化が必要な分野の特定

**入力ファイル**:
- `learning_history/user_learning_history.md` (学習履歴データ)

**出力ファイル**:
- `assessment/current_level_assessment.md` (現在レベル評価結果)

### 2. 学習コンテンツ生成エージェント
**責任範囲**: スイス語学習素材の自動生成
**専門性**: スイス語教育コンテンツの作成
**処理内容**:
- 単語帳の生成
- 文法説明の作成
- 短文例の作成
- 読解文（3-5文の段落）の作成

**入力ファイル**:
- `assessment/current_level_assessment.md` (レベル評価結果)
- `learning_path/next_learning_plan.md` (学習計画)

**出力ファイル**:
- `content/vocabulary_list.md` (単語帳)
- `content/grammar_explanation.md` (文法説明)
- `content/short_sentences.md` (短文例)
- `content/reading_passage.md` (読解文)

### 3. テスト作成エージェント
**責任範囲**: 学習内容に基づくテスト問題の作成
**専門性**: スイス語テスト問題の設計と作成
**処理内容**:
- 読解問題の作成
- 選択式問題の作成
- 難易度調整

**入力ファイル**:
- `content/vocabulary_list.md` (単語帳)
- `content/grammar_explanation.md` (文法説明)
- `content/reading_passage.md` (読解文)

**出力ファイル**:
- `test/daily_test_questions.md` (テスト問題)
- `test/answer_key.md` (解答キー)

### 4. 採点評価エージェント
**責任範囲**: テスト結果の採点と学習成果の評価
**専門性**: テスト結果の分析と学習成果の測定
**処理内容**:
- テスト結果の採点
- 正答率の計算
- 弱点分野の特定

**入力ファイル**:
- `test/daily_test_questions.md` (テスト問題)
- `test/answer_key.md` (解答キー)
- `test/user_answers.md` (ユーザー回答)

**出力ファイル**:
- `evaluation/test_results.md` (採点結果)
- `evaluation/performance_analysis.md` (成績分析)

### 5. 学習履歴管理エージェント
**責任範囲**: 学習データの永続化と履歴管理
**専門性**: 学習進捗データの構造化管理
**処理内容**:
- テスト結果の記録
- 学習進捗の更新
- 履歴データの整理

**入力ファイル**:
- `evaluation/test_results.md` (採点結果)
- `evaluation/performance_analysis.md` (成績分析)
- `learning_history/user_learning_history.md` (既存履歴)

**出力ファイル**:
- `learning_history/user_learning_history.md` (更新された学習履歴)
- `learning_history/progress_summary.md` (進捗サマリー)

### 6. 学習パス決定エージェント
**責任範囲**: 次回学習内容の最適化と決定
**専門性**: 適応的学習パスの設計
**処理内容**:
- 学習履歴の分析
- 次回学習内容の決定
- 難易度調整の判断

**入力ファイル**:
- `learning_history/user_learning_history.md` (学習履歴)
- `learning_history/progress_summary.md` (進捗サマリー)

**出力ファイル**:
- `learning_path/next_learning_plan.md` (次回学習計画)

## ワークフロー図

```
開始
  ↓
[1] 学習レベル評価エージェント
  ├─ 入力: learning_history/user_learning_history.md
  └─ 出力: assessment/current_level_assessment.md
  ↓
[2] 学習コンテンツ生成エージェント
  ├─ 入力: assessment/current_level_assessment.md
  ├─ 入力: learning_path/next_learning_plan.md
  ├─ 出力: content/vocabulary_list.md
  ├─ 出力: content/grammar_explanation.md
  ├─ 出力: content/short_sentences.md
  └─ 出力: content/reading_passage.md
  ↓
[3] テスト作成エージェント
  ├─ 入力: content/vocabulary_list.md
  ├─ 入力: content/grammar_explanation.md
  ├─ 入力: content/reading_passage.md
  ├─ 出力: test/daily_test_questions.md
  └─ 出力: test/answer_key.md
  ↓
[ユーザーがテストを受験]
  ↓ (user_answers.md作成)
[4] 採点評価エージェント
  ├─ 入力: test/daily_test_questions.md
  ├─ 入力: test/answer_key.md
  ├─ 入力: test/user_answers.md
  ├─ 出力: evaluation/test_results.md
  └─ 出力: evaluation/performance_analysis.md
  ↓
[5] 学習履歴管理エージェント
  ├─ 入力: evaluation/test_results.md
  ├─ 入力: evaluation/performance_analysis.md
  ├─ 入力: learning_history/user_learning_history.md
  ├─ 出力: learning_history/user_learning_history.md (更新)
  └─ 出力: learning_history/progress_summary.md
  ↓
[6] 学習パス決定エージェント
  ├─ 入力: learning_history/user_learning_history.md
  ├─ 入力: learning_history/progress_summary.md
  └─ 出力: learning_path/next_learning_plan.md
  ↓
翌日の学習サイクルへ（エージェント1に戻る）
```

## データフロー仕様

### ディレクトリ構造
```
project_root/
├── learning_history/
│   ├── user_learning_history.md
│   └── progress_summary.md
├── assessment/
│   └── current_level_assessment.md
├── content/
│   ├── vocabulary_list.md
│   ├── grammar_explanation.md
│   ├── short_sentences.md
│   └── reading_passage.md
├── test/
│   ├── daily_test_questions.md
│   ├── answer_key.md
│   └── user_answers.md
├── evaluation/
│   ├── test_results.md
│   └── performance_analysis.md
└── learning_path/
    └── next_learning_plan.md
```

### ファイル仕様

#### learning_history/user_learning_history.md
- **目的**: 累積的な学習履歴の保存
- **形式**: 日付別の構造化マークダウン
- **内容**: テスト結果、学習内容、進捗指標

#### assessment/current_level_assessment.md
- **目的**: 現在の学習レベル評価結果
- **形式**: レベル判定と推奨学習内容
- **内容**: スキルレベル、強化分野、学習推奨事項

#### content/ (各ファイル)
- **目的**: 日次学習コンテンツ
- **形式**: スイス語学習用構造化マークダウン
- **内容**: レベル別調整された学習素材

#### test/daily_test_questions.md
- **目的**: 日次テスト問題
- **形式**: 問題番号付き構造化形式
- **内容**: 読解・選択問題

#### evaluation/ (各ファイル)
- **目的**: テスト結果と成績分析
- **形式**: 採点結果と分析レポート
- **内容**: 正答率、弱点分析、改善提案

#### learning_path/next_learning_plan.md
- **目的**: 次回学習内容の指針
- **形式**: 学習計画書
- **内容**: 学習目標、重点分野、難易度設定

## アーキテクチャの品質特性

### 責任分離の明確性
- 各エージェントは単一の専門領域に特化
- エージェント間の責任境界が明確に定義
- データの所有権と更新責任が明確

### ワークフローの効率性
- シーケンシャルな処理フローで依存関係を明確化
- 各ステップの入出力が標準化
- 循環型学習サイクルの自動化

### 疎結合設計
- ファイルベースの疎結合インターフェース
- エージェント間の直接依存関係を排除
- 標準化されたマークダウン形式による互換性

### 拡張性
- 新規エージェントの追加が容易
- 既存エージェントの機能拡張が独立して可能
- データ形式の一貫性により将来の機能追加に対応

### 保守性
- 各エージェントの独立性による保守容易性
- 構造化されたファイル管理
- 明確なデータフロー仕様による理解容易性

## 実装上の考慮事項

### GitHub Copilot Chat対応
- 各エージェントはプロンプトベースで実装
- ファイル読み書きによるデータ永続化
- 人間の介入ポイント（テスト受験）の明確化

### マークダウン標準化
- 全データファイルのマークダウン形式統一
- 構造化されたテンプレート使用
- GitHub Copilot Chatでの読み取り容易性確保

### スイス語特性対応
- 標準ドイツ語ベースの段階的学習
- スイス特有表現の適切な導入
- 初心者レベルでの文化的コンテキスト配慮
