#!/usr/bin/env python3
"""
プロンプトファイルを修正するスクリプト

## 使用方法
```bash
# スクリプトを実行
python code/modify_prompt_files.py

# または実行権限を付与して直接実行
chmod +x code/modify_prompt_files.py
./code/modify_prompt_files.py
```

## 処理内容
このスクリプトは以下の処理を行います：
1. sample/prompts/ ディレクトリ内の *_prompt.md ファイルを検索
2. 各ファイルに対して、front matter（---\nmode: agent\n---）を先頭に追加
3. sample/.github/prompts/ ディレクトリに {agent_name}_prompt.prompt.md として保存
4. Github Copilot Chat等での利用に適した形式のプロンプトファイルを生成

## ファイル構造例
```
sample/
├── prompts/
│   ├── analyzer_prompt.md      # 入力ファイル
│   └── writer_prompt.md        # 入力ファイル
└── .github/
    └── prompts/
        ├── analyzer_prompt.prompt.md  # 出力ファイル（front matter付き）
        └── writer_prompt.prompt.md    # 出力ファイル（front matter付き）
```
"""

from pathlib import Path


def modify_prompt_files():
    """プロンプトファイルを修正してGithub Copilot Chat用の形式に変換する"""
    
    # ディレクトリパスを設定（スクリプトのあるディレクトリの親ディレクトリをベースとする）
    base_dir = Path(__file__).parent.parent
    prompts_dir = base_dir / "sample" / "prompts"
    github_dir = base_dir / "sample" / ".github" / "prompts"
    
    print(f"入力ディレクトリ: {prompts_dir}")
    print(f"出力ディレクトリ: {github_dir}")
    
    # 入力ディレクトリが存在しない場合は作成して終了
    if not prompts_dir.exists():
        print(f"⚠️  入力ディレクトリが存在しません: {prompts_dir}")
        prompts_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ ディレクトリを作成しました: {prompts_dir}")
        print("📝 *_prompt.md ファイルを配置してから再実行してください")
        return
    
    # 出力ディレクトリを準備
    github_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ 出力ディレクトリを準備: {github_dir}")
    
    # *_prompt.md パターンのファイルを検索
    prompt_files = list(prompts_dir.glob("*_prompt.md"))
    
    if not prompt_files:
        print("❌ *_prompt.md ファイルが見つかりません。")
        print(f"📁 {prompts_dir} に以下のような名前のファイルを配置してください:")
        print("   - analyzer_prompt.md")
        print("   - writer_prompt.md")
        print("   - etc...")
        return
    
    print(f"🔍 {len(prompt_files)}個のプロンプトファイルを発見しました。")
    
    # Github Copilot Chat用のfront matter（メタデータ）
    front_matter = """---
mode: agent
---

"""
    
    for prompt_file in prompt_files:
        try:
            # エージェント名をファイル名から抽出（例: analyzer_prompt.md → analyzer）
            agent_name = prompt_file.stem.replace("_prompt", "")
            print(f"\n🔄 処理中: {agent_name}")
            
            # 出力ファイル名を生成（例: analyzer_prompt.prompt.md）
            github_file = github_dir / f"{agent_name}_prompt.prompt.md"        
            
            # 元ファイルの内容を読み込み
            with open(prompt_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # front matterを先頭に追加してGithub Copilot Chat用の内容を作成
            new_content = front_matter + original_content
            
            # Github Copilot Chat用ファイルに書き込み
            with open(github_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"  ✅ 変換完了: {github_file.name}")
            
        except Exception as e:
            print(f"  ❌ エラーが発生しました: {e}")
            continue
    
    print("\n🎉 プロンプトファイルの変換が完了しました。")


def main():
    """メイン関数：スクリプトのエントリーポイント"""
    print("📝 プロンプトファイル変換スクリプトを開始します...")
    modify_prompt_files()
    print("🏁 スクリプトが完了しました。")


if __name__ == "__main__":
    main()
