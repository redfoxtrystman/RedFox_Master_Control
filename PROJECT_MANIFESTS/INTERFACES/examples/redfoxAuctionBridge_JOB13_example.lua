-- JOB-13 example adapter for redfox.auction.bridge.v1
-- Integration template only; not a stock-file override.

local M = {}
local contractVersion = "redfox.auction.bridge.v1"
local processedRequests = {}
local listings = {}

local function result(ok, code, message, data)
  return {ok = ok == true, code = code, message = message, data = data}
end

local function copy(value)
  if type(value) ~= "table" then return value end
  local out = {}
  for k, v in pairs(value) do out[k] = copy(v) end
  return out
end

function M.isAvailable()
  return true
end

function M.readJob09Candidates()
  local tow = extensions and extensions.redfoxTowRecoveryDispatch
  if type(tow) ~= "table" or type(tow.getWebPortalState) ~= "function" then
    return result(false, "JOB09_UNAVAILABLE", "JOB-09 is not loaded")
  end
  local ok, state = pcall(tow.getWebPortalState)
  if not ok or type(state) ~= "table" then
    return result(false, "JOB09_STATE_FAILED", "JOB-09 state could not be read")
  end
  return result(true, "OK", "JOB-09 shop inventory loaded", copy(state.shopInventory or {}))
end

function M.createListing(request)
  if type(request) ~= "table" or request.contractVersion ~= contractVersion then
    return result(false, "BAD_CONTRACT", "Expected " .. contractVersion)
  end
  local requestId = tostring(request.requestId or "")
  if requestId == "" then return result(false, "MISSING_REQUEST_ID", "requestId is required") end
  if processedRequests[requestId] then return copy(processedRequests[requestId]) end

  local listingId = "copart_" .. tostring(os.time()) .. "_" .. tostring(#listings + 1)
  local listing = {
    id = listingId,
    requestId = requestId,
    sourceSystem = request.sourceSystem,
    sourceType = request.sourceType,
    sellerType = request.sellerType,
    sourceRef = copy(request.sourceRef),
    vehicle = copy(request.vehicle),
    sale = copy(request.sale),
    transport = copy(request.transport),
    state = request.transport and request.transport.required and "transport_pending" or "active",
    createdAt = os.time(),
    highBid = tonumber(request.sale and request.sale.startingBid) or 0,
    bidderCount = 0
  }
  listings[listingId] = listing
  local response = result(true, "LISTING_CREATED", "Listing created", copy(listing))
  processedRequests[requestId] = copy(response)
  return response
end

function M.requestSellerSettlement(listingId)
  local listing = listings[tostring(listingId or "")]
  if not listing then return result(false, "NOT_FOUND", "Listing not found") end
  if listing.state == "sold" then return result(true, "ALREADY_SOLD", "Settlement already completed", copy(listing)) end

  listing.state = "settlement_requested"
  local tow = extensions and extensions.redfoxTowRecoveryDispatch
  if listing.sourceSystem == "JOB-09" and type(tow) == "table" and type(tow.settleExternalAuction) == "function" then
    local ok, response = pcall(
      tow.settleExternalAuction,
      listing.sourceRef and listing.sourceRef.shopId,
      listing.id,
      math.floor(tonumber(listing.highBid) or 0),
      listing.requestId .. ":settlement"
    )
    if ok and response then
      listing.state = "sold"
      listing.settledAt = os.time()
      return result(true, "SOLD", "Seller settlement completed", copy(listing))
    end
  end

  listing.state = "settlement_failed"
  return result(false, "SELLER_SETTLEMENT_FAILED", "Seller authority did not confirm vehicle removal/payment")
end

function M.getListing(listingId)
  local listing = listings[tostring(listingId or "")]
  return listing and copy(listing) or nil
end

return M
