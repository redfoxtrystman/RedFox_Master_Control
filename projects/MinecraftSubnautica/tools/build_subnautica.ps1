param(
    [string]$GameDir = $env:SUBNAUTICA_DIR,
    [switch]$Install
)

$ErrorActionPreference = "Stop"
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Project = Join-Path $ProjectRoot "subnautica\MinecraftSubnautica.csproj"

dotnet build $Project -c Release
if ($LASTEXITCODE -ne 0) {
    throw "Bridge build failed."
}

$dll = Join-Path $ProjectRoot "subnautica\bin\Release\net472\MinecraftSubnautica.dll"
if (-not (Test-Path $dll)) {
    throw "Expected bridge DLL was not produced: $dll"
}

if (-not $Install) {
    Write-Host "Built against the official Subnautica.GameLibs/Nautilus packages:"
    Write-Host "  $dll"
    exit 0
}

if ([string]::IsNullOrWhiteSpace($GameDir)) {
    $candidates = @(
        "C:\Program Files (x86)\Steam\steamapps\common\Subnautica",
        "C:\Program Files\Epic Games\Subnautica",
        "C:\XboxGames\Subnautica\Content"
    )

    foreach ($candidate in $candidates) {
        if (Test-Path (Join-Path $candidate "Subnautica_Data")) {
            $GameDir = $candidate
            break
        }
    }
}

if ([string]::IsNullOrWhiteSpace($GameDir)) {
    throw "Build succeeded, but install needs the game path. Set SUBNAUTICA_DIR or pass -GameDir."
}

if (-not (Test-Path (Join-Path $GameDir "Subnautica_Data"))) {
    throw "That does not look like a Subnautica game directory: $GameDir"
}

$bepInEx = Join-Path $GameDir "BepInEx"
if (-not (Test-Path $bepInEx)) {
    throw "BepInEx is not installed under: $GameDir"
}

$nautilus = Join-Path $bepInEx "plugins\Nautilus"
if (-not (Test-Path $nautilus)) {
    Write-Warning "Nautilus was not found at the normal BepInEx\plugins\Nautilus path. The bridge declares Nautilus as a dependency."
}

$dest = Join-Path $bepInEx "plugins\MinecraftSubnautica"
New-Item -ItemType Directory -Force $dest | Out-Null
Copy-Item $dll (Join-Path $dest "MinecraftSubnautica.dll") -Force

Write-Host "Installed Minecraft Subnautica Bridge:"
Write-Host "  $dest"
