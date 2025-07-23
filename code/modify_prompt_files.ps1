# プロンプトファイルを修正するPowerShellスクリプト
#
# 使用方法:
#   # PowerShellで実行
#   .\code\modify_prompt_files.ps1
#   
#   # または絶対パスで
#   PowerShell -ExecutionPolicy Bypass -File ".\code\modify_prompt_files.ps1"
#
# このスクリプトは以下の処理を行います：
# sample/prompts/{agent_name}_prompt.md を元にする。
# sample/.github/prompts/{agent_name}_prompt.prompt.md に本番環境で利用するための完成ファイルを作成する

# エラーが発生したら終了
$ErrorActionPreference = "Stop"

# ベースディレクトリを取得（スクリプトの親ディレクトリ）
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BaseDir = Split-Path -Parent $ScriptDir
$PromptsDir = Join-Path $BaseDir "sample\prompts"
$GitHubDir = Join-Path $BaseDir "sample\.github\prompts"

Write-Host "プロンプトディレクトリを確認中: $PromptsDir"
Write-Host "GitHub用出力ディレクトリ: $GitHubDir"

# プロンプトディレクトリが存在しない場合は作成
if (-not (Test-Path $PromptsDir)) {
    Write-Host "ディレクトリが存在しません: $PromptsDir"
    New-Item -ItemType Directory -Path $PromptsDir -Force | Out-Null
    Write-Host "ディレクトリを作成しました: $PromptsDir"
    exit 0
}

# GitHub用出力ディレクトリが存在しない場合は作成
if (-not (Test-Path $GitHubDir)) {
    New-Item -ItemType Directory -Path $GitHubDir -Force | Out-Null
}
Write-Host "GitHub用出力ディレクトリを準備: $GitHubDir"

# *_prompt.mdファイルを検索
$PromptFiles = Get-ChildItem -Path $PromptsDir -Name "*_prompt.md" -File

# ファイルが存在しない場合の処理
if ($PromptFiles.Count -eq 0) {
    Write-Host "*_prompt.mdファイルが見つかりません。"
    exit 0
}

Write-Host "$($PromptFiles.Count)個のプロンプトファイルを発見しました。"

# front matterの内容
$FrontMatter = @"
---
mode: agent
---


"@

# 各プロンプトファイルを処理
foreach ($promptFile in $PromptFiles) {
    $fullPath = Join-Path $PromptsDir $promptFile
    if (Test-Path $fullPath) {
        # ファイル名を取得
        $agentName = $promptFile -replace "_prompt\.md$", ""
        Write-Host ""
        Write-Host "処理中: $agentName"
        
        # 1. 本番環境用ファイルのパスを作成
        $githubFile = Join-Path $GitHubDir "${agentName}_prompt.prompt.md"
        
        # 2. 元ファイルの内容を読み込み、front matterの重複をチェック
        $originalContent = Get-Content -Path $fullPath -Raw -Encoding UTF8
        
        if ($originalContent.TrimStart().StartsWith("---`nmode: agent`n---")) {
            Write-Host "  front matterが既に存在するため、そのまま使用します"
            $newContent = $originalContent
        } else {
            # front matterを追加して本番環境用ファイルを作成
            $newContent = $FrontMatter + $originalContent
        }
        
        # UTF8 (BOM無し) で保存
        [System.IO.File]::WriteAllText($githubFile, $newContent, [System.Text.UTF8Encoding]::new($false))
        
        Write-Host "  本番環境用ファイルを作成: $(Split-Path -Leaf $githubFile)"
    }
}

Write-Host ""
Write-Host "プロンプトファイルの修正が完了しました。"
