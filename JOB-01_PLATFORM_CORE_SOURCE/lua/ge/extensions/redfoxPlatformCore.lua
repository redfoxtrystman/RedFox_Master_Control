-- RedFox FoxNet / IceFox shared phone + PC platform registry.
-- JOB-01 owns this file. It contains navigation and registration only.
-- Money, inventory, ownership, storage, insurance, rewards, purchases,
-- missions, and save mutations belong to RLS/JOB-02 and are prohibited here.

local M = {}

local CONTRACT_ID = "job01.platform.v1"
local registry = {}
local originComputerId = nil

local allowedFields = {
  id = true,
  owner = true,
  name = true,
  description = true,
  category = true,
  iconPath = true,
  entryPath = true,
  order = true,
  version = true,
  phone = true,
  pc = true,
  enabled = true,
  permissions = true,
  bridgeContract = true,
}

local function copyArray(value)
  local result = {}
  if type(value) ~= "table" then return result end
  for _, item in ipairs(value) do
    if type(item) == "string" then
      table.insert(result, item)
    end
  end
  return result
end

local function copyDestination(value)
  local result = {}
  for key in pairs(allowedFields) do
    local item = value[key]
    if key == "permissions" then
      result[key] = copyArray(item)
    elseif type(item) == "string" or type(item) == "number" or type(item) == "boolean" then
      result[key] = item
    end
  end
  return result
end

local function validId(value)
  return type(value) == "string"
    and #value >= 3
    and #value <= 80
    and value:match("^[a-z0-9][a-z0-9%._%-]+$") ~= nil
end

local function validEntryPath(value)
  if type(value) ~= "string" then return false end
  if value == "internal:redfox.home" then return true end
  if value:find("..", 1, true) then return false end
  return value:sub(1, 15) == "/ui/modModules/"
end

local function validateDestination(value)
  if type(value) ~= "table" then return false, "manifest must be a table" end
  if not validId(value.id) then return false, "invalid id" end
  if type(value.owner) ~= "string" or value.owner == "" then return false, "missing owner" end
  if type(value.name) ~= "string" or value.name == "" then return false, "missing name" end
  if not validEntryPath(value.entryPath) then return false, "invalid entryPath" end
  if value.bridgeContract and value.bridgeContract ~= "job02.bridge.v1" then
    return false, "unsupported bridgeContract"
  end
  return true
end

local function snapshot()
  local items = {}
  for _, value in pairs(registry) do
    table.insert(items, copyDestination(value))
  end
  table.sort(items, function(a, b)
    local aOrder = tonumber(a.order) or 9999
    local bOrder = tonumber(b.order) or 9999
    if aOrder == bOrder then return tostring(a.id) < tostring(b.id) end
    return aOrder < bOrder
  end)
  return {
    ok = true,
    contract = CONTRACT_ID,
    destinations = items,
  }
end

local function publishRegistry()
  if guihooks and guihooks.trigger then
    guihooks.trigger("RedFoxPlatformRegistryChanged", snapshot())
  end
end

function M.registerDestination(value)
  local ok, reason = validateDestination(value)
  if not ok then
    log("E", "redfoxPlatformCore", "Rejected destination: " .. tostring(reason))
    return {ok = false, error = reason}
  end

  local existing = registry[value.id]
  if existing and existing.owner ~= value.owner then
    local reasonText = "destination already owned by " .. tostring(existing.owner)
    log("E", "redfoxPlatformCore", "Rejected " .. value.id .. ": " .. reasonText)
    return {ok = false, error = reasonText}
  end

  local stored = copyDestination(value)
  stored.phone = value.phone ~= false
  stored.pc = value.pc ~= false
  stored.enabled = value.enabled ~= false
  stored.order = tonumber(value.order) or 9999
  stored.permissions = copyArray(value.permissions)
  registry[value.id] = stored
  publishRegistry()
  return {ok = true, id = value.id, contract = CONTRACT_ID}
end

function M.unregisterDestination(id, owner)
  local existing = registry[id]
  if not existing then return {ok = true, removed = false} end
  if existing.owner ~= owner then
    return {ok = false, error = "owner mismatch"}
  end
  registry[id] = nil
  publishRegistry()
  return {ok = true, removed = true}
end

function M.getRegistry()
  return snapshot()
end

function M.getContractId()
  return CONTRACT_ID
end

function M.openPcDesktop(computerId)
  originComputerId = computerId or originComputerId
  if not guihooks or not guihooks.trigger then return false end
  guihooks.trigger("ChangeState", {state = "redfox-icefox-desktop"})
  return true
end

function M.returnToComputer()
  if originComputerId
    and career_modules_computer
    and career_modules_computer.openComputerMenuById then
    career_modules_computer.openComputerMenuById(originComputerId)
    return true
  end
  if career_career and career_career.closeAllMenus then
    career_career.closeAllMenus()
    return true
  end
  return false
end

function M.closePlatform()
  if career_career and career_career.closeAllMenus then
    career_career.closeAllMenus()
    return true
  end
  return false
end

function M.onComputerAddFunctions(menuData, computerFunctions)
  if type(computerFunctions) ~= "table" or type(computerFunctions.general) ~= "table" then return end
  local computerId = menuData
    and menuData.computerFacility
    and menuData.computerFacility.id
    or nil
  computerFunctions.general["redfox-icefox"] = {
    id = "redfox-icefox",
    label = "IceFox / FoxNet",
    callback = function(callbackComputerId)
      M.openPcDesktop(callbackComputerId or computerId)
    end,
    order = 12,
  }
end

local function registerBuiltInDestination()
  M.registerDestination({
    id = "redfox.home",
    owner = "JOB-01",
    name = "IceFox Home",
    description = "Shared RedFox FoxNet front door.",
    category = "Platform",
    iconPath = "/ui/modModules/redfoxPlatformCore/assets/brand/icefox_head.svg",
    entryPath = "internal:redfox.home",
    order = 0,
    version = "0.2.0",
    phone = true,
    pc = true,
    enabled = true,
    permissions = {},
  })
end

function M.onExtensionLoaded()
  registerBuiltInDestination()
  extensions.hook("onRedFoxPlatformReady", CONTRACT_ID)
  log("I", "redfoxPlatformCore", "JOB-01 platform registry loaded: " .. CONTRACT_ID)
end

function M.onModActivated()
  registerBuiltInDestination()
  extensions.hook("onRedFoxPlatformReady", CONTRACT_ID)
end

return M
