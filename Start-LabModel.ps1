$ErrorActionPreference = 'Stop'
$AdapterUrl = 'http://127.0.0.1:11435/lab-config'
try {
    $Config = Invoke-RestMethod -Uri $AdapterUrl -TimeoutSec 2
    if ($Config.think -eq $false) { return }
} catch {}

$PythonPath = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
$AdapterPath = Join-Path $PSScriptRoot 'Ollama-NoThink.py'
Start-Process -FilePath $PythonPath -ArgumentList @($AdapterPath) -WorkingDirectory $PSScriptRoot -WindowStyle Hidden
for ($Attempt = 0; $Attempt -lt 20; $Attempt++) {
    Start-Sleep -Milliseconds 500
    try {
        $Config = Invoke-RestMethod -Uri $AdapterUrl -TimeoutSec 2
        if ($Config.think -eq $false) { return }
    } catch {}
}
throw 'Local Ollama adapter did not start. Check that port 11435 is available.'
