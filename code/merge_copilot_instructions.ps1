#!/usr/bin/env pwsh
# -*- coding: utf-8 -*-
<#
.SYNOPSIS
    sample\copilot-instructions.mdの先頭にsample\variables.yamlの内容を追加して、
    sample\.github\copilot-instructions.mdファイルに出力するスクリプト

.DESCRIPTION
    このスクリプトは、variables.yamlの内容をcopilot-instructions.mdの先頭に追加して、
    .github\copilot-instructions.mdファイルに出力します。

.EXAMPLE
    .\merge_copilot_instructions.ps1
#>

# エラー時の動作を設定
$ErrorActionPreference = "Stop"

function Main {
    try {
        # ベースディレクトリを取得（スクリプトの親ディレクトリ）
        $ScriptPath = if ($MyInvocation.MyCommand.Path) {
            $MyInvocation.MyCommand.Path
        } else {
            $PSCommandPath
        }
        $ScriptDir = Split-Path -Parent $ScriptPath
        $BaseDir = Split-Path -Parent $ScriptDir
   
        # 入力ファイルのパス
        $variablesFile = Join-Path $BaseDir "sample\variables.yaml"
        $copilotInstructionsFile = Join-Path $BaseDir "sample\copilot-instructions.md"
        
        # 出力ディレクトリとファイルのパス
        $outputDir = Join-Path $BaseDir "sample\.github"
        $outputFile = Join-Path $outputDir "copilot-instructions.md"
        
        # 入力ファイルの存在チェック
        if (-not (Test-Path $variablesFile)) {
            Write-Error "エラー: $variablesFile が見つかりません。"
            exit 1
        }
        
        if (-not (Test-Path $copilotInstructionsFile)) {
            Write-Error "エラー: $copilotInstructionsFile が見つかりません。"
            exit 1
        }
        
        # 出力ディレクトリの作成（存在しない場合）
        if (-not (Test-Path $outputDir)) {
            Write-Host "ディレクトリを作成中: $outputDir"
            New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
        }
        
        # variables.yamlの内容を読み込み
        Write-Host "読み込み中: $variablesFile"
        $variablesContent = Get-Content -Path $variablesFile -Raw -Encoding UTF8
        
        # copilot-instructions.mdの内容を読み込み
        Write-Host "読み込み中: $copilotInstructionsFile"
        $copilotContent = Get-Content -Path $copilotInstructionsFile -Raw -Encoding UTF8
        
        # 結合したコンテンツを作成
        # variables.yamlの内容をコードブロックで囲む
        $mergedContent = @"

# Variables Configuration
``````yaml
$variablesContent``````

---

$copilotContent
"@
        
        # 出力ファイルに書き込み
        Write-Host "書き込み中: $outputFile"
        Set-Content -Path $outputFile -Value $mergedContent -Encoding UTF8
        
        Write-Host "✅ 正常に完了しました。" -ForegroundColor Green
        Write-Host "   出力ファイル: $outputFile" -ForegroundColor Green
        Write-Host "   variables.yaml の内容が copilot-instructions.md の先頭に追加されました。" -ForegroundColor Green
        
    }
    catch {
        if ($_.Exception -is [System.IO.FileNotFoundException]) {
            Write-Error "❌ ファイルが見つかりません: $($_.Exception.Message)"
        }
        elseif ($_.Exception -is [System.UnauthorizedAccessException]) {
            Write-Error "❌ ファイルアクセス権限エラー: $($_.Exception.Message)"
        }
        elseif ($_.Exception -is [System.Text.DecoderFallbackException]) {
            Write-Error "❌ 文字エンコーディングエラー: $($_.Exception.Message)"
            Write-Host "ファイルがUTF-8でエンコードされていることを確認してください。"
        }
        else {
            Write-Error "❌ 予期しないエラーが発生しました: $($_.Exception.Message)"
        }
        exit 1
    }
}

# スクリプトが直接実行された場合のみメイン関数を呼び出し
if ($MyInvocation.InvocationName -ne '.') {
    Main
}
