#!/usr/bin/env python3
"""
Meta Prompt 統合実行スクリプト (Python版)
GitHub Copilot Chat用プロンプト自動生成システム
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# カラー出力用クラス
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    GRAY = '\033[0;37m'
    NC = '\033[0m'  # No Color

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.NC}")

def print_info(message):
    print(f"{Colors.CYAN}📋 {message}{Colors.NC}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.NC}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.NC}")

def clear_screen():
    """画面をクリア"""
    os.system('cls' if os.name == 'nt' else 'clear')

def check_file_exists(file_path, description=""):
    """ファイルの存在確認"""
    if Path(file_path).exists():
        print_success(f"✓ {file_path} {description}")
        return True
    else:
        print_warning(f"✗ {file_path} (見つかりません) {description}")
        return False

def run_script(script_path):
    """スクリプトを実行"""
    try:
        if script_path.endswith('.ps1'):
            # PowerShellスクリプト
            result = subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', script_path], 
                                  capture_output=True, text=True)
        elif script_path.endswith('.sh'):
            # Bashスクリプト
            # 実行権限を確認・付与
            os.chmod(script_path, 0o755)
            result = subprocess.run(['bash', script_path], capture_output=True, text=True)
        elif script_path.endswith('.py'):
            # Pythonスクリプト
            result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        else:
            print_error(f"未対応のスクリプト形式: {script_path}")
            return False
        
        if result.returncode == 0:
            return True
        else:
            print_warning(f"スクリプト実行で警告: {result.stderr}")
            return False
            
    except Exception as e:
        print_error(f"スクリプト実行エラー: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Meta Prompt 統合実行スクリプト')
    parser.add_argument('--skip-checks', action='store_true', help='前提条件チェックをスキップ')
    parser.add_argument('--auto-confirm', action='store_true', help='確認プロンプトをスキップ')
    args = parser.parse_args()

    # ヘッダー表示
    clear_screen()
    print(f"{Colors.MAGENTA}🚀 Meta Prompt 統合実行スクリプト{Colors.NC}")
    print(f"{Colors.MAGENTA}{'=' * 50}{Colors.NC}")
    print_info("GitHub Copilot Chat用プロンプト自動生成システム")
    print()

    # 1. 前提条件チェック
    if not args.skip_checks:
        print_info("前提条件をチェック中...")
        
        # INPUT/task.md の存在確認
        if not Path("INPUT/task.md").exists():
            print_error("INPUT/task.md が見つかりません")
            print_info("以下のコマンドでファイルを作成してください：")
            print(f"{Colors.GRAY}  touch INPUT/task.md{Colors.NC}")
            print(f"{Colors.GRAY}  その後、task.mdにプロジェクト要件を記述してください{Colors.NC}")
            sys.exit(1)
        
        # スクリプトファイル存在確認
        script_extensions = ['.ps1', '.sh', '.py']
        required_scripts = ['code/modify_prompt_files', 'code/merge_copilot_instructions']
        
        found_scripts = {}
        for script_base in required_scripts:
            found = False
            for ext in script_extensions:
                script_path = f"{script_base}{ext}"
                if Path(script_path).exists():
                    found_scripts[script_base] = script_path
                    found = True
                    break
            
            if not found:
                print_error(f"必須スクリプトが見つかりません: {script_base}.*")
                sys.exit(1)
        
        print_success("前提条件チェック完了")
        print()

    # 2. タスク内容表示
    task_file = Path("INPUT/task.md")
    if task_file.exists():
        print_info("現在のタスク内容:")
        print(f"{Colors.GRAY}{'─' * 30}{Colors.NC}")
        with open(task_file, 'r', encoding='utf-8') as f:
            for line in f:
                print(f"  {line.rstrip()}")
        print(f"{Colors.GRAY}{'─' * 30}{Colors.NC}")
        print()

    # 3. GitHub Copilot Chat手順の表示
    print(f"{Colors.YELLOW}📋 GitHub Copilot Chat での実行手順{Colors.NC}")
    print(f"{Colors.YELLOW}{'=' * 40}{Colors.NC}")
    print()
    print_info("VSCodeでGitHub Copilot Chatを開き、以下のコマンドを順番に実行してください：")
    print()
    print(f"{Colors.CYAN}  1. /requirement_analyzer{Colors.NC}")
    print(f"{Colors.GRAY}     → 要件分析レポートを生成します{Colors.NC}")
    print()
    print(f"{Colors.CYAN}  2. /architect_designer{Colors.NC}")
    print(f"{Colors.GRAY}     → アーキテクチャ設計レポートを生成します{Colors.NC}")
    print()
    print(f"{Colors.CYAN}  3. /prompt_generator{Colors.NC}")
    print(f"{Colors.GRAY}     → エージェント用プロンプトを生成します{Colors.NC}")
    print(f"{Colors.YELLOW}     ※ 必要に応じて複数回実行してください{Colors.NC}")
    print()
    print(f"{Colors.CYAN}  4. /readme{Colors.NC}")
    print(f"{Colors.GRAY}     → プロジェクト用READMEを生成します{Colors.NC}")
    print()

    # 4. ユーザー確認待ち
    if not args.auto_confirm:
        print(f"{Colors.YELLOW}⏳ 確認{Colors.NC}")
        input("上記4つのコマンドをGitHub Copilot Chatで実行完了後、Enterキーを押してください: ")

    print()

    # 5. 生成ファイル確認
    print_info("生成ファイルを確認中...")

    expected_files = [
        "sample/requirement_analysis_report.md",
        "sample/architect_design_report.md", 
        "sample/README.md"
    ]

    missing_files = []
    for file_path in expected_files:
        if not check_file_exists(file_path):
            missing_files.append(file_path)

    # promptsフォルダのチェック
    prompts_dir = Path("sample/prompts")
    if prompts_dir.exists():
        prompt_files = list(prompts_dir.glob("*.md"))
        if prompt_files:
            print_success(f"✓ sample/prompts/ (ファイル数: {len(prompt_files)})")
        else:
            print_warning("✗ sample/prompts/ (プロンプトファイルが見つかりません)")
            missing_files.append("sample/prompts/*.md")
    else:
        print_warning("✗ sample/prompts/ (フォルダが見つかりません)")
        missing_files.append("sample/prompts/")

    if missing_files:
        print()
        print_error("一部のファイルが見つかりません。GitHub Copilot Chatでの実行を確認してください:")
        for file_path in missing_files:
            print(f"{Colors.RED}  - {file_path}{Colors.NC}")
        
        continue_choice = input("それでも続行しますか？ (y/N): ")
        if continue_choice.lower() not in ['y', 'yes']:
            print_info("処理を中断しました")
            sys.exit(1)

    print()

    # 6. 自動処理実行
    print(f"{Colors.YELLOW}🔄 ファイル変換処理を開始...{Colors.NC}")

    # スクリプト実行
    scripts_to_run = [
        ('code/modify_prompt_files', 'プロンプトファイルをGitHub Copilot Chat形式に変換'),
        ('code/merge_copilot_instructions', '設定ファイルをマージ')
    ]

    for script_base, description in scripts_to_run:
        print_info(f"{description}中...")
        
        # 利用可能なスクリプト形式を探す
        script_path = None
        for ext in ['.py', '.ps1', '.sh']:  # Python優先
            candidate = f"{script_base}{ext}"
            if Path(candidate).exists():
                script_path = candidate
                break
        
        if script_path:
            if run_script(script_path):
                print_success(f"{description}完了")
            else:
                print_warning(f"{description}で警告が発生しました")
        else:
            print_error(f"実行可能なスクリプトが見つかりません: {script_base}.*")

    print()

    # 7. 完了メッセージと次のステップ
    print(f"{Colors.GREEN}🎉 処理完了！{Colors.NC}")
    print(f"{Colors.GREEN}{'=' * 20}{Colors.NC}")

    github_dir = Path("sample/.github")
    if github_dir.exists():
        print_success("sample/.github/ フォルダが正常に生成されました")
        
        # 生成されたファイル一覧表示
        print_info("生成されたファイル:")
        for file_path in github_dir.rglob("*"):
            if file_path.is_file():
                print(f"  📄 {file_path}")
    else:
        print_warning("sample/.github/ フォルダが見つかりません")

    print()
    print(f"{Colors.CYAN}📋 次のステップ:{Colors.NC}")
    print("1. 新しいプロジェクトフォルダを作成")
    print("2. sample/.github/ フォルダを新プロジェクトにコピー")
    print("3. sample/README.md も必要に応じてコピー")
    print("4. VSCodeで新プロジェクトを開いてGitHub Copilot Chatを活用")

    print()
    print_info("使用例:")
    print(f"{Colors.GRAY}  mkdir my-new-project{Colors.NC}")
    print(f"{Colors.GRAY}  cp -r sample/.github my-new-project/{Colors.NC}")
    print(f"{Colors.GRAY}  cp sample/README.md my-new-project/{Colors.NC}")
    print(f"{Colors.GRAY}  cd my-new-project && code .{Colors.NC}")

    print()
    print_success("Meta Promptをご利用いただき、ありがとうございました！")

if __name__ == "__main__":
    main()
