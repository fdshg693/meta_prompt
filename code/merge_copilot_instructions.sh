#!/bin/bash
# -*- coding: utf-8 -*-
#
# sample/copilot-instructions.mdの先頭にsample/variables.yamlの内容を追加して、
# sample/.github/copilot-instructions.mdファイルに出力するスクリプト
#

set -euo pipefail

# エラーハンドリング関数
error_exit() {
    echo "❌ $1" >&2
    exit 1
}

# メイン処理
main() {
    # スクリプトのあるディレクトリを基準にパスを設定
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    
    # 入力ファイルのパス
    local variables_file="${script_dir}/sample/variables.yaml"
    local copilot_instructions_file="${script_dir}/sample/copilot-instructions.md"
    
    # 出力ディレクトリとファイルのパス
    local output_dir="${script_dir}/sample/.github"
    local output_file="${output_dir}/copilot-instructions.md"
    
    # 入力ファイルの存在チェック
    if [[ ! -f "$variables_file" ]]; then
        error_exit "エラー: $variables_file が見つかりません。"
    fi
    
    if [[ ! -f "$copilot_instructions_file" ]]; then
        error_exit "エラー: $copilot_instructions_file が見つかりません。"
    fi
    
    # 出力ディレクトリの作成（存在しない場合）
    if [[ ! -d "$output_dir" ]]; then
        echo "ディレクトリを作成中: $output_dir"
        mkdir -p "$output_dir" || error_exit "出力ディレクトリの作成に失敗しました。"
    fi
    
    # ファイルの読み取り可能性チェック
    if [[ ! -r "$variables_file" ]]; then
        error_exit "❌ ファイル読み取り権限エラー: $variables_file"
    fi
    
    if [[ ! -r "$copilot_instructions_file" ]]; then
        error_exit "❌ ファイル読み取り権限エラー: $copilot_instructions_file"
    fi
    
    # variables.yamlの内容を読み込み
    echo "読み込み中: $variables_file"
    local variables_content
    if ! variables_content=$(cat "$variables_file"); then
        error_exit "variables.yamlの読み込みに失敗しました。"
    fi
    
    # copilot-instructions.mdの内容を読み込み
    echo "読み込み中: $copilot_instructions_file"
    local copilot_content
    if ! copilot_content=$(cat "$copilot_instructions_file"); then
        error_exit "copilot-instructions.mdの読み込みに失敗しました。"
    fi
    
    # 結合したコンテンツを作成して出力ファイルに書き込み
    echo "書き込み中: $output_file"
    {
        echo ""
        echo "# Variables Configuration"
        echo '```yaml'
        echo "$variables_content"
        echo '```'
        echo ""
        echo "---"
        echo ""
        echo "$copilot_content"
    } > "$output_file" || error_exit "出力ファイルの書き込みに失敗しました。"
    
    echo "✅ 正常に完了しました。"
    echo "   出力ファイル: $output_file"
    echo "   variables.yaml の内容が copilot-instructions.md の先頭に追加されました。"
}

# スクリプトが直接実行された場合のみメイン関数を呼び出し
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
