Param()

Write-Host "Submodule summary:" -ForegroundColor Cyan
git config -f .gitmodules --get-regexp path | ForEach-Object {
    $tokens = $_ -split " "
    if ($tokens.Length -ge 2) {
        $name = $tokens[0] -replace "submodule\." -replace "\.path"
        $path = $tokens[1]
        Write-Host ("- {0}: {1}" -f $name, $path)
    }
}
