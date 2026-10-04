param(
    [Parameter(Mandatory=$true)]
    [string]$GameDir,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$GameDir = (Resolve-Path $GameDir).Path
$exe = Join-Path $GameDir "Subnautica.exe"
if (-not (Test-Path $exe)) {
    throw "Subnautica.exe was not found in: $GameDir"
}

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$addon = Join-Path $here "MinecraftSubnautica.addon64"
$shader = Join-Path $here "reshade-shaders\Shaders\MinecraftSubnautica.fx"
$fxh = Join-Path $here "reshade-shaders\Shaders\ReShade.fxh"
foreach ($required in @($addon, $shader, $fxh)) {
    if (-not (Test-Path $required)) { throw "Package file is missing: $required" }
}

$dxgi = Join-Path $GameDir "dxgi.dll"
if (-not (Test-Path $dxgi)) {
    $url = "https://reshade.me/downloads/ReShade_Setup_6.8.0_Addon.exe"
    $setup = Join-Path $env:TEMP "ReShade_Setup_6.8.0_Addon.exe"
    Write-Host "ReShade add-on runtime is not installed in the Subnautica folder."
    Write-Host "Downloading the official ReShade 6.8.0 add-on installer pinned by Universal Modder..."
    Invoke-WebRequest $url -OutFile $setup
    Write-Host ""
    Write-Host "The official installer will open now."
    Write-Host "Select: $exe"
    Write-Host "Select: DirectX 10/11/12"
    Write-Host "Use the build WITH full add-on support."
    Start-Process -FilePath $setup -Wait
    if (-not (Test-Path $dxgi)) {
        throw "ReShade did not install dxgi.dll beside Subnautica.exe. Finish the ReShade install, then run this script again."
    }
}

$destAddon = Join-Path $GameDir "MinecraftSubnautica.addon64"
$shaderDir = Join-Path $GameDir "reshade-shaders\Shaders"
New-Item -ItemType Directory -Force $shaderDir | Out-Null

if ((Test-Path $destAddon) -and -not $Force) {
    Copy-Item $destAddon "$destAddon.pre-minecraftsubnautica.bak" -Force
}
$destShader = Join-Path $shaderDir "MinecraftSubnautica.fx"
if ((Test-Path $destShader) -and -not $Force) {
    Copy-Item $destShader "$destShader.pre-minecraftsubnautica.bak" -Force
}

Copy-Item $addon $destAddon -Force
Copy-Item $shader $destShader -Force
Copy-Item $fxh (Join-Path $shaderDir "ReShade.fxh") -Force

$preset = Join-Path $GameDir "MinecraftSubnauticaPreset.ini"
@"
Techniques=MinecraftSubnautica@MinecraftSubnautica.fx
TechniqueSorting=MinecraftSubnautica@MinecraftSubnautica.fx
"@ | Set-Content -Encoding ASCII $preset

$ini = Join-Path $GameDir "ReShade.ini"
if (-not (Test-Path $ini)) {
@"
[GENERAL]
EffectSearchPaths=.\reshade-shaders\Shaders\
TextureSearchPaths=.\reshade-shaders\Textures\
PresetPath=.\MinecraftSubnauticaPreset.ini

[OVERLAY]
TutorialProgress=4
ShowClock=0
ShowFPS=0
"@ | Set-Content -Encoding ASCII $ini
} else {
    Write-Host "Existing ReShade.ini left intact."
    Write-Host "Set the active preset to MinecraftSubnauticaPreset.ini if your existing preset is different."
}

Write-Host ""
Write-Host "Installed MinecraftSubnautica ReShade compositor."
Write-Host "Expected files:"
Write-Host "  $destAddon"
Write-Host "  $destShader"
Write-Host "  $preset"
