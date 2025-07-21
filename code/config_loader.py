#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設定ファイル読み込みモジュール

JSONファイルから設定を読み込む機能を提供する。
標準モジュールのみ使用。
"""

import json
from pathlib import Path
from typing import Dict, Any


def load_config(config_file_path: Path) -> Dict[str, Any]:
    """
    設定ファイル（JSON）からタスク設定を読み込む
    
    Args:
        config_file_path: 設定ファイルのパス
        
    Returns:
        設定辞書
    """
    try:
        with config_file_path.open('r', encoding='utf-8') as file:
            config = json.load(file)
        print(f"設定ファイル読み込み完了: {config_file_path}")
        return config
    except FileNotFoundError:
        print(f"エラー: 設定ファイルが見つかりません: {config_file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"エラー: 設定ファイルの解析に失敗しました: {e}")
        return {}
    except Exception as e:
        print(f"エラー: 設定ファイル読み込み中にエラーが発生しました: {e}")
        return {}


def get_task_config(config: Dict[str, Any], task_name: str = None):
    """
    指定されたタスク名の設定を取得する
    
    Args:
        config: 全体設定
        task_name: タスク名（Noneの場合はデフォルトタスク）
        
    Returns:
        タスク設定辞書（見つからない場合はNone）
    """
    if "tasks" not in config:
        print("エラー: 設定ファイルにtasksが定義されていません")
        return None
    
    tasks = config["tasks"]
    
    # タスク名が指定されていない場合はデフォルトタスクを使用
    if task_name is None:
        task_name = config.get("default_task")
        if task_name is None:
            print("エラー: デフォルトタスクが設定されていません")
            return None
    
    # 指定されたタスクを検索
    for task in tasks:
        if task.get("name") == task_name:
            return task
    
    print(f"エラー: タスク '{task_name}' が見つかりません")
    return None


def list_available_tasks(config: Dict[str, Any]) -> None:
    """
    利用可能なタスク一覧を表示する
    
    Args:
        config: 全体設定
    """
    if "tasks" not in config:
        print("利用可能なタスクがありません")
        return
    
    tasks = config["tasks"]
    default_task = config.get("default_task", "")
    
    # デフォルトタスクが配列の場合の処理
    default_task_names = []
    if isinstance(default_task, list):
        default_task_names = default_task
    elif default_task:
        default_task_names = [default_task]
    
    print("利用可能なタスク:")
    for task in tasks:
        name = task.get("name", "")
        description = task.get("description", "")
        task_type = task.get("type", "directory")
        marker = " (デフォルト)" if name in default_task_names else ""
        
        print(f"  - {name}: {description} [タイプ: {task_type}]{marker}")
        
        # ファイルペアの詳細表示
        if task_type in ["file_pairs", "mixed"] and "file_pairs" in task:
            file_pairs = task["file_pairs"]
            if file_pairs:
                print(f"    ファイルペア数: {len(file_pairs)}")
                for i, pair in enumerate(file_pairs):
                    input_file = pair.get("input_file", "")
                    output_file = pair.get("output_file", "")
                    print(f"      {i+1}. {input_file} → {output_file}")
        
        # ディレクトリ処理の詳細表示
        if task_type in ["directory", "mixed"]:
            input_dir = task.get("input_dir", "")
            output_dir = task.get("output_dir", "")
            if input_dir and output_dir:
                print(f"    ディレクトリ: {input_dir} → {output_dir}")


def validate_task_config(task_config: Dict[str, str]) -> bool:
    """
    タスク設定の妥当性をチェックする
    
    Args:
        task_config: タスク設定辞書
        
    Returns:
        妥当性チェック結果
    """
    # 基本フィールドのチェック
    required_fields = ["name", "variables_file"]
    
    for field in required_fields:
        if field not in task_config:
            print(f"エラー: タスク設定に必須フィールド '{field}' がありません")
            return False
        
        if not task_config[field]:
            print(f"エラー: タスク設定のフィールド '{field}' が空です")
            return False
    
    # タスクタイプに応じたバリデーション
    task_type = task_config.get("type", "directory")
    
    if task_type == "directory":
        # ディレクトリ処理タイプ
        dir_fields = ["input_dir", "output_dir"]
        for field in dir_fields:
            if field not in task_config or not task_config[field]:
                print(f"エラー: ディレクトリタイプのタスクには '{field}' が必要です")
                return False
                
    elif task_type == "file_pairs":
        # ファイルペア処理タイプ
        if "file_pairs" not in task_config:
            print("エラー: ファイルペアタイプのタスクには 'file_pairs' が必要です")
            return False
            
        file_pairs = task_config["file_pairs"]
        if not isinstance(file_pairs, list) or len(file_pairs) == 0:
            print("エラー: 'file_pairs' は空でないリストである必要があります")
            return False
            
        for i, pair in enumerate(file_pairs):
            if not isinstance(pair, dict):
                print(f"エラー: file_pairs[{i}] は辞書である必要があります")
                return False
                
            pair_fields = ["input_file", "output_file"]
            for field in pair_fields:
                if field not in pair or not pair[field]:
                    print(f"エラー: file_pairs[{i}] に '{field}' が必要です")
                    return False
                    
    elif task_type == "mixed":
        # 混在処理タイプ
        dir_fields = ["input_dir", "output_dir"]
        for field in dir_fields:
            if field not in task_config or not task_config[field]:
                print(f"エラー: 混在タイプのタスクには '{field}' が必要です")
                return False
        
        # file_pairsは任意
        if "file_pairs" in task_config:
            file_pairs = task_config["file_pairs"]
            if not isinstance(file_pairs, list):
                print("エラー: 'file_pairs' はリストである必要があります")
                return False
                
            for i, pair in enumerate(file_pairs):
                if not isinstance(pair, dict):
                    print(f"エラー: file_pairs[{i}] は辞書である必要があります")
                    return False
                    
                pair_fields = ["input_file", "output_file"]
                for field in pair_fields:
                    if field not in pair or not pair[field]:
                        print(f"エラー: file_pairs[{i}] に '{field}' が必要です")
                        return False
    else:
        print(f"エラー: 不明なタスクタイプです: {task_type}")
        return False
    
    return True


def get_default_config() -> Dict[str, Any]:
    """
    デフォルトの設定を取得する
    
    Returns:
        デフォルト設定辞書
    """
    return {
        "tasks": [
            {
                "name": "default",
                "description": "デフォルトタスク",
                "variables_file": "sample/variables.yaml",
                "input_dir": "sample/prompts",
                "output_dir": "sample/processed/.github/prompts"
            }
        ],
        "default_task": "default"
    }


def create_default_config_file(config_file_path: Path) -> bool:
    """
    デフォルトの設定ファイルを作成する
    
    Args:
        config_file_path: 作成する設定ファイルのパス
        
    Returns:
        作成成功の場合True
    """
    try:
        # 親ディレクトリを作成
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # デフォルト設定を書き込み
        default_config = get_default_config()
        with config_file_path.open('w', encoding='utf-8') as file:
            json.dump(default_config, file, ensure_ascii=False, indent=2)
        
        print(f"デフォルト設定ファイルを作成しました: {config_file_path}")
        return True
        
    except Exception as e:
        print(f"エラー: デフォルト設定ファイルの作成に失敗しました: {e}")
        return False


def load_config_with_fallback(config_file_path: Path) -> Dict[str, Any]:
    """
    設定ファイルを読み込み、存在しない場合はデフォルト設定ファイルを作成する
    
    Args:
        config_file_path: 設定ファイルのパス
        
    Returns:
        設定辞書
    """
    if config_file_path.exists():
        return load_config(config_file_path)
    else:
        print(f"設定ファイルが存在しないため、デフォルト設定を作成します: {config_file_path}")
        if create_default_config_file(config_file_path):
            return load_config(config_file_path)
        else:
            print("デフォルト設定の作成に失敗したため、メモリ上のデフォルト設定を使用します")
            return get_default_config()
