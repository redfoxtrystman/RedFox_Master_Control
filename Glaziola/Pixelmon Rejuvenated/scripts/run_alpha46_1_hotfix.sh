#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
javac --add-exports java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED scripts/RepairMinecraftComponentLinks.java
java --add-exports java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED -cp scripts RepairMinecraftComponentLinks build/pack
python3 scripts/package_alpha46_1.py
