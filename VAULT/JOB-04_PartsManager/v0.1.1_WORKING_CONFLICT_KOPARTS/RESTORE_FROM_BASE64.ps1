$src = "JOB04_PartsManager_v0.1.1_UI_BOOT_FIX.zip.base64"
$dst = "JOB04_PartsManager_v0.1.1_UI_BOOT_FIX.zip"
[IO.File]::WriteAllBytes($dst, [Convert]::FromBase64String((Get-Content $src -Raw)))
Write-Host "Restored $dst"
Write-Host "Expected SHA-256: e10cd85b6f05646bef4b1939263337038bb06d44692fbe49d06a196c822f876a"
