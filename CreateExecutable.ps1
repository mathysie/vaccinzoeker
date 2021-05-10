Push-Location $PSScriptRoot
Start-Process -FilePath "pyinstaller.exe" -ArgumentList "--onefile", ".\src\PageGetter.py", "--icon=$PSScriptRoot\src\Spuit.ico" -Wait
Copy-Item -Path ".\src\Spuit.ico" -Destination ".\dist\"
Pop-Location