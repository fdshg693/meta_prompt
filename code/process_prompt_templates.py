#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
プロンプトテンプレート処理スクリプト

【実行方法】
cd c:\CodeStudy\meta_prompt

# デフォルトタスクを実行
python code\process_prompt_templates.py

# 特定のタスクを実行
python code\process_prompt_templates.py [タスク名]

# 全タスクを実行
python code\process_prompt_templates.py --all

# タスク一覧表示
python code\process_prompt_templates.py --list

# ヘルプ表示
python code\process_prompt_templates.py --help

【必要環境】
- Python 3.7以上（標準モジュールのみ使用）

【機能】
config/paths.jsonで定義された複数のタスクを実行可能。
各タスクで指定されたディレクトリ配下のMDファイルや個別ファイルペアの{{変数}}を
変数ファイルで定義されている値に置き換えて出力先に出力する

【タスクタイプ】
1. directory: ディレクトリ内の全MDファイルを一括処理
2. file_pairs: 個別のファイルペアを個別に処理
3. mixed: ディレクトリ処理とファイルペア処理の両方を実行

【ファイル構成】
- 設定: code/config/paths.json (タスク定義とファイルパス設定)
- 入力: 各タスクで指定されたテンプレートディレクトリ/*.md または個別ファイル
- 変数: 各タスクで指定された変数ファイル
- 出力: 各タスクで指定された出力ディレクトリ/*.md または個別ファイル

【タスク設定例】
{
  "tasks": [
    {
      "name": "dir_task",
      "type": "directory",
      "description": "ディレクトリ一括処理",
      "variables_file": "sample/variables.yaml",
      "input_dir": "sample/prompts",
      "output_dir": "sample/output"
    },
    {
      "name": "pair_task",
      "type": "file_pairs",
      "description": "ファイルペア処理",
      "variables_file": "sample/variables.yaml",
      "file_pairs": [
        {
          "input_file": "sample/prompts/template1.md",
          "output_file": "sample/output/result1.md"
        }
      ]
    },
    {
      "name": "mixed_task",
      "type": "mixed",
      "description": "混在処理",
      "variables_file": "sample/variables.yaml",
      "input_dir": "sample/prompts",
      "output_dir": "sample/output",
      "file_pairs": [
        {
          "input_file": "sample/special/template.md",
          "output_file": "sample/special_output/result.md"
        }
      ]
    }
  ],
  "default_task": "dir_task"
}
"""

import re
import sys
from pathlib import Path
from typing import Dict, Any
from variable_loader import load_variables
from config_loader import load_config_with_fallback, get_task_config, list_available_tasks


def process_file_pairs(file_pairs: list, variables: Dict[str, Any], project_root: Path) -> int:
    """
    ファイルペアリストを処理する
    
    Args:
        file_pairs: ファイルペアのリスト
        variables: 変数辞書
        project_root: プロジェクトルートディレクトリ
        
    Returns:
        成功したファイル数
    """
    success_count = 0
    
    for i, pair in enumerate(file_pairs):
        input_file_rel = pair.get("input_file", "")
        output_file_rel = pair.get("output_file", "")
        
        if not input_file_rel or not output_file_rel:
            print(f"警告: ファイルペア {i+1} でファイルパスが不正です")
            continue
            
        input_file_path = project_root / input_file_rel
        output_file_path = project_root / output_file_rel
        
        print(f"ファイルペア {i+1}: {input_file_rel} → {output_file_rel}")
        
        if process_markdown_file(input_file_path, output_file_path, variables):
            success_count += 1
    
    return success_count


def process_directory_files(input_dir: Path, output_dir: Path, variables: Dict[str, Any]) -> int:
    """
    ディレクトリ内のMDファイルを処理する
    
    Args:
        input_dir: 入力ディレクトリ
        output_dir: 出力ディレクトリ
        variables: 変数辞書
        
    Returns:
        成功したファイル数
    """
    # MDファイルを検索
    md_files = list(input_dir.glob("*.md"))
    if not md_files:
        print(f"警告: 入力ディレクトリにMDファイルが見つかりません: {input_dir}")
        return 0
    
    print(f"ディレクトリ処理対象ファイル: {len(md_files)} 個")
    
    success_count = 0
    for md_file in md_files:
        output_file_path = output_dir / md_file.name
        
        if process_markdown_file(md_file, output_file_path, variables):
            success_count += 1
    
    return success_count


def process_task(config: Dict[str, Any], task_name: str = None) -> bool:
    """
    指定されたタスクを実行する
    
    Args:
        config: 全体設定
        task_name: タスク名（Noneの場合はデフォルトタスク）
        
    Returns:
        実行成功の場合True
    """
    # タスク設定を取得
    task_config = get_task_config(config, task_name)
    if task_config is None:
        return False
    
    # プロジェクトルートディレクトリを基準とする
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # 基本設定を取得
    variables_file = project_root / task_config.get("variables_file", "sample/variables.yaml")
    task_type = task_config.get("type", "directory")

    print(f"タスク実行: {task_config.get('name', 'unknown')}")
    print(f"説明: {task_config.get('description', '')}")
    print(f"タイプ: {task_type}")
    print(f"変数ファイル: {variables_file}")
    
    # タスクタイプに応じてパス情報を表示
    if task_type in ["directory", "mixed"]:
        input_dir = project_root / task_config.get("input_dir", "sample/prompts")
        output_dir = project_root / task_config.get("output_dir", "sample/processed/.github/prompts")
        print(f"入力ディレクトリ: {input_dir}")
        print(f"出力ディレクトリ: {output_dir}")
    
    if task_type in ["file_pairs", "mixed"]:
        file_pairs = task_config.get("file_pairs", [])
        print(f"ファイルペア数: {len(file_pairs)}")
    
    print("-" * 50)
    
    # 変数ファイルの読み込み（標準モジュールのみ使用）
    variables = load_variables(variables_file, use_yaml_module=False)
    if not variables:
        print("変数が読み込めなかったため、処理を中止します。")
        return False
    
    total_files = 0
    success_count = 0
    
    # タスクタイプに応じて処理を実行
    if task_type == "directory":
        # ディレクトリ処理のみ
        input_dir = project_root / task_config.get("input_dir")
        output_dir = project_root / task_config.get("output_dir")
        
        if not input_dir.exists():
            print(f"エラー: 入力ディレクトリが存在しません: {input_dir}")
            return False
        
        md_files = list(input_dir.glob("*.md"))
        total_files = len(md_files)
        success_count = process_directory_files(input_dir, output_dir, variables)
        
    elif task_type == "file_pairs":
        # ファイルペア処理のみ
        file_pairs = task_config.get("file_pairs", [])
        total_files = len(file_pairs)
        success_count = process_file_pairs(file_pairs, variables, project_root)
        
    elif task_type == "mixed":
        # ディレクトリ処理とファイルペア処理の混在
        input_dir = project_root / task_config.get("input_dir")
        output_dir = project_root / task_config.get("output_dir")
        file_pairs = task_config.get("file_pairs", [])
        
        # ディレクトリ処理
        if input_dir.exists():
            md_files = list(input_dir.glob("*.md"))
            dir_total = len(md_files)
            dir_success = process_directory_files(input_dir, output_dir, variables)
            
            print(f"ディレクトリ処理結果: {dir_success}/{dir_total}")
        else:
            print(f"警告: 入力ディレクトリが存在しません: {input_dir}")
            dir_total = 0
            dir_success = 0
        
        # ファイルペア処理
        pair_total = len(file_pairs)
        if pair_total > 0:
            print()
            print("ファイルペア処理:")
            pair_success = process_file_pairs(file_pairs, variables, project_root)
            print(f"ファイルペア処理結果: {pair_success}/{pair_total}")
        else:
            pair_success = 0
        
        total_files = dir_total + pair_total
        success_count = dir_success + pair_success
    
    else:
        print(f"エラー: 不明なタスクタイプです: {task_type}")
        return False
    
    print()
    print("-" * 50)
    print(f"タスク '{task_config.get('name')}' 処理完了: {success_count}/{total_files} ファイルの処理に成功しました")
    
    if success_count == total_files and total_files > 0:
        print("✅ すべてのファイルが正常に処理されました")
        return True
    else:
        if total_files == 0:
            print("⚠️  処理対象ファイルがありませんでした")
        else:
            print(f"⚠️  {total_files - success_count} ファイルの処理に失敗しました")
        return False


def replace_variables_in_text(text: str, variables: Dict[str, Any]) -> str:
    """
    テキスト内の{{変数}}を実際の値に置き換える
    
    Args:
        text: 置き換え対象のテキスト
        variables: 変数辞書
        
    Returns:
        置き換え後のテキスト
    """
    # {{変数名}}のパターンを検索
    pattern = r'\{\{(\w+)\}\}'
    
    def replace_func(match):
        var_name = match.group(1)
        if var_name in variables:
            return str(variables[var_name])
        else:
            warning_message = f"変数 '{var_name}' が見つかりません。そのまま残します。"
            print(f"警告: {warning_message}")
            
            return match.group(0)  # 元の{{変数名}}を返す
    
    return re.sub(pattern, replace_func, text)


def process_markdown_file(input_file_path: Path, output_file_path: Path, variables: Dict[str, Any]) -> bool:
    """
    MDファイルを処理して変数を置き換え、出力ファイルに保存する
    
    Args:
        input_file_path: 入力ファイルのパス (Path オブジェクト)
        output_file_path: 出力ファイルのパス (Path オブジェクト)
        variables: 変数辞書
        
    Returns:
        処理成功の場合True、失敗の場合False
    """
    try:
        # 入力ファイルを読み込み
        content = input_file_path.read_text(encoding='utf-8')
        
        # 変数置き換え
        processed_content = replace_variables_in_text(content, variables)
        
        # 出力ディレクトリを作成（存在しない場合）
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 出力ファイルに書き込み
        output_file_path.write_text(processed_content, encoding='utf-8')
        
        print(f"処理完了: {input_file_path.name} → {output_file_path.name}")
        return True
        
    except FileNotFoundError:
        print(f"エラー: 入力ファイルが見つかりません: {input_file_path}")
        return False
    except Exception as e:
        print(f"エラー: ファイル処理中にエラーが発生しました: {e}")
        return False


def main():
    """
    メイン処理
    """
    # スクリプトファイルのディレクトリを基準とした相対パス
    script_dir = Path(__file__).parent
    
    # 設定ファイルの読み込み
    config_file = script_dir / "config" / "paths.json"
    config = load_config_with_fallback(config_file)
    if not config:
        print("設定が読み込めなかったため、処理を中止します。")
        return

    print("プロンプトテンプレート処理スクリプト開始")
    print(f"設定ファイル: {config_file}")
    print()
    
    # コマンドライン引数の処理
    args = sys.argv[1:]
    
    if len(args) == 0:
        # 引数なしの場合はデフォルトタスクを実行
        print("デフォルトタスクを実行します")
        default_task = config.get("default_task")
        
        if default_task is None:
            print("エラー: デフォルトタスクが設定されていません")
            return
        
        # デフォルトタスクが配列の場合は複数タスクを順次実行
        if isinstance(default_task, list):
            print(f"複数のデフォルトタスクを実行します: {default_task}")
            success_count = 0
            for task_name in default_task:
                print(f"{'='*60}")
                if process_task(config, task_name):
                    success_count += 1
                print()
            
            print(f"{'='*60}")
            print(f"デフォルトタスク実行結果: {success_count}/{len(default_task)} タスクが成功しました")
            
            if success_count == len(default_task):
                print("✅ すべてのデフォルトタスクが正常に完了しました")
            else:
                print(f"⚠️  {len(default_task) - success_count} タスクが失敗しました")
        else:
            # 単一のデフォルトタスクを実行
            process_task(config, default_task)
    elif args[0] == "--list" or args[0] == "-l":
        # タスク一覧表示
        list_available_tasks(config)
    elif args[0] == "--all" or args[0] == "-a":
        # 全タスク実行
        print("全タスクを実行します")
        print()
        tasks = config.get("tasks", [])
        success_count = 0
        for task in tasks:
            task_name = task.get("name")
            if task_name:
                print(f"{'='*60}")
                if process_task(config, task_name):
                    success_count += 1
                print()
        
        print(f"{'='*60}")
        print(f"全体結果: {success_count}/{len(tasks)} タスクが成功しました")
        
        if success_count == len(tasks):
            print("✅ すべてのタスクが正常に完了しました")
        else:
            print(f"⚠️  {len(tasks) - success_count} タスクが失敗しました")
    elif args[0] == "--help" or args[0] == "-h":
        # ヘルプ表示
        print("使用方法:")
        print("  python code\\process_prompt_templates.py [オプション] [タスク名]")
        print()
        print("オプション:")
        print("  -h, --help     このヘルプを表示")
        print("  -l, --list     利用可能なタスク一覧を表示")
        print("  -a, --all      すべてのタスクを実行")
        print()
        print("タスク名を指定しない場合はデフォルトタスクが実行されます")
        print()
        list_available_tasks(config)
    else:
        # 指定されたタスクを実行
        task_name = args[0]
        print(f"指定されたタスクを実行します: {task_name}")
        if not process_task(config, task_name):
            sys.exit(1)


if __name__ == "__main__":
    main()
