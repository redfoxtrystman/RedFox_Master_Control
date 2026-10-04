using System;
using System.Collections;
using System.Collections.Generic;
using BepInEx.Logging;
using UnityEngine;
using UWE;

namespace MinecraftSubnautica.Bridge
{
    /// <summary>
    /// Live Subnautica inventory adapter for cross-game item transfers.
    ///
    /// Slice 001 intentionally enables only Seaglide until duplication protection and state restore
    /// are proven in-game. The transport itself is generic and ready for additional TechTypes.
    /// </summary>
    public sealed class SubnauticaItemBridge : IDisposable
    {
        private readonly ManualLogSource _log;
        private readonly CrossGameItemChannel _channel;
        private readonly Dictionary<ulong, CrossGameItem> _latestState = new Dictionary<ulong, CrossGameItem>();

        private ulong _nextTransferId = (ulong)DateTime.UtcNow.Ticks;
        private bool _disposed;
        private int _suppressPickupExport;

        public static SubnauticaItemBridge Current { get; private set; }

        public SubnauticaItemBridge(ManualLogSource log)
        {
            _log = log ?? throw new ArgumentNullException(nameof(log));
            _channel = new CrossGameItemChannel();
            Current = this;
            _log.LogInfo($"Cross-game item channel created: {CrossGameItemProtocol.DefaultMappingName}");
        }

        public void Tick()
        {
            if (_disposed)
                return;

            _channel.PulseHostHeartbeat();

            int processed = 0;
            while (processed++ < 32 && _channel.TryReceiveFromMinecraft(out CrossGameItem item))
            {
                _latestState[item.TransferId] = item;

                if (item.Operation == CrossGameItemOp.Transfer)
                {
                    CoroutineHost.StartCoroutine(RestoreToSubnautica(item));
                }
                else
                {
                    _log.LogInfo(
                        $"ITEM BRIDGE: state {item.Operation} id={item.TransferId} item={item.ItemId} " +
                        $"energy={item.Energy:F2}/{item.MaxEnergy:F2}");
                }
            }
        }

        /// <summary>
        /// Called by the Inventory.Pickup Harmony postfix after Subnautica has successfully added
        /// an item to the player's inventory. Returns true only when the item was transferred and
        /// removed locally, so a failed/full bridge never eats the player's item.
        /// </summary>
        public bool TryExportPickup(Pickupable pickupable)
        {
            if (_disposed || _suppressPickupExport != 0 || pickupable == null)
                return false;

            if (!_channel.MinecraftHeartbeatIsFresh())
                return false;

            TechType techType = pickupable.GetTechType();

            // First functional item proof. Add more TechTypes only after this path is live-proven.
            if (techType != TechType.Seaglide)
                return false;

            CrossGameItem item = BuildTransfer(pickupable, techType);
            if (!_channel.TrySendToMinecraft(item))
            {
                _log.LogWarning($"ITEM BRIDGE: queue full; keeping {techType} in Subnautica inventory.");
                return false;
            }

            bool removed = Inventory.main != null
                && Inventory.main.container != null
                && Inventory.main.container.RemoveItem(pickupable, true);

            if (!removed)
            {
                _log.LogError(
                    $"ITEM BRIDGE: queued {techType} transfer {item.TransferId} but could not remove it from " +
                    "Subnautica inventory. Sending compensating remove to Minecraft.");

                item.Operation = CrossGameItemOp.Remove;
                _channel.TrySendToMinecraft(item);
                return false;
            }

            _latestState[item.TransferId] = item;
            UnityEngine.Object.Destroy(pickupable.gameObject);

            _log.LogInfo(
                $"ITEM BRIDGE PROOF: exported {techType} transfer={item.TransferId} " +
                $"energy={item.Energy:F2}/{item.MaxEnergy:F2}");
            return true;
        }

        private CrossGameItem BuildTransfer(Pickupable pickupable, TechType techType)
        {
            var item = new CrossGameItem
            {
                TransferId = ++_nextTransferId,
                Operation = CrossGameItemOp.Transfer,
                Origin = CrossGameOrigin.Subnautica,
                Flags = CrossGameItemFlags.Tool,
                Count = 1,
                MaxStack = 1,
                ItemId = "subnautica:" + techType,
                DisplayName = Language.main != null ? Language.main.Get(techType) : techType.ToString()
            };

            EnergyMixin energy = pickupable.GetComponent<EnergyMixin>();
            if (energy != null)
            {
                item.Flags |= CrossGameItemFlags.HasEnergy;
                item.Energy = energy.charge;
                item.MaxEnergy = energy.capacity;

                string batteryTechType = "None";
                try
                {
                    InventoryItem stored = energy.batterySlot != null ? energy.batterySlot.storedItem : null;
                    if (stored != null && stored.item != null)
                        batteryTechType = stored.item.GetTechType().ToString();
                }
                catch (Exception ex)
                {
                    _log.LogDebug($"Could not read installed battery TechType: {ex.Message}");
                }

                item.StateJson =
                    "{\"techType\":\"" + EscapeJson(techType.ToString()) + "\"," +
                    "\"batteryTechType\":\"" + EscapeJson(batteryTechType) + "\"," +
                    "\"charge\":" + item.Energy.ToString(System.Globalization.CultureInfo.InvariantCulture) + "," +
                    "\"capacity\":" + item.MaxEnergy.ToString(System.Globalization.CultureInfo.InvariantCulture) + "}";
            }
            else
            {
                item.StateJson = "{\"techType\":\"" + EscapeJson(techType.ToString()) + "\"}";
            }

            return item;
        }

        private IEnumerator RestoreToSubnautica(CrossGameItem item)
        {
            TechType techType;
            if (!TryResolveTechType(item.ItemId, out techType))
            {
                _log.LogWarning($"ITEM BRIDGE: cannot restore unsupported item id {item.ItemId}");
                yield break;
            }

            var result = new TaskResult<GameObject>();
            yield return CraftData.InstantiateFromPrefabAsync(techType, result, false);

            GameObject gameObject = result.Get();
            if (gameObject == null)
            {
                _log.LogError($"ITEM BRIDGE: prefab spawn failed for {techType}");
                yield break;
            }

            Pickupable pickupable = gameObject.GetComponent<Pickupable>();
            if (pickupable == null)
            {
                UnityEngine.Object.Destroy(gameObject);
                _log.LogError($"ITEM BRIDGE: prefab {techType} had no Pickupable.");
                yield break;
            }

            ApplyMutableState(gameObject, item);

            bool pickedUp = false;
            try
            {
                _suppressPickupExport++;
                pickedUp = Inventory.main != null && Inventory.main.Pickup(pickupable, false);
            }
            finally
            {
                _suppressPickupExport--;
            }

            if (!pickedUp)
            {
                // Don't delete the player's item if inventory is full. Leave it safely in-world
                // just in front of the player instead.
                if (Player.main != null)
                {
                    Transform t = Player.main.transform;
                    gameObject.transform.position = t.position + t.forward * 1.5f;
                }
                gameObject.SetActive(true);
                _log.LogWarning($"ITEM BRIDGE: inventory full; returned {techType} was dropped in front of player.");
                yield break;
            }

            _log.LogInfo(
                $"ITEM BRIDGE PROOF: restored {techType} transfer={item.TransferId} " +
                $"energy={item.Energy:F2}/{item.MaxEnergy:F2}");
        }

        private static void ApplyMutableState(GameObject gameObject, CrossGameItem item)
        {
            EnergyMixin energy = gameObject.GetComponent<EnergyMixin>();
            if (energy == null || (item.Flags & CrossGameItemFlags.HasEnergy) == 0)
                return;

            // EnergyMixin.charge is read-only in the current game libraries; the installed
            // battery is the mutable source of truth.
            IBattery battery = energy.battery;
            if (battery == null)
                return;

            if (item.MaxEnergy > 0.0f && battery.capacity > 0.0f)
            {
                float normalized = Mathf.Clamp01(item.Energy / item.MaxEnergy);
                battery.charge = normalized * battery.capacity;
            }
            else
            {
                battery.charge = Mathf.Clamp(item.Energy, 0.0f, battery.capacity);
            }
        }

        private static bool TryResolveTechType(string itemId, out TechType techType)
        {
            // Explicit mapping is deliberate for the proof slice. It prevents arbitrary protocol
            // strings from becoming game object spawns.
            if (string.Equals(itemId, "subnautica:Seaglide", StringComparison.OrdinalIgnoreCase))
            {
                techType = TechType.Seaglide;
                return true;
            }

            techType = TechType.None;
            return false;
        }

        private static string EscapeJson(string value)
        {
            return (value ?? string.Empty)
                .Replace("\\", "\\\\")
                .Replace("\"", "\\\"");
        }

        public void Dispose()
        {
            if (_disposed)
                return;

            _disposed = true;
            if (ReferenceEquals(Current, this))
                Current = null;
            _channel.Dispose();
        }
    }
}
