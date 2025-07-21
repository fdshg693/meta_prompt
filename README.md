## 概要
Github Copilot Chatに与えるプロンプトを自動生成するためのプロジェクトです。

## 必要条件
- Github Copilot Chatのアカウント
- VSCodeのインストール

## 使い方
1. このリポジトリをクローンします。
2. `INPUT\task.md`にタスクを記述します。
3. `/requirement_analyzer`をGithub Copilot Chatで打ち込みます
4. `sample`フォルダに生成されたファイルを確認します。
    - `sample/requirement_analysis_report.md`が生成され、要件分析の結果が記述されています。
    - `sample/questions.md`が存在すれば、必要に応じて`sample/answers.md`を作成して回答を記述します。直接、`sample/requirement_analysis_report.md`を編集しても構いません。
    - `sample/answers.md`を記述した後、再度`/requirement_analyzer`を実行すると、回答を反映した要件分析が行われます。
5. `/architect_designer`をGithub Copilot Chatで打ち込みます。
    - `sample/architect_design_report.md`が生成され、アーキテクチャ設計の結果が記述されています。
6. `/prompt_generator.prompt`をGithub Copilot Chatで打ち込みます。
    - `sample/prompts/{agent_name}_prompt.md`が生成され、各エージェントのプロンプトが記述されています。
    - 1回の実行で、最大3ファイルまでの生成が行われるため、必要に応じて複数回実行してください。
7. `/readme`をGithub Copilot Chatで打ち込みます。
    - `sample/README.md`が生成され、プロジェクトの進め方が記述されています。
8. `code/`フォルダの配下にある任意のスクリプトを実行しまて、ファイル形式の微修正を行います。
    - `sample/prompts/{agent_name}_prompt.md`を元に、`sample/.github/prompts/{agent_name}_prompt.prompt.md`を作成します。
    - `sample/.github/prompts/{agent_name}_prompt.prompt.md`の先頭ファイルに以下の内容を追加します。（Github Copilot Chatのpromptsの形式に合わせるため）
      ```
      ---
      mode: agent
      ---
      ```    
9. 任意のフォルダを作成し、`sample/.github`フォルダ全体をコピーします。
    - 必要に応じて、`sample/README.md`もコピーすると便利です。
10. VSCodeで新しいフォルダを開き、Github Copilot Chatを起動して、7.で作成した`sample/README.md`の指示に従い進めます。
    - プロンプトを実行する際は、`/{プロンプトファイル名}`のショートカットを入力して実行すると便利です。
   