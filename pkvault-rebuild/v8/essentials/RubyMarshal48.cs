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
    public byte[] Bytes { get; } = bytes;
    public Dictionary<string, object?> Ivars { get; } = new(StringComparer.Ordinal);
    public string Text => Encoding.UTF8.GetString(Bytes);
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
