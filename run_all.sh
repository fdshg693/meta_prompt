#!/bin/bash

# Meta Prompt 統合実行スクリプト (Bash版)
# GitHub Copilot Chat用プロンプト自動生成システム

# カラー出力用関数
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_info() { echo -e "${CYAN}📋 $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }

# オプション解析
SKIP_CHECKS=false
AUTO_CONFIRM=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-checks)
            SKIP_CHECKS=true
            shift
            ;;
        --auto-confirm)
            AUTO_CONFIRM=true
            shift
            ;;
        *)
            echo "不明なオプション: $1"
            echo "使用法: $0 [--skip-checks] [--auto-confirm]"
            exit 1
            ;;
    esac
done

# ヘッダー表示
clear
echo -e "${MAGENTA}🚀 Meta Prompt 統合実行スクリプト${NC}"
echo -e "${MAGENTA}==================================================${NC}"
print_info "GitHub Copilot Chat用プロンプト自動生成システム"
echo ""

# 1. 前提条件チェック
if [ "$SKIP_CHECKS" = false ]; then
    print_info "前提条件をチェック中..."
    
    # INPUT/task.md の存在確認
    if [ ! -f "INPUT/task.md" ]; then
        print_error "INPUT/task.md が見つかりません"
        print_info "以下のコマンドでファイルを作成してください："
        echo -e "${GRAY}  touch INPUT/task.md${NC}"
        echo -e "${GRAY}  その後、task.mdにプロジェクト要件を記述してください${NC}"
        exit 1
    fi
    
    # VSCode チェック
    if ! command -v code &> /dev/null; then
        print_warning "VSCodeが見つかりません。手動でVSCodeを起動してください"
    fi
    
    # スクリプトファイル存在確認
    required_scripts=("code/modify_prompt_files.sh" "code/merge_copilot_instructions.sh")
    
    for script in "${required_scripts[@]}"; do
        if [ ! -f "$script" ]; then
            print_error "必須スクリプトが見つかりません: $script"
            exit 1
        fi
        
        # 実行権限チェック
        if [ ! -x "$script" ]; then
            print_info "実行権限を付与中: $script"
            chmod +x "$script"
        fi
    done
    
    print_success "前提条件チェック完了"
    echo ""
fi

# 2. タスク内容表示
if [ -f "INPUT/task.md" ]; then
    print_info "現在のタスク内容:"
    echo -e "${GRAY}──────────────────────────────${NC}"
    while IFS= read -r line; do
        echo -e "  ${NC}$line"
    done < "INPUT/task.md"
    echo -e "${GRAY}──────────────────────────────${NC}"
    echo ""
fi

# 3. GitHub Copilot Chat手順の表示
echo -e "${YELLOW}📋 GitHub Copilot Chat での実行手順${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""
print_info "VSCodeでGitHub Copilot Chatを開き、以下のコマンドを順番に実行してください："
echo ""
echo -e "${CYAN}  1. /requirement_analyzer${NC}"
echo -e "${GRAY}     → 要件分析レポートを生成します${NC}"
echo ""
echo -e "${CYAN}  2. /architect_designer${NC}"
echo -e "${GRAY}     → アーキテクチャ設計レポートを生成します${NC}"
echo ""
echo -e "${CYAN}  3. /prompt_generator${NC}"
echo -e "${GRAY}     → エージェント用プロンプトを生成します${NC}"
echo -e "${YELLOW}     ※ 必要に応じて複数回実行してください${NC}"
echo ""
echo -e "${CYAN}  4. /readme${NC}"
echo -e "${GRAY}     → プロジェクト用READMEを生成します${NC}"
echo ""

# 4. ユーザー確認待ち
if [ "$AUTO_CONFIRM" = false ]; then
    echo -e "${YELLOW}⏳ 確認${NC}"
    echo "上記4つのコマンドをGitHub Copilot Chatで実行完了後、Enterキーを押してください"
    read -p "準備ができたらEnterキーを押してください: "
fi

echo ""

# 5. 生成ファイル確認
print_info "生成ファイルを確認中..."

expected_files=("sample/requirement_analysis_report.md" "sample/architect_design_report.md" "sample/README.md")
missing_files=()

for file in "${expected_files[@]}"; do
    if [ -f "$file" ]; then
        print_success "✓ $file"
    else
        print_warning "✗ $file (見つかりません)"
        missing_files+=("$file")
    fi
done

# promptsフォルダのチェック
if [ -d "sample/prompts" ]; then
    prompt_count=$(find sample/prompts -name "*.md" -type f | wc -l)
    if [ "$prompt_count" -gt 0 ]; then
        print_success "✓ sample/prompts/ (ファイル数: $prompt_count)"
    else
        print_warning "✗ sample/prompts/ (プロンプトファイルが見つかりません)"
        missing_files+=("sample/prompts/*.md")
    fi
else
    print_warning "✗ sample/prompts/ (フォルダが見つかりません)"
    missing_files+=("sample/prompts/")
fi

if [ ${#missing_files[@]} -gt 0 ]; then
    echo ""
    print_error "一部のファイルが見つかりません。GitHub Copilot Chatでの実行を確認してください:"
    for file in "${missing_files[@]}"; do
        echo -e "${RED}  - $file${NC}"
    done
    
    read -p "それでも続行しますか？ (y/N): " continue_choice
    if [[ ! "$continue_choice" =~ ^[yY] ]]; then
        print_info "処理を中断しました"
        exit 1
    fi
fi

echo ""

# 6. 自動処理実行
echo -e "${YELLOW}🔄 ファイル変換処理を開始...${NC}"

# プロンプトファイル変換
print_info "プロンプトファイルをGitHub Copilot Chat形式に変換中..."
if ./code/modify_prompt_files.sh; then
    print_success "プロンプトファイル変換完了"
else
    print_warning "プロンプトファイル変換で警告が発生しました"
fi

# 設定ファイルマージ
print_info "設定ファイルをマージ中..."
if ./code/merge_copilot_instructions.sh; then
    print_success "設定ファイルマージ完了"
else
    print_warning "設定ファイルマージで警告が発生しました"
fi

echo ""

# 7. 完了メッセージと次のステップ
echo -e "${GREEN}🎉 処理完了！${NC}"
echo -e "${GREEN}====================${NC}"

if [ -d "sample/.github" ]; then
    print_success "sample/.github/ フォルダが正常に生成されました"
    
    # 生成されたファイル一覧表示
    print_info "生成されたファイル:"
    find sample/.github -type f | while read -r file; do
        echo -e "  📄 ${NC}$file"
    done
else
    print_warning "sample/.github/ フォルダが見つかりません"
fi

echo ""
echo -e "${CYAN}📋 次のステップ:${NC}"
echo "1. 新しいプロジェクトフォルダを作成"
echo "2. sample/.github/ フォルダを新プロジェクトにコピー"
echo "3. sample/README.md も必要に応じてコピー"
echo "4. VSCodeで新プロジェクトを開いてGitHub Copilot Chatを活用"

echo ""
print_info "使用例:"
echo -e "${GRAY}  mkdir my-new-project${NC}"
echo -e "${GRAY}  cp -r sample/.github my-new-project/${NC}"
echo -e "${GRAY}  cp sample/README.md my-new-project/${NC}"
echo -e "${GRAY}  cd my-new-project && code .${NC}"

echo ""
print_success "Meta Promptをご利用いただき、ありがとうございました！"
