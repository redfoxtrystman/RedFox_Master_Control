param(
    [string]$GameDir = $env:SUBNAUTICA_DIR,
    [switch]$Launch
)

$ErrorActionPreference = "Stop"
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

function Resolve-SubnauticaDir([string]$Requested) {
    if (-not [string]::IsNullOrWhiteSpace($Requested)) {
        return (Resolve-Path $Requested).Path
    }

    $candidates = @(
        "C:\Program Files (x86)\Steam\steamapps\common\Subnautica",
        "C:\Program Files\Epic Games\Subnautica",
        "C:\XboxGames\Subnautica\Content"
    )

    foreach ($candidate in $candidates) {
        if (Test-Path (Join-Path $candidate "Subnautica_Data")) {
            return $candidate
        }
    }

    throw "Could not find Subnautica. Set SUBNAUTICA_DIR or pass -GameDir."
}

$GameDir = Resolve-SubnauticaDir $GameDir

Write-Host "== Minecraft <-> Subnautica / Vertical Slice 001 =="
Write-Host "Subnautica: $GameDir"

& (Join-Path $PSScriptRoot "build_subnautica.ps1") -GameDir $GameDir -Install
if ($LASTEXITCODE -ne 0) {
    throw "Subnautica bridge build/install failed."
}

$log = Join-Path $GameDir "BepInEx\LogOutput.log"
Write-Host ""
Write-Host "Bridge installed."
Write-Host "Expected proof log: $log"
Write-Host ""
Write-Host "Minecraft mapping: Local\SkyCraft_Subnautica_v1"
Write-Host "Takeover defaults OFF until coordinate/yaw calibration is confirmed."
Write-Host ""

if ($Launch) {
    $exe = Join-Path $GameDir "Subnautica.exe"
    if (-not (Test-Path $exe)) {
        throw "Subnautica.exe not found: $exe"
    }

    Start-Process $exe

    $launcher = Join-Path $PSScriptRoot "launch_minecraft_subnautica.bat"
    Start-Process "cmd.exe" -ArgumentList "/c", ('"' + $launcher + '"')

    Write-Host "Started Subnautica and the SkyCraft Minecraft client."
}

Write-Host ""
Write-Host "LIVE PROOF CHECKLIST"
Write-Host "  1. Load a Subnautica save and move into open ocean."
Write-Host "  2. Minecraft should open/create its SkyCraft mirror world automatically."
Write-Host "  3. In BepInEx LogOutput.log, confirm: BRIDGE PROOF: Minecraft connected"
Write-Host "  4. Enter the water deeply enough to swim."
Write-Host "  5. Confirm: BRIDGE PROOF: Minecraft swimming=True"
Write-Host "  6. Surface and confirm swimming returns False."
Write-Host "  7. For drowning proof, remain submerged and verify Minecraft death/air behavior."
Write-Host "  8. For mob proof, summon a zombie in the Minecraft mirror world below the Subnautica water surface."
Write-Host "     Do not use bridge-side conversion code: it must become drowned through Minecraft itself."
Write-Host ""
Write-Host "After the first launch, enable MinecraftTakeover only for coordinate/yaw calibration."
