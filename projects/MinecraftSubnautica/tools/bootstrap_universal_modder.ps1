param(
    [string]$Target = ""
)

$ErrorActionPreference = "Stop"

$Repo = "https://github.com/rehan-remade/universal-modder.git"
$Commit = "8607693be42ce02442251f05e0495f58c2b77e5d"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if ([string]::IsNullOrWhiteSpace($Target)) {
    $Target = Join-Path $ProjectRoot ".tools\universal-modder"
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "git is required."
}

if (-not (Test-Path $Target)) {
    New-Item -ItemType Directory -Force -Path (Split-Path $Target -Parent) | Out-Null
    git clone $Repo $Target
}

Push-Location $Target
try {
    git remote set-url origin $Repo
    git fetch origin
    git checkout --detach $Commit

    $Actual = (git rev-parse HEAD).Trim()
    if ($Actual -ne $Commit) {
        throw "Universal Modder checkout mismatch. Expected $Commit, got $Actual."
    }

    if (Get-Command uv -ErrorAction SilentlyContinue) {
        uv tool install --force .
    }
    elseif (Get-Command python -ErrorAction SilentlyContinue) {
        python -m pip install -e .
    }
    else {
        throw "Install uv or Python so the Universal Modder CLI can be installed."
    }

    Write-Host "Universal Modder ready at $Target"
    Write-Host "Pinned commit: $Commit"
}
finally {
    Pop-Location
}
