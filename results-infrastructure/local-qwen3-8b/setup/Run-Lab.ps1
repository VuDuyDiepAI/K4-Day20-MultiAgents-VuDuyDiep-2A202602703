param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $LabArguments
)

# Run the existing lab CLI in Linux; Ollama runs on the Windows host.
& "$PSScriptRoot\Start-LabModel.ps1"
& docker exec -e OLLAMA_HOST=http://host.docker.internal:11435 lab-workflow-linux python @LabArguments
exit $LASTEXITCODE
