using System.Security.Cryptography;

namespace PKVault.Core;

public record TradeSwapActionInput(string OutgoingVariantId, TradePokemonDTO Incoming);

public class TradeSwapAction(
    IPkmVariantLoader pkmVariantLoader,
    IBoxLoader boxLoader,
    IPkmFileLoader pkmFileLoader
) : DataAction<TradeSwapActionInput>
{
    protected override async Task<DataActionPayload> Execute(TradeSwapActionInput input, DataUpdateFlags flags)
    {
        var outgoing = await pkmVariantLoader.GetEntity(input.OutgoingVariantId)
            ?? throw new KeyNotFoundException($"Trade Pokemon not found: {input.OutgoingVariantId}");

        var targetBox = await boxLoader.GetDto(outgoing.BoxId)
            ?? throw new KeyNotFoundException($"Trade target box not found: {outgoing.BoxId}");

        var outgoingGroup = (await pkmVariantLoader.GetEntitiesByBox(outgoing.BoxId, outgoing.BoxSlot))
            .Values.ToList();

        if (outgoingGroup.Count == 0)
            throw new InvalidOperationException("Trade source slot is empty.");

        var main = outgoingGroup.FirstOrDefault(x => x.IsMain)
            ?? throw new InvalidOperationException("Trade source slot has no main Pokemon.");

        if (main.Id != input.OutgoingVariantId)
            throw new InvalidOperationException("Only the main PKVault variant can be traded.");

        foreach (var entity in outgoingGroup)
        {
            var dto = await pkmVariantLoader.CreateDTO(entity);
            if (!dto.CanDelete || dto.IsExternal)
                throw new InvalidOperationException($"Trade source cannot be removed: {dto.Id}");
        }

        var bytes = Convert.FromBase64String(input.Incoming.PayloadBase64);
        var fingerprint = Convert.ToHexString(SHA256.HashData(bytes));
        if (!fingerprint.Equals(input.Incoming.Fingerprint, StringComparison.OrdinalIgnoreCase))
            throw new InvalidOperationException("Incoming trade Pokemon fingerprint mismatch.");

        var extension = input.Incoming.Extension.TrimStart('.');
        if (string.IsNullOrWhiteSpace(extension))
            throw new InvalidOperationException("Incoming trade Pokemon has no format extension.");

        var tempFile = new PkmFileEntity
        {
            Filepath = $"trade-incoming.{extension}",
            Data = bytes,
            Error = null,
            Updated = false,
            Deleted = false,
        };

        var incomingPkm = pkmFileLoader.CreatePKM(tempFile, input.Incoming.Context);
        if (!incomingPkm.IsEnabled)
            throw new InvalidOperationException("Incoming trade Pokemon could not be loaded by PKVault.");

        foreach (var entity in outgoingGroup)
            await pkmVariantLoader.DeleteEntity(entity);

        var created = await pkmVariantLoader.AddEntity(new(
            Box: targetBox,
            BoxSlot: outgoing.BoxSlot,
            IsMain: true,
            IsExternal: false,
            AttachedSaveId: null,
            AttachedSavePkmIdBase: null,
            Context: input.Incoming.Context,
            Generation: input.Incoming.Generation,
            Pkm: incomingPkm,
            Id: Guid.NewGuid().ToString(),
            Updated: true,
            CheckPkm: true
        ));

        return new(
            type: DataActionType.MOVE_PKM,
            parameters: [
                incomingPkm.Nickname,
                null,
                null,
                $"Trade from {input.Incoming.PeerName}",
                outgoing.BoxSlot,
                false,
                incomingPkm.Species
            ]
        );
    }
}
