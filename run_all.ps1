# Meta Prompt 統合実行スクリプト
# GitHub Copilot Chat用プロンプト自動生成システム

param(
    [switch]$SkipChecks,
    [switch]$AutoConfirm
)

# カラー出力用関数
function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Write-Success { param([string]$Message) Write-ColorOutput "✅ $Message" "Green" }
function Write-Info { param([string]$Message) Write-ColorOutput "📋 $Message" "Cyan" }
function Write-Warning { param([string]$Message) Write-ColorOutput "⚠️  $Message" "Yellow" }
function Write-Error { param([string]$Message) Write-ColorOutput "❌ $Message" "Red" }

# ヘッダー表示
Clear-Host
Write-ColorOutput "🚀 Meta Prompt 統合実行スクリプト" "Magenta"
Write-ColorOutput "=" * 50 "Magenta"
Write-Info "GitHub Copilot Chat用プロンプト自動生成システム"
Write-Host ""

# 1. 前提条件チェック
if (-not $SkipChecks) {
    Write-Info "前提条件をチェック中..."
    
    # INPUT/task.md の存在確認
    if (-not (Test-Path "INPUT/task.md")) {
        Write-Error "INPUT/task.md が見つかりません"
        Write-Info "以下のコマンドでファイルを作成してください："
        Write-Host "  New-Item -Path 'INPUT/task.md' -ItemType File -Force" -ForegroundColor Gray
        Write-Host "  その後、task.mdにプロジェクト要件を記述してください" -ForegroundColor Gray
        exit 1
    }
    
    # VSCode GitHub Copilot チェック（簡易）
    $vscodePath = Get-Command "code" -ErrorAction SilentlyContinue
    if (-not $vscodePath) {
        Write-Warning "VSCodeが見つかりません。手動でVSCodeを起動してください"
    }
    
    # スクリプトファイル存在確認
    $requiredScripts = @(
        "code/modify_prompt_files.ps1",
        "code/merge_copilot_instructions.ps1"
    )
    
    foreach ($script in $requiredScripts) {
        if (-not (Test-Path $script)) {
            Write-Error "必須スクリプトが見つかりません: $script"
            exit 1
        }
    }
    
    Write-Success "前提条件チェック完了"
    Write-Host ""
}

# 2. タスク内容表示
if (Test-Path "INPUT/task.md") {
    Write-Info "現在のタスク内容:"
    Write-Host "─" * 30 -ForegroundColor Gray
    Get-Content "INPUT/task.md" | ForEach-Object { Write-Host "  $_" -ForegroundColor White }
    Write-Host "─" * 30 -ForegroundColor Gray
    Write-Host ""
}

# 3. GitHub Copilot Chat手順の表示
Write-ColorOutput "📋 GitHub Copilot Chat での実行手順" "Yellow"
Write-ColorOutput "=" * 40 "Yellow"
Write-Host ""
Write-Info "VSCodeでGitHub Copilot Chatを開き、以下のコマンドを順番に実行してください："
Write-Host ""
Write-ColorOutput "  1. /requirement_analyzer" "Cyan"
Write-Host "     → 要件分析レポートを生成します" -ForegroundColor Gray
Write-Host ""
Write-ColorOutput "  2. /architect_designer" "Cyan"  
Write-Host "     → アーキテクチャ設計レポートを生成します" -ForegroundColor Gray
Write-Host ""
Write-ColorOutput "  3. /prompt_generator" "Cyan"
Write-Host "     → エージェント用プロンプトを生成します" -ForegroundColor Gray
Write-Host "     ※ 必要に応じて複数回実行してください" -ForegroundColor Yellow
Write-Host ""
Write-ColorOutput "  4. /readme" "Cyan"
Write-Host "     → プロジェクト用READMEを生成します" -ForegroundColor Gray
Write-Host ""

# 4. ユーザー確認待ち
if (-not $AutoConfirm) {
    Write-ColorOutput "⏳ 確認" "Yellow"
    Write-Host "上記4つのコマンドをGitHub Copilot Chatで実行完了後、Enterキーを押してください"
    Read-Host "準備ができたらEnterキーを押してください"
}

Write-Host ""

# 5. 生成ファイル確認
Write-Info "生成ファイルを確認中..."

$expectedFiles = @(
    "sample/requirement_analysis_report.md",
    "sample/architect_design_report.md", 
    "sample/README.md"
)

$missingFiles = @()
foreach ($file in $expectedFiles) {
    if (Test-Path $file) {
        Write-Success "✓ $file"
    } else {
        Write-Warning "✗ $file (見つかりません)"
        $missingFiles += $file
    }
}

# promptsフォルダのチェック
if (Test-Path "sample/prompts") {
    $promptFiles = Get-ChildItem "sample/prompts" -Filter "*.md"
    if ($promptFiles.Count -gt 0) {
        Write-Success "✓ sample/prompts/ (ファイル数: $($promptFiles.Count))"
    } else {
        Write-Warning "✗ sample/prompts/ (プロンプトファイルが見つかりません)"
        $missingFiles += "sample/prompts/*.md"
    }
} else {
    Write-Warning "✗ sample/prompts/ (フォルダが見つかりません)" 
    $missingFiles += "sample/prompts/"
}

if ($missingFiles.Count -gt 0) {
    Write-Host ""
    Write-Error "一部のファイルが見つかりません。GitHub Copilot Chatでの実行を確認してください:"
    foreach ($file in $missingFiles) {
        Write-Host "  - $file" -ForegroundColor Red
    }
    
    $continue = Read-Host "それでも続行しますか？ (y/N)"
    if ($continue -notmatch '^[yY]') {
        Write-Info "処理を中断しました"
        exit 1
    }
}

Write-Host ""

# 6. 自動処理実行
Write-ColorOutput "🔄 ファイル変換処理を開始..." "Yellow"

try {
    # プロンプトファイル変換
    Write-Info "プロンプトファイルをGitHub Copilot Chat形式に変換中..."
    & .\code\modify_prompt_files.ps1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "プロンプトファイル変換完了"
    } else {
        Write-Warning "プロンプトファイル変換で警告が発生しました"
    }
    
    # 設定ファイルマージ
    Write-Info "設定ファイルをマージ中..."
    & .\code\merge_copilot_instructions.ps1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "設定ファイルマージ完了"
    } else {
        Write-Warning "設定ファイルマージで警告が発生しました"
    }
    
} catch {
    Write-Error "処理中にエラーが発生しました: $($_.Exception.Message)"
    exit 1
}

Write-Host ""

# 7. 完了メッセージと次のステップ
Write-ColorOutput "🎉 処理完了！" "Green"
Write-ColorOutput "=" * 20 "Green"

if (Test-Path "sample/.github") {
    Write-Success "sample/.github/ フォルダが正常に生成されました"
    
    # 生成されたファイル一覧表示
    Write-Info "生成されたファイル:"
    Get-ChildItem "sample/.github" -Recurse -File | ForEach-Object {
        Write-Host "  📄 $($_.FullName.Replace((Get-Location).Path + '\', ''))" -ForegroundColor White
    }
} else {
    Write-Warning "sample/.github/ フォルダが見つかりません"
}

Write-Host ""
Write-ColorOutput "📋 次のステップ:" "Cyan"
Write-Host "1. 新しいプロジェクトフォルダを作成"
Write-Host "2. sample/.github/ フォルダを新プロジェクトにコピー"
Write-Host "3. sample/README.md も必要に応じてコピー"
Write-Host "4. VSCodeで新プロジェクトを開いてGitHub Copilot Chatを活用"

Write-Host ""
Write-Info "使用例:"
Write-Host "  mkdir my-new-project" -ForegroundColor Gray
Write-Host "  cp -r sample/.github my-new-project/" -ForegroundColor Gray
Write-Host "  cp sample/README.md my-new-project/" -ForegroundColor Gray
Write-Host "  cd my-new-project && code ." -ForegroundColor Gray

Write-Host ""
Write-Success "Meta Promptをご利用いただき、ありがとうございました！"
