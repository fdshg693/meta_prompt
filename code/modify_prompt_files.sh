#!/bin/bash
# プロンプトファイルを修正するスクリプト
#
# 使用方法:
#   # 実行権限を付与（Linux/macOS）
#   chmod +x code/modify_prompt_files.sh
#   
#   # 実行
#   ./code/modify_prompt_files.sh
#   
#   # Windows環境では Git Bash または WSL で実行
#
# このスクリプトは以下の処理を行います：
# sample/prompts/{agent_name}_prompt.md を元にする。
# sample/.github/prompts/{agent_name}_prompt.prompt.md に本番環境で利用するための完成ファイルを作成する

set -e  # エラーが発生したら終了

# ベースディレクトリを取得（スクリプトの親ディレクトリ）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
PROMPTS_DIR="$BASE_DIR/sample/prompts"
GITHUB_DIR="$BASE_DIR/sample/.github/prompts"

echo "プロンプトディレクトリを確認中: $PROMPTS_DIR"
echo "GitHub用出力ディレクトリ: $GITHUB_DIR"

# プロンプトディレクトリが存在しない場合は作成
if [ ! -d "$PROMPTS_DIR" ]; then
    echo "ディレクトリが存在しません: $PROMPTS_DIR"
    mkdir -p "$PROMPTS_DIR"
    echo "ディレクトリを作成しました: $PROMPTS_DIR"
    exit 0
fi

# GitHub用出力ディレクトリが存在しない場合は作成
mkdir -p "$GITHUB_DIR"
echo "GitHub用出力ディレクトリを準備: $GITHUB_DIR"

# *_prompt.mdファイルを検索
PROMPT_FILES=("$PROMPTS_DIR"/*_prompt.md)

# ファイルが存在しない場合の処理
if [ ! -e "${PROMPT_FILES[0]}" ]; then
    echo "*_prompt.mdファイルが見つかりません。"
    exit 0
fi

echo "${#PROMPT_FILES[@]}個のプロンプトファイルを発見しました。"

# front matterの内容
FRONT_MATTER="---
mode: agent
---

"

# 各プロンプトファイルを処理
for prompt_file in "${PROMPT_FILES[@]}"; do
    if [ -f "$prompt_file" ]; then
        # ファイル名を取得
        filename=$(basename "$prompt_file")
        agent_name="${filename%_prompt.md}"
        echo ""
        echo "処理中: $agent_name"
        
        # 1. 本番環境用ファイルのパスを作成
        github_file="$GITHUB_DIR/${agent_name}_prompt.prompt.md"
        
        # 2. 元ファイルの内容を読み込み、front matterの重複をチェック
        if head -n 3 "$prompt_file" | grep -q "^---$" && head -n 3 "$prompt_file" | grep -q "mode: agent"; then
            echo "  front matterが既に存在するため、そのまま使用します"
            cp "$prompt_file" "$github_file"
        else
            # front matterを追加して本番環境用ファイルを作成
            {
                echo "$FRONT_MATTER"
                cat "$prompt_file"
            } > "$github_file"
        fi
        
        echo "  本番環境用ファイルを作成: $(basename "$github_file")"
    fi
done

echo ""
echo "プロンプトファイルの修正が完了しました。"
