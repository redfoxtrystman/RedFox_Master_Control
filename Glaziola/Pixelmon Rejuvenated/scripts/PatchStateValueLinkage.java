import java.nio.file.*;
import jdk.internal.org.objectweb.asm.*;
import jdk.internal.org.objectweb.asm.tree.*;

/**
 * Repairs Minecraft 1.21.1 bytecode references compiled against a defective
 * BlockState#setValue stub returning BlockState instead of Object.
 *
 * Compile (Java 21):
 * javac --add-exports java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED --add-exports java.base/jdk.internal.org.objectweb.asm.tree=ALL-UNNAMED scripts/PatchStateValueLinkage.java
 * Run on an unpacked Alpha 48 build/pack:
 * java --add-exports java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED --add-exports java.base/jdk.internal.org.objectweb.asm.tree=ALL-UNNAMED -cp scripts PatchStateValueLinkage build/pack
 *
 * For regular releases, use real NeoForge/Minecraft libraries, not stubs.
 */
public final class PatchStateValueLinkage {
    private static final String STATE = "net/minecraft/world/level/block/state/BlockState";
    private static final String PROP = "net/minecraft/world/level/block/state/properties/Property";
    private static final String BAD = "(L" + PROP + ";Ljava/lang/Comparable;)L" + STATE + ";";
    private static final String GOOD = "(L" + PROP + ";Ljava/lang/Comparable;)Ljava/lang/Object;";
    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("Usage: PatchStateValueLinkage <build/pack>");
        Path classes = Path.of(args[0]).resolve("com/glaziola/pixelmonrejuvenated");
        int scanned=0, files=0, fixed=0;
        try (var paths = Files.walk(classes)) {
            for (Path path : (Iterable<Path>) paths.filter(p -> p.toString().endsWith(".class"))::iterator) {
                scanned++;
                ClassNode c = new ClassNode();
                new ClassReader(Files.readAllBytes(path)).accept(c, 0);
                int n=0;
                for (MethodNode method : c.methods) {
                    for (AbstractInsnNode in=method.instructions.getFirst(); in!=null;) {
                        AbstractInsnNode next=in.getNext();
                        if (in instanceof MethodInsnNode m && m.owner.equals(STATE)
                                && m.name.equals("setValue") && m.desc.equals(BAD)) {
                            m.desc=GOOD;
                            method.instructions.insert(m, new TypeInsnNode(Opcodes.CHECKCAST,STATE));
                            n++;
                        }
                        in=next;
                    }
                }
                if (n>0) {
                    ClassWriter writer = new ClassWriter(0);
                    c.accept(writer);
                    Files.write(path,writer.toByteArray());
                    files++; fixed+=n;
                    System.out.println("Fixed "+path.getFileName()+" calls="+n);
                }
            }
        }
        if (files!=2 || fixed!=20)
            throw new IllegalStateException("Unexpected Alpha 48 input: expected 20 bad calls in two classes; found "+fixed+" / "+files);
        System.out.println("Validated "+scanned+" classes; repaired "+fixed+" calls");
    }
}
