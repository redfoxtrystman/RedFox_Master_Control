@echo off
setlocal

rem Runs the existing SkyCraft Minecraft client against the Subnautica host mapping.
set "SKYCRAFT_LINK=Local\SkyCraft_Subnautica_v1"
set "SKYCRAFT_USERNAME=Ryley"

cd /d "%~dp0..\..\FalloutCraft\source\full_port\fabric"
call gradlew.bat runClient --no-configuration-cache

endlocal
