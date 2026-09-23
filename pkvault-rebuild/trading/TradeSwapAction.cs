using System.Security.Cryptography;
using PKHeX.Core;

namespace PKVault.Core;

public record TradeSwapActionInput(string[] OutgoingVariantIds, TradePokemonDTO[] Incoming);

public class TradeSwapAction(
    IServiceProvider sp,
    IPkmVariantLoader pkmVariantLoader,
    IBoxLoader boxLoader,
    IPkmFileLoader pkmFileLoader
) : DataAction<TradeSwapActionInput>
{
    private record SlotTarget(BoxDTO Box, int Slot);

    protected override async Task<DataActionPayload> Execute(TradeSwapActionInput input, DataUpdateFlags flags)
    {
        if (input.OutgoingVariantIds.Length > 6 || input.Incoming.Length > 6)
            throw new ArgumentException("A PKVault trade can contain at most 6 Pokemon per side.");
        if (input.OutgoingVariantIds.Length == 0 && input.Incoming.Length == 0)
            throw new ArgumentException("A trade cannot be empty.");
        if (input.OutgoingVariantIds.Distinct().Count() != input.OutgoingVariantIds.Length)
            throw new ArgumentException("The same Pokemon cannot be offered twice.");

        // Validate and materialize all incoming Pokemon before touching storage.
        var incomingPkms = new List<(TradePokemonDTO Offer, ImmutablePKM Pkm)>();
        foreach (var incoming in input.Incoming)
        {
            var bytes = Convert.FromBase64String(incoming.PayloadBase64);
            var fingerprint = Convert.ToHexString(SHA256.HashData(bytes));
            if (!fingerprint.Equals(incoming.Fingerprint, StringComparison.OrdinalIgnoreCase))
                throw new InvalidOperationException("Incoming trade Pokemon fingerprint mismatch.");

            var extension = incoming.Extension.TrimStart('.');
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

            var pkm = pkmFileLoader.CreatePKM(tempFile, incoming.Context);
            if (!pkm.IsEnabled)
                throw new InvalidOperationException("Incoming trade Pokemon could not be loaded by PKVault.");

            incomingPkms.Add((incoming, pkm));
        }

        // Resolve each logical outgoing Pokemon. All variants occupying its slot
        // leave together so an alternate generation copy cannot be left behind.
        var outgoingSlots = new List<(PkmVariantEntity Main, BoxDTO Box, List<PkmVariantEntity> Group)>();
        var logicalSlotKeys = new HashSet<string>();

        foreach (var id in input.OutgoingVariantIds)
        {
            var outgoing = await pkmVariantLoader.GetEntity(id)
                ?? throw new KeyNotFoundException($"Trade Pokemon not found: {id}");
            var dto = await pkmVariantLoader.CreateDTO(outgoing);

            if (!dto.IsMain)
                throw new InvalidOperationException("Only the main PKVault variant can be traded.");
            if (!dto.IsEnabled || !dto.CanDelete || dto.IsExternal)
                throw new InvalidOperationException($"Trade source cannot be removed: {dto.Id}");

            var slotKey = $"{outgoing.BoxId}:{outgoing.BoxSlot}";
            if (!logicalSlotKeys.Add(slotKey))
                throw new InvalidOperationException("Two offered variants point to the same PKVault slot.");

            var box = await boxLoader.GetDto(outgoing.BoxId)
                ?? throw new KeyNotFoundException($"Trade source box not found: {outgoing.BoxId}");

            var group = (await pkmVariantLoader.GetEntitiesByBox(outgoing.BoxId, outgoing.BoxSlot))
                .Values.ToList();

            foreach (var entity in group)
            {
                var related = await pkmVariantLoader.CreateDTO(entity);
                if (!related.CanDelete || related.IsExternal)
                    throw new InvalidOperationException($"Trade source has a protected/external variant: {related.Id}");
            }

            outgoingSlots.Add((outgoing, box, group));
        }

        // Reuse the offered slots first. If this side is receiving more Pokemon
        // than it sends, place the extras in the first empty normal PKVault slots.
        var targets = new List<SlotTarget>();
        foreach (var outgoing in outgoingSlots.Take(incomingPkms.Count))
            targets.Add(new(outgoing.Box, outgoing.Main.BoxSlot));

        if (targets.Count < incomingPkms.Count)
        {
            var allBoxes = (await boxLoader.GetAllDtos())
                .Where(b => b.Type == BoxType.Box)
                .OrderBy(b => b.BankId)
                .ThenBy(b => b.Order)
                .ThenBy(b => b.IdInt)
                .ToArray();

            var occupied = (await pkmVariantLoader.GetAllEntities())
                .Values
                .Select(e => $"{e.BoxId}:{e.BoxSlot}")
                .ToHashSet();

            // Offered slots are about to be removed and therefore count as free.
            foreach (var outgoing in outgoingSlots)
                occupied.Remove($"{outgoing.Main.BoxId}:{outgoing.Main.BoxSlot}");

            foreach (var target in targets)
                occupied.Add($"{target.Box.Id}:{target.Slot}");

            foreach (var box in allBoxes)
            {
                for (var slot = 0; slot < box.SlotCount && targets.Count < incomingPkms.Count; slot++)
                {
                    var key = $"{box.Id}:{slot}";
                    if (!occupied.Add(key))
                        continue;
                    targets.Add(new(box, slot));
                }
                if (targets.Count == incomingPkms.Count)
                    break;
            }

            if (targets.Count != incomingPkms.Count)
                throw new InvalidOperationException("There are not enough empty PKVault box slots to receive this trade.");
        }

        foreach (var outgoing in outgoingSlots)
            foreach (var entity in outgoing.Group)
                await pkmVariantLoader.DeleteEntity(entity);

        for (var i = 0; i < incomingPkms.Count; i++)
        {
            var (offer, pkm) = incomingPkms[i];
            var target = targets[i];

            await pkmVariantLoader.AddEntity(new(
                Box: target.Box,
                BoxSlot: target.Slot,
                IsMain: true,
                IsExternal: false,
                AttachedSaveId: null,
                AttachedSavePkmIdBase: null,
                Context: offer.Context,
                Generation: offer.Generation,
                Pkm: pkm,
                Id: Guid.NewGuid().ToString(),
                Updated: true,
                CheckPkm: true
            ));

            // Receiving a Pokemon through PKVault trading counts as obtaining it.
            // Use PKVault's native persistent dex record so trading it away later
            // never removes the caught/seen history. Eggs and glitch species 0
            // deliberately do not create official Pokedex entries.
            if (!pkm.IsEgg && pkm.Species > 0 && pkm.Species < (ushort)Species.MAX_COUNT)
            {
                await new DexMainService(sp).EnablePKM(pkm);
                flags.Dex.Ids.Add(pkm.Species.ToString());
            }
        }

        var firstIncoming = incomingPkms.FirstOrDefault();
        return new(
            type: DataActionType.MOVE_PKM,
            parameters: [
                firstIncoming.Pkm?.Nickname ?? "Trade",
                null,
                null,
                $"PKVault trade ({input.OutgoingVariantIds.Length} sent / {input.Incoming.Length} received)",
                targets.FirstOrDefault()?.Slot ?? -1,
                false,
                firstIncoming.Pkm?.Species ?? 0
            ]
        );
    }
}
