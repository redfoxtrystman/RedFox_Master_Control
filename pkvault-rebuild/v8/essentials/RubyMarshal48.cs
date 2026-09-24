using System.Buffers.Binary;
using System.Text;

namespace PKVault.Core;

/// <summary>
/// Minimal Ruby 1.8 Marshal 4.8 reader for legacy Pokémon Essentials saves.
/// It intentionally focuses on the value types present in Essentials/RMXP
/// save streams and preserves object/symbol links.
/// </summary>
public sealed class RubyMarshal48Reader
{
    private readonly ReadOnlyMemory<byte> Source;
    private int Position;
    private readonly List<string> Symbols = [];
    private readonly List<object?> Objects = [];

    public RubyMarshal48Reader(ReadOnlyMemory<byte> source, int offset = 0)
    {
        Source = source;
        Position = offset;
    }

    public int BytesConsumed => Position;
    public int StartOffset { get; private set; }

    public RubyMarshalDocument ReadDocument()
    {
        StartOffset = Position;
        Require(2);
        if (ReadByte() != 4 || ReadByte() != 8)
            throw new InvalidDataException($"Ruby Marshal 4.8 header missing at offset {StartOffset}.");

        Symbols.Clear();
        Objects.Clear();
        var value = ReadValue();
        return new(value, StartOffset, Position - StartOffset);
    }

    private object? ReadValue()
    {
        Require(1);
        var tag = (char)ReadByte();
        return tag switch
        {
            '0' => null,
            'T' => true,
            'F' => false,
            'i' => ReadLong(),
            'l' => ReadBignum(),
            'f' => Register(new RubyFloat(ReadRawString())),
            '"' => Register(new RubyString(ReadBytes(ReadLong()))),
            ':' => ReadNewSymbol(),
            ';' => ReadSymbolLink(),
            '@' => ReadObjectLink(),
            '[' => ReadArray(),
            '{' => ReadHash(false),
            '}' => ReadHash(true),
            'o' => ReadRubyObject(),
            'I' => ReadIvarWrapper(),
            'u' => ReadUserDefined(),
            'U' => ReadUserMarshal(),
            'd' => ReadDataObject(),
            'C' => ReadUserClass(),
            'e' => ReadExtended(),
            'c' => Register(new RubyClassRef(ReadRawString())),
            'm' => Register(new RubyModuleRef(ReadRawString())),
            '/' => ReadRegexp(),
            'S' => ReadStruct(),
            _ => throw new InvalidDataException($"Unsupported Ruby Marshal tag 0x{(byte)tag:X2} '{tag}' at offset {Position - 1}."),
        };
    }

    private long ReadBignum()
    {
        var sign = (char)ReadByte();
        var words = checked((int)ReadLong());
        if (words < 0 || words > 8)
            throw new InvalidDataException($"Unsupported Ruby bignum word count {words}.");

        ulong value = 0;
        for (var i = 0; i < words * 2; i++)
            value |= (ulong)ReadByte() << (8 * i);

        if (value > long.MaxValue)
            throw new OverflowException("Ruby bignum exceeds Int64 range.");

        var signed = (long)value;
        return sign == '-' ? -signed : signed;
    }

    private RubyArray ReadArray()
    {
        var arr = Register(new RubyArray());
        var count = CheckedCount(ReadLong());
        for (var i = 0; i < count; i++)
            arr.Items.Add(ReadValue());
        return arr;
    }

    private RubyHash ReadHash(bool hasDefault)
    {
        var hash = Register(new RubyHash());
        hash.HasDefault = hasDefault;
        var count = CheckedCount(ReadLong());
        for (var i = 0; i < count; i++)
            hash.Entries.Add(new(ReadValue(), ReadValue()));
        if (hasDefault)
            hash.DefaultValue = ReadValue();
        return hash;
    }

    private RubyObject ReadRubyObject()
    {
        var className = ReadSymbol();
        var obj = Register(new RubyObject(className));
        ReadMembers(obj.Fields);
        return obj;
    }

    private object? ReadIvarWrapper()
    {
        var inner = ReadValue();
        var count = CheckedCount(ReadLong());
        var ivars = new Dictionary<string, object?>(StringComparer.Ordinal);
        for (var i = 0; i < count; i++)
            ivars[ReadSymbol()] = ReadValue();

        if (inner is IRubyWithIvars target)
            foreach (var entry in ivars)
                target.Ivars[entry.Key] = entry.Value;

        return inner;
    }

    private RubyUserDefined ReadUserDefined()
    {
        var className = ReadSymbol();
        var bytes = ReadBytes(ReadLong());
        return Register(new RubyUserDefined(className, bytes));
    }

    private RubyUserMarshal ReadUserMarshal()
    {
        var className = ReadSymbol();
        var obj = Register(new RubyUserMarshal(className));
        obj.Value = ReadValue();
        return obj;
    }

    private RubyDataObject ReadDataObject()
    {
        var className = ReadSymbol();
        var obj = Register(new RubyDataObject(className));
        obj.Value = ReadValue();
        return obj;
    }

    private RubyUserClass ReadUserClass()
    {
        var className = ReadSymbol();
        var obj = Register(new RubyUserClass(className));
        obj.Value = ReadValue();
        return obj;
    }

    private object? ReadExtended()
    {
        var moduleName = ReadSymbol();
        var obj = ReadValue();
        if (obj is IRubyExtended extended)
            extended.Modules.Add(moduleName);
        return obj;
    }

    private RubyRegexp ReadRegexp()
    {
        var pattern = ReadBytes(ReadLong());
        var options = ReadByte();
        return Register(new RubyRegexp(pattern, options));
    }

    private RubyStruct ReadStruct()
    {
        var className = ReadSymbol();
        var obj = Register(new RubyStruct(className));
        ReadMembers(obj.Fields);
        return obj;
    }

    private void ReadMembers(Dictionary<string, object?> members)
    {
        var count = CheckedCount(ReadLong());
        for (var i = 0; i < count; i++)
            members[ReadSymbol()] = ReadValue();
    }

    private string ReadNewSymbol()
    {
        var value = ReadRawString();
        Symbols.Add(value);
        return value;
    }

    private string ReadSymbolLink()
    {
        var index = CheckedIndex(ReadLong(), Symbols.Count, "symbol");
        return Symbols[index];
    }

    private object? ReadObjectLink()
    {
        var index = CheckedIndex(ReadLong(), Objects.Count, "object");
        return Objects[index];
    }

    private string ReadSymbol()
    {
        Require(1);
        var tag = (char)ReadByte();
        return tag switch
        {
            ':' => ReadNewSymbol(),
            ';' => ReadSymbolLink(),
            _ => throw new InvalidDataException($"Expected Ruby symbol at offset {Position - 1}, got '{tag}'."),
        };
    }

    private RubyFloat Register(RubyFloat value) => RegisterObject(value);
    private RubyString Register(RubyString value) => RegisterObject(value);
    private RubyArray Register(RubyArray value) => RegisterObject(value);
    private RubyHash Register(RubyHash value) => RegisterObject(value);
    private RubyObject Register(RubyObject value) => RegisterObject(value);
    private RubyUserDefined Register(RubyUserDefined value) => RegisterObject(value);
    private RubyUserMarshal Register(RubyUserMarshal value) => RegisterObject(value);
    private RubyDataObject Register(RubyDataObject value) => RegisterObject(value);
    private RubyUserClass Register(RubyUserClass value) => RegisterObject(value);
    private RubyClassRef Register(RubyClassRef value) => RegisterObject(value);
    private RubyModuleRef Register(RubyModuleRef value) => RegisterObject(value);
    private RubyRegexp Register(RubyRegexp value) => RegisterObject(value);
    private RubyStruct Register(RubyStruct value) => RegisterObject(value);

    private T RegisterObject<T>(T value) where T : class
    {
        Objects.Add(value);
        return value;
    }

    private string ReadRawString()
    {
        var bytes = ReadBytes(ReadLong());
        return DecodeString(bytes);
    }

    private byte[] ReadBytes(long rawLength)
    {
        if (rawLength < 0 || rawLength > int.MaxValue)
            throw new InvalidDataException($"Invalid Ruby string length {rawLength}.");

        var length = (int)rawLength;
        Require(length);
        var bytes = Source.Span.Slice(Position, length).ToArray();
        Position += length;
        return bytes;
    }

    private static string DecodeString(ReadOnlySpan<byte> bytes)
    {
        // Essentials save strings are typically ASCII/UTF-8. Keep malformed
        // bytes lossless enough for diagnostics rather than throwing.
        return Encoding.UTF8.GetString(bytes);
    }

    private long ReadLong()
    {
        var c = unchecked((sbyte)ReadByte());
        if (c == 0)
            return 0;
        if (c >= 5)
            return c - 5;
        if (c <= -5)
            return c + 5;

        if (c > 0)
        {
            long value = 0;
            for (var i = 0; i < c; i++)
                value |= (long)ReadByte() << (8 * i);
            return value;
        }

        var count = -c;
        long raw = 0;
        for (var i = 0; i < count; i++)
            raw |= (long)ReadByte() << (8 * i);

        return raw - (1L << (8 * count));
    }

    private byte ReadByte()
    {
        Require(1);
        return Source.Span[Position++];
    }

    private void Require(int count)
    {
        if (count < 0 || Position + count > Source.Length)
            throw new EndOfStreamException($"Ruby Marshal value exceeds source at offset {Position}.");
    }

    private static int CheckedCount(long value)
    {
        if (value < 0 || value > 1_000_000)
            throw new InvalidDataException($"Unreasonable Ruby collection size {value}.");
        return (int)value;
    }

    private static int CheckedIndex(long value, int count, string kind)
    {
        if (value < 0 || value >= count)
            throw new InvalidDataException($"Invalid Ruby {kind} link {value}; count={count}.");
        return (int)value;
    }
}

public sealed record RubyMarshalDocument(object? Root, int Offset, int Length);

public interface IRubyWithIvars
{
    Dictionary<string, object?> Ivars { get; }
}

public interface IRubyExtended
{
    List<string> Modules { get; }
}

public sealed class RubyString(byte[] bytes) : IRubyWithIvars
{
    public byte[] Bytes { get; private set; } = bytes;
    public Dictionary<string, object?> Ivars { get; } = new(StringComparer.Ordinal);
    public string Text => Encoding.UTF8.GetString(Bytes);
    public void SetText(string value) => Bytes = Encoding.UTF8.GetBytes(value);
    public override string ToString() => Text;
}

public sealed record RubyFloat(string Raw);
public sealed class RubyArray
{
    public List<object?> Items { get; } = [];
}
public sealed class RubyHash
{
    public List<KeyValuePair<object?, object?>> Entries { get; } = [];
    public bool HasDefault { get; set; }
    public object? DefaultValue { get; set; }
}
public sealed class RubyObject(string className) : IRubyWithIvars, IRubyExtended
{
    public string ClassName { get; } = className;
    public Dictionary<string, object?> Fields { get; } = new(StringComparer.Ordinal);
    public Dictionary<string, object?> Ivars { get; } = new(StringComparer.Ordinal);
    public List<string> Modules { get; } = [];
}
public sealed record RubyUserDefined(string ClassName, byte[] Data);
public sealed class RubyUserMarshal(string className)
{
    public string ClassName { get; } = className;
    public object? Value { get; set; }
}
public sealed class RubyDataObject(string className)
{
    public string ClassName { get; } = className;
    public object? Value { get; set; }
}
public sealed class RubyUserClass(string className)
{
    public string ClassName { get; } = className;
    public object? Value { get; set; }
}
public sealed record RubyClassRef(string Name);
public sealed record RubyModuleRef(string Name);
public sealed record RubyRegexp(byte[] Pattern, byte Options);
public sealed class RubyStruct(string className)
{
    public string ClassName { get; } = className;
    public Dictionary<string, object?> Fields { get; } = new(StringComparer.Ordinal);
}

public static class RubyValue
{
    public static long Int(object? value, long fallback = 0) => value switch
    {
        int i => i,
        long l => l,
        _ => fallback,
    };

    public static string Text(object? value, string fallback = "") => value switch
    {
        string s => s,
        RubyString s => s.Text,
        _ => fallback,
    };

    public static RubyObject? Object(object? value, string? className = null)
        => value is RubyObject obj && (className == null || obj.ClassName == className) ? obj : null;

    public static RubyArray? Array(object? value) => value as RubyArray;
}


/// <summary>
/// Ruby Marshal 4.8 writer paired with <see cref="RubyMarshal48Reader"/>.
/// It preserves symbol/object links and the value kinds used by legacy
/// Pokémon Essentials saves. This lets PKVault rewrite only the trainer and
/// storage streams while leaving every unrelated top-level stream untouched.
/// </summary>
public sealed class RubyMarshal48Writer
{
    private readonly MemoryStream Output = new();
    private readonly Dictionary<string, int> Symbols = new(StringComparer.Ordinal);
    private readonly Dictionary<object, int> Objects = new(ReferenceComparer.Instance);

    public static byte[] WriteDocument(object? root)
    {
        var writer = new RubyMarshal48Writer();
        writer.Output.WriteByte(4);
        writer.Output.WriteByte(8);
        writer.WriteValue(root);
        return writer.Output.ToArray();
    }

    public static object? CloneValue(object? root)
    {
        var bytes = WriteDocument(root);
        return new RubyMarshal48Reader(bytes).ReadDocument().Root;
    }

    private void WriteValue(object? value)
    {
        switch (value)
        {
            case null:
                Output.WriteByte((byte)'0');
                return;
            case bool b:
                Output.WriteByte((byte)(b ? 'T' : 'F'));
                return;
            case byte b:
                WriteInteger(b);
                return;
            case sbyte b:
                WriteInteger(b);
                return;
            case short s:
                WriteInteger(s);
                return;
            case ushort s:
                WriteInteger(s);
                return;
            case int i:
                WriteInteger(i);
                return;
            case uint i:
                WriteInteger(i);
                return;
            case long l:
                WriteInteger(l);
                return;
            case string symbol:
                WriteSymbol(symbol);
                return;
        }

        if (!IsLinkable(value))
            throw new InvalidDataException($"Unsupported Ruby Marshal value type {value.GetType().FullName}.");

        if (Objects.TryGetValue(value, out var linkedIndex))
        {
            Output.WriteByte((byte)'@');
            WriteLong(linkedIndex);
            return;
        }

        if (value is IRubyExtended extended && extended.Modules.Count > 0)
        {
            for (var i = extended.Modules.Count - 1; i >= 0; i--)
            {
                Output.WriteByte((byte)'e');
                WriteSymbol(extended.Modules[i]);
            }
        }

        if (value is IRubyWithIvars withIvars && withIvars.Ivars.Count > 0)
        {
            Output.WriteByte((byte)'I');
            WriteCore(value);
            WriteLong(withIvars.Ivars.Count);
            foreach (var (key, ivar) in withIvars.Ivars)
            {
                WriteSymbol(key);
                WriteValue(ivar);
            }
            return;
        }

        WriteCore(value);
    }

    private void WriteCore(object value)
    {
        switch (value)
        {
            case RubyFloat f:
                Register(value);
                Output.WriteByte((byte)'f');
                WriteRawString(f.Raw);
                break;
            case RubyString s:
                Register(value);
                Output.WriteByte((byte)'"');
                WriteRawBytes(s.Bytes);
                break;
            case RubyArray a:
                Register(value);
                Output.WriteByte((byte)'[');
                WriteLong(a.Items.Count);
                foreach (var item in a.Items)
                    WriteValue(item);
                break;
            case RubyHash h:
                Register(value);
                Output.WriteByte((byte)(h.HasDefault ? '}' : '{'));
                WriteLong(h.Entries.Count);
                foreach (var pair in h.Entries)
                {
                    WriteValue(pair.Key);
                    WriteValue(pair.Value);
                }
                if (h.HasDefault)
                    WriteValue(h.DefaultValue);
                break;
            case RubyObject o:
                Register(value);
                Output.WriteByte((byte)'o');
                WriteSymbol(o.ClassName);
                WriteMembers(o.Fields);
                break;
            case RubyUserDefined u:
                Register(value);
                Output.WriteByte((byte)'u');
                WriteSymbol(u.ClassName);
                WriteRawBytes(u.Data);
                break;
            case RubyUserMarshal u:
                Register(value);
                Output.WriteByte((byte)'U');
                WriteSymbol(u.ClassName);
                WriteValue(u.Value);
                break;
            case RubyDataObject d:
                Register(value);
                Output.WriteByte((byte)'d');
                WriteSymbol(d.ClassName);
                WriteValue(d.Value);
                break;
            case RubyUserClass c:
                Register(value);
                Output.WriteByte((byte)'C');
                WriteSymbol(c.ClassName);
                WriteValue(c.Value);
                break;
            case RubyClassRef c:
                Register(value);
                Output.WriteByte((byte)'c');
                WriteRawString(c.Name);
                break;
            case RubyModuleRef m:
                Register(value);
                Output.WriteByte((byte)'m');
                WriteRawString(m.Name);
                break;
            case RubyRegexp r:
                Register(value);
                Output.WriteByte((byte)'/');
                WriteRawBytes(r.Pattern);
                Output.WriteByte(r.Options);
                break;
            case RubyStruct s:
                Register(value);
                Output.WriteByte((byte)'S');
                WriteSymbol(s.ClassName);
                WriteMembers(s.Fields);
                break;
            default:
                throw new InvalidDataException($"Unsupported Ruby Marshal object type {value.GetType().FullName}.");
        }
    }

    private void WriteMembers(Dictionary<string, object?> members)
    {
        WriteLong(members.Count);
        foreach (var (key, value) in members)
        {
            WriteSymbol(key);
            WriteValue(value);
        }
    }

    private void WriteSymbol(string value)
    {
        if (Symbols.TryGetValue(value, out var index))
        {
            Output.WriteByte((byte)';');
            WriteLong(index);
            return;
        }

        Symbols.Add(value, Symbols.Count);
        Output.WriteByte((byte)':');
        WriteRawString(value);
    }

    private void Register(object value)
    {
        if (!Objects.TryAdd(value, Objects.Count))
            throw new InvalidDataException("Ruby Marshal object was registered twice without an object link.");
    }

    private static bool IsLinkable(object value) => value is
        RubyFloat or RubyString or RubyArray or RubyHash or RubyObject or
        RubyUserDefined or RubyUserMarshal or RubyDataObject or RubyUserClass or
        RubyClassRef or RubyModuleRef or RubyRegexp or RubyStruct;

    private void WriteInteger(long value)
    {
        if (value is >= int.MinValue and <= int.MaxValue)
        {
            Output.WriteByte((byte)'i');
            WriteLong(value);
            return;
        }

        Output.WriteByte((byte)'l');
        var negative = value < 0;
        Output.WriteByte((byte)(negative ? '-' : '+'));

        ulong magnitude = negative
            ? (ulong)(-(value + 1)) + 1
            : (ulong)value;
        var byteCount = 1;
        var probe = magnitude;
        while ((probe >>= 8) != 0)
            byteCount++;
        var words = (byteCount + 1) / 2;
        WriteLong(words);
        for (var i = 0; i < words * 2; i++)
            Output.WriteByte((byte)(magnitude >> (8 * i)));
    }

    private void WriteLong(long value)
    {
        if (value == 0)
        {
            Output.WriteByte(0);
            return;
        }

        if (value > 0 && value < 123)
        {
            Output.WriteByte((byte)(value + 5));
            return;
        }

        if (value < 0 && value > -124)
        {
            Output.WriteByte(unchecked((byte)(sbyte)(value - 5)));
            return;
        }

        if (value > int.MaxValue || value < int.MinValue)
            throw new InvalidDataException($"Ruby Marshal long {value} exceeds the supported 32-bit fixnum encoding.");

        if (value > 0)
        {
            var raw = (uint)value;
            var count = 1;
            while (count < 4 && (raw >> (count * 8)) != 0)
                count++;
            Output.WriteByte((byte)count);
            for (var i = 0; i < count; i++)
                Output.WriteByte((byte)(raw >> (8 * i)));
            return;
        }

        var bits = unchecked((uint)(int)value);
        var negativeCount = 4;
        while (negativeCount > 1 && ((bits >> ((negativeCount - 1) * 8)) & 0xFF) == 0xFF)
            negativeCount--;

        Output.WriteByte(unchecked((byte)(sbyte)-negativeCount));
        for (var i = 0; i < negativeCount; i++)
            Output.WriteByte((byte)(bits >> (8 * i)));
    }

    private void WriteRawString(string value) => WriteRawBytes(Encoding.UTF8.GetBytes(value));

    private void WriteRawBytes(ReadOnlySpan<byte> bytes)
    {
        WriteLong(bytes.Length);
        Output.Write(bytes);
    }

    private sealed class ReferenceComparer : IEqualityComparer<object>
    {
        public static readonly ReferenceComparer Instance = new();
        public new bool Equals(object? x, object? y) => ReferenceEquals(x, y);
        public int GetHashCode(object obj) => System.Runtime.CompilerServices.RuntimeHelpers.GetHashCode(obj);
    }
}
