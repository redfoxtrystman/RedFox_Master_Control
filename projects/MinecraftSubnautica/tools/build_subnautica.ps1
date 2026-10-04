param(
    [string]$GameDir = $env:SUBNAUTICA_DIR,
    [switch]$Install
)

$ErrorActionPreference = "Stop"
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Project = Join-Path $ProjectRoot "subnautica\MinecraftSubnautica.csproj"

if ([string]::IsNullOrWhiteSpace($GameDir)) {
    $steamDefault = "C:\Program Files (x86)\Steam\steamapps\common\Subnautica"
    if (Test-Path $steamDefault) {
        $GameDir = $steamDefault
    } else {
        throw "Set SUBNAUTICA_DIR or pass -GameDir with your Subnautica folder."
    }
}

$assembly = Join-Path $GameDir "Subnautica_Data\Managed\Assembly-CSharp.dll"
if (-not (Test-Path $assembly)) {
    throw "Subnautica managed assemblies not found under: $GameDir"
}

dotnet build $Project -c Release "/p:SubnauticaDir=$GameDir"
if ($LASTEXITCODE -ne 0) {
    throw "Bridge build failed."
}

$dll = Join-Path $ProjectRoot "subnautica\bin\Release\net472\MinecraftSubnautica.dll"

if ($Install) {
    $dest = Join-Path $GameDir "BepInEx\plugins\MinecraftSubnautica"
    New-Item -ItemType Directory -Force $dest | Out-Null
    Copy-Item $dll (Join-Path $dest "MinecraftSubnautica.dll") -Force
    Write-Host "Installed to $dest"
} else {
    Write-Host "Built: $dll"
}
