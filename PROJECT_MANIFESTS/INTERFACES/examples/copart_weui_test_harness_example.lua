-- Minimal JOB-13 WEUI test harness pattern.
-- PREVIEW and TEST must be the default. LIVE requires explicit activation.

local M = {}
local im = ui_imgui
local windowOpen = im and im.BoolPtr(false) or nil
local modeIndex = im and im.IntPtr(0) or nil
local modes = {"PREVIEW", "TEST", "LIVE"}
local logLines = {}

local function addLog(text)
  table.insert(logLines, 1, os.date("%H:%M:%S") .. "  " .. tostring(text))
  while #logLines > 100 do table.remove(logLines) end
end

function M.openWindow()
  if windowOpen then windowOpen[0] = true end
  return true
end

function M.closeWindow()
  if windowOpen then windowOpen[0] = false end
  return true
end

local function currentMode()
  local index = math.max(0, math.min(#modes - 1, modeIndex and modeIndex[0] or 0))
  return modes[index + 1]
end

local function drawWindow()
  if not (im and windowOpen and windowOpen[0]) then return end
  im.SetNextWindowSizeConstraints(im.ImVec2(520, 420), im.ImVec2(1050, 920))
  local visible = im.Begin("RedFox Copart Auction — WEUI Test Harness###redfox_copart_test", windowOpen)
  if visible then
    im.TextUnformatted("TRANSACTION MODE")
    im.Combo1("Mode", modeIndex, modes)
    im.TextWrapped("PREVIEW: read only. TEST: persistent fake transactions. LIVE: real Career money/ownership with rollback.")
    if currentMode() == "LIVE" then
      im.TextColored(im.ImVec4(1, 0.35, 0.2, 1), "LIVE MODE — back up the Career save first")
    end
    im.Separator()

    if im.Button("Read JOB-09 Shop Candidates", im.ImVec2(-1, 34)) then
      local bridge = extensions and extensions.redfoxCopartAuction
      local response = bridge and bridge.readJob09Candidates and bridge.readJob09Candidates()
      addLog(response and response.message or "JOB-13 bridge is not loaded")
    end
    if im.Button("Create Test Listing", im.ImVec2(-1, 34)) then addLog("Create listing requested in " .. currentMode() .. " mode") end
    if im.Button("Simulate Reserve Not Met", im.ImVec2(-1, 34)) then addLog("Reserve-not-met test requested") end
    if im.Button("Simulate Seller Settlement", im.ImVec2(-1, 34)) then addLog("Seller settlement test requested") end
    if im.Button("Simulate Purchase Rollback", im.ImVec2(-1, 34)) then addLog("Purchase rollback test requested") end

    im.Separator()
    im.TextUnformatted("TEST LOG")
    if im.BeginChild1("copart_test_log", im.ImVec2(0, -45), true) then
      for _, line in ipairs(logLines) do im.TextWrapped(line) end
    end
    im.EndChild()
  end
  im.End()
end

function M.onUpdate()
  drawWindow()
end

return M
