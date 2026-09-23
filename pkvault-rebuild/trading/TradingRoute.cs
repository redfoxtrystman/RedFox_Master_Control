namespace PKVault.Core.trading.routes;

[Route("api/[controller]")]
public class TradingController(TradingService tradingService)
{
    [HttpGet("state")]
    public Task<TradeStateDTO> GetState() => tradingService.GetStateAsync();

    [HttpPost("host")]
    public Task<TradeStateDTO> Host(TradeHostPayload payload) => tradingService.HostAsync(payload.LocalTest);

    [HttpPost("connect")]
    public Task<TradeStateDTO> Connect(TradeConnectPayload payload) => tradingService.ConnectAsync(payload.Address);

    [HttpPut("offer")]
    public Task<TradeStateDTO> SetOffer(TradeOfferPayload payload) => tradingService.SetOfferAsync(payload.PkmVariantId);

    [HttpPut("ready")]
    public Task<TradeStateDTO> SetReady(TradeReadyPayload payload) => tradingService.SetReadyAsync(payload.Ready);

    [HttpDelete("session")]
    public Task<TradeStateDTO> Disconnect() => tradingService.DisconnectAsync();
}
