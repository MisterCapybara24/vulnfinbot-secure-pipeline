$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
if (-not (Test-Path '.venv/Scripts/python.exe')) { py -3.12 -m venv .venv }
& .venv/Scripts/python.exe -m pip install -r requirements-dev.txt
$env:AI_BACKEND = 'ollama'
$env:OLLAMA_MODEL = 'phi3:latest'
Write-Host 'Open http://127.0.0.1:5000 . Stop: Ctrl+C'
& .venv/Scripts/python.exe run.py
