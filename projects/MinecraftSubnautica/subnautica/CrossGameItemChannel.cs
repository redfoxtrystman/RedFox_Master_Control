using System;
using System.Diagnostics;
using System.IO.MemoryMappedFiles;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;

namespace MinecraftSubnautica.Bridge
{
    /// <summary>
    /// Reliable single-producer/single-consumer item transport in both directions.
    /// Ring consumption is the acknowledgement for a successful handoff; TransferId lets adapters
    /// make processing idempotent across their own save/recovery layer.
    /// </summary>
    public sealed class CrossGameItemChannel : IDisposable
    {
        private readonly MemoryMappedFile _mapping;
        private readonly MemoryMappedViewAccessor _view;
        private readonly object _hostWriteLock = new object();
        private readonly object _hostReadLock = new object();
        private bool _disposed;

        public CrossGameItemChannel(string mappingName = null)
        {
            string name = string.IsNullOrWhiteSpace(mappingName)
                ? CrossGameItemProtocol.DefaultMappingName
                : mappingName;

            _mapping = MemoryMappedFile.CreateOrOpen(name, CrossGameItemProtocol.MappingBytes, MemoryMappedFileAccess.ReadWrite);
            _view = _mapping.CreateViewAccessor(0, CrossGameItemProtocol.MappingBytes, MemoryMappedFileAccess.ReadWrite);

            _view.Write(CrossGameItemProtocol.OffHeader + CrossGameItemProtocol.HMagic, CrossGameItemProtocol.Magic);
            _view.Write(CrossGameItemProtocol.OffHeader + CrossGameItemProtocol.HVersion, CrossGameItemProtocol.Version);
            _view.Write(CrossGameItemProtocol.OffHeader + CrossGameItemProtocol.HHostPid, (uint)Process.GetCurrentProcess().Id);
            PulseHostHeartbeat();
        }

        public void PulseHostHeartbeat()
        {
            ThrowIfDisposed();
            _view.Write(CrossGameItemProtocol.OffHeader + CrossGameItemProtocol.HHostHeartbeat, NativeMethods.GetTickCount64());
        }

        public uint MinecraftPid
        {
            get
            {
                ThrowIfDisposed();
                return _view.ReadUInt32(CrossGameItemProtocol.OffHeader + CrossGameItemProtocol.HMinecraftPid);
            }
        }

        public bool MinecraftHeartbeatIsFresh(long timeoutMs = 8000)
        {
            ThrowIfDisposed();
            ulong beat = _view.ReadUInt64(
                CrossGameItemProtocol.OffHeader + CrossGameItemProtocol.HMinecraftHeartbeat);

            if (beat == 0)
                return false;

            ulong now = NativeMethods.GetTickCount64();
            return now >= beat && now - beat < (ulong)Math.Max(1, timeoutMs);
        }

        public bool TrySendToMinecraft(CrossGameItem item)
        {
            lock (_hostWriteLock)
                return TryWrite(CrossGameItemProtocol.OffHostToMinecraft, item);
        }

        public bool TryReceiveFromMinecraft(out CrossGameItem item)
        {
            lock (_hostReadLock)
                return TryRead(CrossGameItemProtocol.OffMinecraftToHost, out item);
        }

        private bool TryWrite(long ringBase, CrossGameItem item)
        {
            ThrowIfDisposed();
            if (item == null)
                throw new ArgumentNullException("item");
            if (string.IsNullOrWhiteSpace(item.ItemId))
                throw new ArgumentException("Cross-game items require a stable namespaced ItemId.", "item");

            ulong head = _view.ReadUInt64(ringBase + CrossGameItemProtocol.RHead);
            ulong tail = _view.ReadUInt64(ringBase + CrossGameItemProtocol.RTail);
            if (head - tail >= (ulong)CrossGameItemProtocol.RingEntries)
                return false;

            long record = ringBase + CrossGameItemProtocol.RData
                + (long)(head & (CrossGameItemProtocol.RingEntries - 1)) * CrossGameItemProtocol.RecordBytes;

            WriteRecord(record, item);
            Thread.MemoryBarrier();
            _view.Write(ringBase + CrossGameItemProtocol.RHead, head + 1);
            return true;
        }

        private bool TryRead(long ringBase, out CrossGameItem item)
        {
            ThrowIfDisposed();
            item = null;

            ulong head = _view.ReadUInt64(ringBase + CrossGameItemProtocol.RHead);
            ulong tail = _view.ReadUInt64(ringBase + CrossGameItemProtocol.RTail);
            if (tail >= head)
                return false;

            long record = ringBase + CrossGameItemProtocol.RData
                + (long)(tail & (CrossGameItemProtocol.RingEntries - 1)) * CrossGameItemProtocol.RecordBytes;

            CrossGameItem parsed = ReadRecord(record);
            Thread.MemoryBarrier();
            _view.Write(ringBase + CrossGameItemProtocol.RTail, tail + 1);
            item = parsed;
            return true;
        }

        private void WriteRecord(long b, CrossGameItem item)
        {
            _view.Write(b + CrossGameItemProtocol.ITransferId, item.TransferId);
            _view.Write(b + CrossGameItemProtocol.IOperation, (uint)item.Operation);
            _view.Write(b + CrossGameItemProtocol.IOrigin, (uint)item.Origin);
            _view.Write(b + CrossGameItemProtocol.IFlags, (uint)item.Flags);
            _view.Write(b + CrossGameItemProtocol.ICount, item.Count);
            _view.Write(b + CrossGameItemProtocol.IMaxStack, item.MaxStack);
            _view.Write(b + CrossGameItemProtocol.IEnergy, item.Energy);
            _view.Write(b + CrossGameItemProtocol.IMaxEnergy, item.MaxEnergy);
            _view.Write(b + CrossGameItemProtocol.IDurability, item.Durability);
            _view.Write(b + CrossGameItemProtocol.IMaxDurability, item.MaxDurability);

            WriteUtf8(b + CrossGameItemProtocol.IId, CrossGameItemProtocol.IdBytes, b + CrossGameItemProtocol.IIdLength, item.ItemId);
            WriteUtf8(b + CrossGameItemProtocol.IName, CrossGameItemProtocol.NameBytes, b + CrossGameItemProtocol.INameLength, item.DisplayName ?? string.Empty);
            WriteUtf8(b + CrossGameItemProtocol.IState, CrossGameItemProtocol.StateBytes, b + CrossGameItemProtocol.IStateLength, item.StateJson ?? string.Empty);
        }

        private CrossGameItem ReadRecord(long b)
        {
            return new CrossGameItem
            {
                TransferId = _view.ReadUInt64(b + CrossGameItemProtocol.ITransferId),
                Operation = (CrossGameItemOp)_view.ReadUInt32(b + CrossGameItemProtocol.IOperation),
                Origin = (CrossGameOrigin)_view.ReadUInt32(b + CrossGameItemProtocol.IOrigin),
                Flags = (CrossGameItemFlags)_view.ReadUInt32(b + CrossGameItemProtocol.IFlags),
                Count = _view.ReadInt32(b + CrossGameItemProtocol.ICount),
                MaxStack = _view.ReadInt32(b + CrossGameItemProtocol.IMaxStack),
                Energy = _view.ReadSingle(b + CrossGameItemProtocol.IEnergy),
                MaxEnergy = _view.ReadSingle(b + CrossGameItemProtocol.IMaxEnergy),
                Durability = _view.ReadSingle(b + CrossGameItemProtocol.IDurability),
                MaxDurability = _view.ReadSingle(b + CrossGameItemProtocol.IMaxDurability),
                ItemId = ReadUtf8(b + CrossGameItemProtocol.IId, CrossGameItemProtocol.IdBytes, _view.ReadInt32(b + CrossGameItemProtocol.IIdLength)),
                DisplayName = ReadUtf8(b + CrossGameItemProtocol.IName, CrossGameItemProtocol.NameBytes, _view.ReadInt32(b + CrossGameItemProtocol.INameLength)),
                StateJson = ReadUtf8(b + CrossGameItemProtocol.IState, CrossGameItemProtocol.StateBytes, _view.ReadInt32(b + CrossGameItemProtocol.IStateLength))
            };
        }

        private void WriteUtf8(long dataOffset, int capacity, long lengthOffset, string value)
        {
            byte[] bytes = Encoding.UTF8.GetBytes(value ?? string.Empty);
            if (bytes.Length > capacity)
                throw new ArgumentException("UTF-8 field exceeds fixed protocol capacity.");

            byte[] zero = new byte[capacity];
            _view.WriteArray(dataOffset, zero, 0, zero.Length);
            if (bytes.Length != 0)
                _view.WriteArray(dataOffset, bytes, 0, bytes.Length);
            _view.Write(lengthOffset, bytes.Length);
        }

        private string ReadUtf8(long dataOffset, int capacity, int length)
        {
            if (length < 0 || length > capacity)
                throw new InvalidOperationException("Corrupt cross-game item string length.");

            if (length == 0)
                return string.Empty;

            byte[] bytes = new byte[length];
            _view.ReadArray(dataOffset, bytes, 0, length);
            return Encoding.UTF8.GetString(bytes);
        }

        private static class NativeMethods
        {
            [DllImport("kernel32.dll")]
            internal static extern ulong GetTickCount64();
        }

        private void ThrowIfDisposed()
        {
            if (_disposed)
                throw new ObjectDisposedException("CrossGameItemChannel");
        }

        public void Dispose()
        {
            if (_disposed)
                return;
            _disposed = true;
            _view.Dispose();
            _mapping.Dispose();
        }
    }
}
