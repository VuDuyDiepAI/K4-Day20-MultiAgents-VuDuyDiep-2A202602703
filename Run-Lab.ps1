param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $LabArguments
)

# Run the existing lab CLI in Linux; Ollama runs on the Windows host.
& docker exec -e OLLAMA_HOST=http://host.docker.internal:11434 lab-workflow-linux python @LabArguments
exit $LASTEXITCODE
