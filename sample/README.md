# スイス語学習支援システム

## プロジェクト概要

このプロジェクトは、6つの専門エージェントによる循環型ワークフローを使用して、個人に最適化されたスイス語学習体験を提供するシステムです。各エージェントは特定の責任を持ち、連携して継続的な学習サイクルを実現します。

## システム構成

### エージェント構成一覧
1. **学習レベル評価エージェント** - ユーザーの現在の知識レベルを評価
2. **学習コンテンツ生成エージェント** - レベルに応じた学習素材を自動生成
3. **テスト作成エージェント** - 学習内容に基づくテスト問題を作成
4. **採点評価エージェント** - テスト結果の採点と学習成果の評価
5. **学習履歴管理エージェント** - 学習データの永続化と履歴管理
6. **学習パス決定エージェント** - 次回学習内容の最適化と決定

## プロジェクトの進め方

### ステップ1: プロジェクト構造の準備

まず、以下のディレクトリ構造を作成してください：

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

### ステップ2: 各エージェントのプロンプト作成

`prompts/` ディレクトリにある以下のプロンプトファイルを確認し、必要に応じてカスタマイズしてください：

- `level_assessment_agent_prompt.md` - レベル評価エージェント用
- `content_generator_agent_prompt.md` - コンテンツ生成エージェント用
- `test_creator_agent_prompt.md` - テスト作成エージェント用
- `scoring_agent_prompt.md` - 採点評価エージェント用
- `learning_history_manager_agent_prompt.md` - 履歴管理エージェント用
- `learning_path_optimizer_agent_prompt.md` - 学習パス決定エージェント用

### ステップ3: 初期設定とワークフロー開始

#### 3.1 初期学習履歴の作成
`learning_history/user_learning_history.md` に初期の学習者情報を設定します。

#### 3.2 ワークフロー実行順序

毎日の学習サイクルは以下の順序で実行してください：

1. **学習レベル評価エージェント実行**
   - 入力: `learning_history/user_learning_history.md`
   - 出力: `assessment/current_level_assessment.md`

2. **学習コンテンツ生成エージェント実行**
   - 入力: `assessment/current_level_assessment.md`, `learning_path/next_learning_plan.md`
   - 出力: `content/` ディレクトリ内の各学習素材ファイル

3. **テスト作成エージェント実行**
   - 入力: `content/` ディレクトリの学習素材
   - 出力: `test/daily_test_questions.md`, `test/answer_key.md`

4. **ユーザーがテストを受験**
   - `test/user_answers.md` にユーザーの回答を記録

5. **採点評価エージェント実行**
   - 入力: テスト問題、解答キー、ユーザー回答
   - 出力: `evaluation/test_results.md`, `evaluation/performance_analysis.md`

6. **学習履歴管理エージェント実行**
   - 入力: 評価結果と既存履歴
   - 出力: 更新された学習履歴とサマリー

7. **学習パス決定エージェント実行**
   - 入力: 学習履歴とサマリー
   - 出力: `learning_path/next_learning_plan.md`

### ステップ4: GitHub Copilot Chatでの実行

各エージェントは GitHub Copilot Chat で実行できるように設計されています：

1. 対応するプロンプトファイルを開く
2. GitHub Copilot Chat でプロンプトを使用
3. 入力ファイルを指定して実行
4. 出力ファイルを確認・保存

## 重要なポイント

### データフロー管理
- 各エージェントは標準化されたマークダウン形式でデータを交換
- ファイルベースの疎結合設計により、各エージェントは独立して動作
- 明確な入出力仕様により、データの整合性を確保

### 学習の継続性
- 循環型ワークフローにより、毎日の学習が前日の結果を活用
- 学習履歴の蓄積により、個人に最適化された学習パスを提供
- 適応的な難易度調整機能

### カスタマイズポイント
- 各エージェントのプロンプトは学習者のニーズに応じて調整可能
- スイス語の特殊性（標準ドイツ語ベース）に対応
- 初心者から上級者まで対応可能な柔軟な設計

## トラブルシューティング

### よくある問題と解決方法

1. **ファイルが見つからない**
   - プロジェクト構造が正しく作成されているか確認
   - 絶対パスまたは相対パスが正しいか確認

2. **エージェントの出力が期待と異なる**
   - 入力ファイルの内容と形式を確認
   - プロンプトファイルの指示が明確か確認

3. **学習進捗が反映されない**
   - 学習履歴ファイルが正しく更新されているか確認
   - ワークフローの実行順序が正しいか確認

## 拡張性

このシステムは以下の拡張が可能です：
- 新しい学習コンテンツタイプの追加
- より高度なテスト形式の導入
- 他の言語への対応
- AI モデルの統合による自動化の向上

詳細な技術仕様については `agent_architecture_design.md` を参照してください。