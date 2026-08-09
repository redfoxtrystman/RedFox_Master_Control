using Mono.Cecil;
using Mono.Cecil.Cil;
using System.Text;

if (args.Length == 0)
{
    Console.Error.WriteLine("Usage: ILDump <assembly.dll> [output.txt]");
    return 2;
}

var input = Path.GetFullPath(args[0]);
var output = args.Length > 1 ? Path.GetFullPath(args[1]) : input + ".ildump.txt";
var resolver = new DefaultAssemblyResolver();
resolver.AddSearchDirectory(Path.GetDirectoryName(input)!);
var rp = new ReaderParameters { AssemblyResolver = resolver, ReadSymbols = false };
using var asm = AssemblyDefinition.ReadAssembly(input, rp);

var sb = new StringBuilder(1024 * 1024);
sb.AppendLine($"ASSEMBLY {asm.Name.FullName}");
sb.AppendLine("REFERENCES");
foreach (var r in asm.MainModule.AssemblyReferences) sb.AppendLine($"  {r.FullName}");
sb.AppendLine();

foreach (var t in asm.MainModule.Types.SelectMany(Flatten))
{
    sb.AppendLine($"TYPE {t.FullName} : {t.BaseType?.FullName ?? "<none>"}");
    DumpAttributes(sb, t.CustomAttributes, "  ATTR ");
    foreach (var f in t.Fields)
        sb.AppendLine($"  FIELD {f.Attributes} {f.FieldType.FullName} {f.Name}" + (f.HasConstant ? $" = {Format(f.Constant)}" : ""));
    foreach (var p in t.Properties)
        sb.AppendLine($"  PROPERTY {p.PropertyType.FullName} {p.Name} get={p.GetMethod?.Name ?? "-"} set={p.SetMethod?.Name ?? "-"}");
    foreach (var m in t.Methods)
    {
        sb.AppendLine();
        sb.Append($"  METHOD {m.Attributes} {m.ReturnType.FullName} {m.Name}(");
        sb.Append(string.Join(", ", m.Parameters.Select(p => p.ParameterType.FullName + " " + p.Name)));
        sb.AppendLine(")");
        DumpAttributes(sb, m.CustomAttributes, "    ATTR ");
        if (!m.HasBody) continue;
        sb.AppendLine($"    MAXSTACK {m.Body.MaxStackSize} INITLOCALS {m.Body.InitLocals}");
        for (int i = 0; i < m.Body.Variables.Count; i++)
            sb.AppendLine($"    LOCAL V_{i} {m.Body.Variables[i].VariableType.FullName}");
        foreach (var eh in m.Body.ExceptionHandlers)
            sb.AppendLine($"    EH {eh.HandlerType} try IL_{eh.TryStart?.Offset:X4}-IL_{eh.TryEnd?.Offset:X4} handler IL_{eh.HandlerStart?.Offset:X4}-IL_{eh.HandlerEnd?.Offset:X4} catch={eh.CatchType?.FullName}");
        foreach (var ins in m.Body.Instructions)
            sb.AppendLine($"    IL_{ins.Offset:X4}: {ins.OpCode,-12} {Operand(ins.Operand)}");
    }
    sb.AppendLine();
}

File.WriteAllText(output, sb.ToString(), new UTF8Encoding(false));
Console.WriteLine(output);
return 0;

static IEnumerable<TypeDefinition> Flatten(TypeDefinition t)
{
    yield return t;
    foreach (var n in t.NestedTypes)
        foreach (var x in Flatten(n)) yield return x;
}

static void DumpAttributes(StringBuilder sb, IEnumerable<CustomAttribute> attrs, string prefix)
{
    foreach (var a in attrs)
    {
        try
        {
            var args = string.Join(", ", a.ConstructorArguments.Select(x => Format(x.Value)));
            sb.AppendLine($"{prefix}{a.AttributeType.FullName}({args})");
        }
        catch (Exception ex)
        {
            sb.AppendLine($"{prefix}{a.AttributeType.FullName}(<? unresolved: {ex.GetType().Name}: {ex.Message} ?>)");
        }
    }
}

static string Operand(object? o) => o switch
{
    null => "",
    string s => "\"" + s.Replace("\\", "\\\\").Replace("\"", "\\\"").Replace("\r", "\\r").Replace("\n", "\\n") + "\"",
    Instruction i => $"IL_{i.Offset:X4}",
    Instruction[] a => "[" + string.Join(", ", a.Select(i => $"IL_{i.Offset:X4}")) + "]",
    MethodReference m => m.FullName,
    FieldReference f => f.FullName,
    TypeReference t => t.FullName,
    ParameterDefinition p => p.Name,
    VariableDefinition v => $"V_{v.Index}",
    _ => o.ToString() ?? ""
};

static string Format(object? o) => o switch
{
    null => "null",
    string s => "\"" + s.Replace("\"", "\\\"") + "\"",
    CustomAttributeArgument[] a => "[" + string.Join(", ", a.Select(x => Format(x.Value))) + "]",
    _ => o.ToString() ?? ""
};
