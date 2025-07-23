- Github Copilot Chatにタスクをやる際に、常に細かいタスクに分割して１回で部分的に実行していくような仕組みを作りたい
    1. ユーザーがタスクを入力
    2. ユーザーのタスクの不明点などをGithub Copilot Chatが質問
    3. ユーザーが質問に答える
    4. 詳細が決まったら、Github Copilot Chatがタスクを細かいステップに分割
    5. Github Copilot Chatがまだ完了していないステップを実行（なければ終了）
    6. ユーザー向けにGithub Copilot Chatが行った変更の概要をファイルに出力
    7. 5. のステップに戻る
