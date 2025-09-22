Param()

Write-Host "Initializing submodules..."
git submodule update --init --recursive

Write-Host "Current submodule status:"
git submodule status

Write-Host "Done."
