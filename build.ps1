$exclude = @("venv", "clima_Df8.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "clima_Df8.zip" -Force