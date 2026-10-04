using HarmonyLib;

namespace MinecraftSubnautica.Bridge
{
    /// <summary>
    /// Observes successful player pickups after Subnautica has fully created/attached the item.
    /// Export only occurs after success, and SubnauticaItemBridge removes the local copy only after
    /// the cross-game ring accepts the transfer.
    /// </summary>
    [HarmonyPatch(typeof(Inventory))]
    internal static class SubnauticaPickupPatch
    {
        [HarmonyPostfix]
        [HarmonyPatch(nameof(Inventory.Pickup), typeof(Pickupable), typeof(bool))]
        private static void PickupPostfix(Pickupable pickupable, bool __result)
        {
            if (!__result || pickupable == null)
                return;

            SubnauticaItemBridge.Current?.TryExportPickup(pickupable);
        }
    }
}
