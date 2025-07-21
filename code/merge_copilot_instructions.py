#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sample\copilot-instructions.mdの先頭にsample\variables.yamlの内容を追加して、
sample\.github\copilot-instructions.mdファイルに出力するスクリプト
"""

import sys
from pathlib import Path


def main():
    """メイン処理"""
    # スクリプトのあるディレクトリを基準にパスを設定
    script_dir = Path(__file__).parent.parent
    
    # 入力ファイルのパス
    variables_file = script_dir / "sample" / "variables.yaml"
    copilot_instructions_file = script_dir / "sample" / "copilot-instructions.md"
    
    # 出力ディレクトリとファイルのパス
    output_dir = script_dir / "sample" / ".github"
    output_file = output_dir / "copilot-instructions.md"
    
    try:
        # 入力ファイルの存在チェック
        if not variables_file.exists():
            print(f"エラー: {variables_file} が見つかりません。")
            sys.exit(1)
            
        if not copilot_instructions_file.exists():
            print(f"エラー: {copilot_instructions_file} が見つかりません。")
            sys.exit(1)
        
        # 出力ディレクトリの作成（存在しない場合）
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # variables.yamlの内容を読み込み
        print(f"読み込み中: {variables_file}")
        with open(variables_file, 'r', encoding='utf-8') as f:
            variables_content = f.read()
        
        # copilot-instructions.mdの内容を読み込み
        print(f"読み込み中: {copilot_instructions_file}")
        with open(copilot_instructions_file, 'r', encoding='utf-8') as f:
            copilot_content = f.read()
        
        # 結合したコンテンツを作成
        # variables.yamlの内容をコードブロックで囲む
        merged_content = f"""

# Variables Configuration
```yaml
{variables_content}```

---

{copilot_content}
"""
        
        # 出力ファイルに書き込み
        print(f"書き込み中: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(merged_content)
        
        print(f"✅ 正常に完了しました。")
        print(f"   出力ファイル: {output_file}")
        print(f"   variables.yaml の内容が copilot-instructions.md の先頭に追加されました。")
        
    except FileNotFoundError as e:
        print(f"❌ ファイルが見つかりません: {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"❌ ファイルアクセス権限エラー: {e}")
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"❌ 文字エンコーディングエラー: {e}")
        print("ファイルがUTF-8でエンコードされていることを確認してください。")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 予期しないエラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
