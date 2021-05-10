Push-Location $PSScriptRoot
If (Test-Path -Path ".\dist" -PathType Container) {
    Remove-Item -Path ".\dist" -Recurse
}
If (Test-Path -Path ".\build" -PathType Container) {
    Remove-Item -Path ".\build" -Recurse
}

Start-Process -FilePath "pyinstaller.exe" -ArgumentList "--onefile", ".\src\PageGetter.py", "--icon=$PSScriptRoot\src\Spuit.ico" -Wait
Copy-Item -Path ".\src\Spuit.ico" -Destination ".\dist\"
Pop-Location