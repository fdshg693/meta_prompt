#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
変数読み込みモジュール

YAMLファイルから変数を読み込む機能を提供する。
PyYAMLモジュール使用版と手動パース版の両方を提供。
"""

import re
from pathlib import Path
from typing import Dict, Any, Union

# PyYAMLが利用可能かチェック
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


def parse_simple_yaml(content: str) -> Dict[str, Union[str, int, bool, float]]:
    """
    単純なYAMLファイル（Key: Value形式）を手動でパースする
    
    対応形式:
    - key: value
    - key: "quoted value"
    - key: 'quoted value'
    - key: 123 (整数)
    - key: 123.45 (浮動小数点)
    - key: true/false (ブール値)
    - # コメント行
    
    Args:
        content: YAMLファイルの内容
        
    Returns:
        変数辞書
    """
    variables = {}
    
    for line_num, line in enumerate(content.split('\n'), 1):
        # 空行やコメント行をスキップ
        original_line = line
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Key: Value形式の行を処理
        if ':' in line:
            try:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # インラインコメントを除去
                if '#' in value and not (value.startswith('"') or value.startswith("'")):
                    value = value.split('#')[0].strip()
                
                # 空の値の場合は空文字列として扱う
                if not value:
                    variables[key] = ""
                    continue
                
                # クォートを除去
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                    variables[key] = value  # クォートされた値は文字列として扱う
                    continue
                
                # 型変換を試行
                # ブール型（true/false、True/False）
                if value.lower() in ('true', 'false'):
                    variables[key] = value.lower() == 'true'
                # 整数型
                elif value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                    variables[key] = int(value)
                # 浮動小数点型
                elif '.' in value and value.replace('.', '', 1).replace('-', '', 1).isdigit():
                    variables[key] = float(value)
                # その他は文字列として扱う
                else:
                    variables[key] = value
                    
            except ValueError as e:
                print(f"警告: 行 {line_num} の解析に失敗しました: '{original_line}' - {e}")
                continue
    
    return variables


def load_variables_with_yaml(yaml_file_path: Path) -> Dict[str, Any]:
    """
    PyYAMLモジュールを使用してYAMLファイルから変数を読み込む
    
    Args:
        yaml_file_path: YAMLファイルのパス (Path オブジェクト)
        
    Returns:
        変数辞書
    """
    if not YAML_AVAILABLE:
        raise ImportError("PyYAMLモジュールがインストールされていません。pip install pyyamlでインストールしてください。")
    
    try:
        with yaml_file_path.open('r', encoding='utf-8') as file:
            variables = yaml.safe_load(file)
        
        # YAMLファイルがコメントのみの場合は空辞書を返す
        if variables is None:
            variables = {}
            
        print(f"変数ファイル読み込み完了: {len(variables)} 個の変数を読み込みました")
        return variables
    except FileNotFoundError:
        print(f"エラー: 変数ファイルが見つかりません: {yaml_file_path}")
        return {}
    except yaml.YAMLError as e:
        print(f"エラー: YAMLファイルの解析に失敗しました: {e}")
        return {}


def load_variables_without_yaml(yaml_file_path: Path) -> Dict[str, Any]:
    """
    手動パースでYAMLファイルから変数を読み込む（PyYAMLモジュール不使用版）
    
    Args:
        yaml_file_path: YAMLファイルのパス (Path オブジェクト)
        
    Returns:
        変数辞書
    """
    try:
        with yaml_file_path.open('r', encoding='utf-8') as file:
            content = file.read()
        
        variables = parse_simple_yaml(content)
            
        print(f"変数ファイル読み込み完了: {len(variables)} 個の変数を読み込みました")
        
        # デバッグ用：読み込んだ変数を表示
        if variables:
            print("読み込まれた変数:")
            for key, value in variables.items():
                print(f"  {key}: {value} ({type(value).__name__})")
        
        return variables
    except FileNotFoundError:
        print(f"エラー: 変数ファイルが見つかりません: {yaml_file_path}")
        return {}
    except Exception as e:
        print(f"エラー: ファイルの解析に失敗しました: {e}")
        return {}


def load_variables(yaml_file_path: Path, use_yaml_module: bool = True) -> Dict[str, Any]:
    """
    YAMLファイルから変数を読み込む（統一インターフェース）
    
    Args:
        yaml_file_path: YAMLファイルのパス (Path オブジェクト)
        use_yaml_module: PyYAMLモジュールを使用するかどうか（デフォルト: True）
        
    Returns:
        変数辞書
    """
    if use_yaml_module and YAML_AVAILABLE:
        return load_variables_with_yaml(yaml_file_path)
    else:
        if use_yaml_module and not YAML_AVAILABLE:
            print("警告: PyYAMLモジュールが利用できないため、手動パースを使用します")
        return load_variables_without_yaml(yaml_file_path)
