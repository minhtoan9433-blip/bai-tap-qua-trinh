$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$env:MPLCONFIGDIR = Join-Path $PSScriptRoot '.mpl-cache'
$python = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $python)) {
    Write-Host 'Chua co moi truong Python. Xem huong dan cai dat trong README.md.'
    exit 1
}
& $python -m streamlit run "Khoa học Màu sắc.py" --server.address 127.0.0.1 --server.port 8501
