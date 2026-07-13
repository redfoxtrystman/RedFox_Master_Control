-- JOB-01 RedFox IceFox Platform Core loader.
-- Loads one ordinary GE extension. It does not register a Career module and
-- does not replace any RLS Career authority file.

if extensions and extensions.load and not extensions.redfoxPlatformCore then
  local ok, err = pcall(extensions.load, "redfoxPlatformCore")
  if not ok then
    log("E", "redfoxPlatformCore", "Unable to load JOB-01 platform extension: " .. tostring(err))
  end
end

if setExtensionUnloadMode then
  pcall(setExtensionUnloadMode, "redfoxPlatformCore", "manual")
end
