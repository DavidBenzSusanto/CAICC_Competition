param(
    [string]$Label = "opencode_evidence",
    [int]$DelaySeconds = 3
)

# Enable Per-Monitor / System DPI Awareness so 125%/150% Windows scaling doesn't crop the screenshot
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class DpiHelper {
    [DllImport("user32.dll")]
    public static extern bool SetProcessDPIAware();
}
"@
[DpiHelper]::SetProcessDPIAware() | Out-Null

Add-Type -AssemblyName System.Windows.Forms, System.Drawing

$outDir = Join-Path $PSScriptRoot "screenshots_for_submission"
if (-not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Force -Path $outDir | Out-Null
}

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  CAICC 2026 Screenshot Helper" -ForegroundColor Cyan
Write-Host "  Switch to your OpenCode window now!" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

for ($i = $DelaySeconds; $i -gt 0; $i--) {
    Write-Host "  Capturing in $i..." -ForegroundColor Yellow
    Start-Sleep -Seconds 1
}

$bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bmp = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bmp)
$graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$fileName = "${timestamp}_${Label}.png"
$filePath = Join-Path $outDir $fileName

$bmp.Save($filePath, [System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose()
$bmp.Dispose()

Write-Host ""
Write-Host "[SUCCESS] Saved full-resolution screenshot ($($bounds.Width)x$($bounds.Height)) to:" -ForegroundColor Green
Write-Host "  $filePath" -ForegroundColor White
Write-Host ""
