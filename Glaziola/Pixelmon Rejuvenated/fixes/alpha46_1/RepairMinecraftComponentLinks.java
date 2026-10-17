import java.nio.file.*;
import java.util.Set;
import jdk.internal.org.objectweb.asm.*;

/**
 * Java 21 patch of erroneous Component static factory references in precompiled Alpha 46 classes.
 * Uses the ASM bundled with the JDK. Run only once on ORIGINAL unpatched build/pack.
 */
public final class RepairMinecraftComponentLinks {
    private static final String COMPONENT = "net/minecraft/network/chat/Component";
    private static final String MUTABLE = "Lnet/minecraft/network/chat/MutableComponent;";
    private static final Set<String> FACTORIES = Set.of(
        "translatable", "translatableEscape", "literal", "empty", "keybind",
        "score", "selector", "nbt"
    );

    public static void main(String[] args) throws Exception {
        if (args.length != 1)
            throw new IllegalArgumentException("Usage: RepairMinecraftComponentLinks <classes-dir>");
        Path dir = Paths.get(args[0]);
        int files = 0, changed = 0, calls = 0;
        try (var paths = Files.walk(dir)) {
            for (Path p : (Iterable<Path>)paths.filter(x -> x.toString().endsWith(".class"))::iterator) {
                files++;
                byte[] original = Files.readAllBytes(p);
                ClassReader reader = new ClassReader(original);
                ClassWriter writer = new ClassWriter(0);
                final int[] repaired = {0};
                ClassVisitor visitor = new ClassVisitor(Opcodes.ASM8, writer) {
                    @Override
                    public MethodVisitor visitMethod(int access, String name,
                            String descriptor, String signature, String[] exceptions) {
                        MethodVisitor mv = super.visitMethod(access, name, descriptor, signature, exceptions);
                        return new MethodVisitor(Opcodes.ASM8, mv) {
                            @Override
                            public void visitMethodInsn(int opcode, String owner, String name,
                                    String descriptor, boolean isInterface) {
                                if (opcode == Opcodes.INVOKESTATIC
                                        && COMPONENT.equals(owner)
                                        && FACTORIES.contains(name)) {
                                    int close = descriptor.lastIndexOf(')');
                                    if (close >= 0 && descriptor.substring(close + 1)
                                            .equals("Lnet/minecraft/network/chat/Component;")) {
                                        descriptor = descriptor.substring(0, close + 1) + MUTABLE;
                                        isInterface = true;
                                        repaired[0]++;
                                    }
                                }
                                super.visitMethodInsn(opcode, owner, name, descriptor, isInterface);
                            }
                        };
                    }
                };
                reader.accept(visitor, 0);
                if (repaired[0] > 0) {
                    Files.write(p, writer.toByteArray());
                    changed++;
                    calls += repaired[0];
                    System.out.println("PATCHED " + dir.relativize(p) + " calls=" + repaired[0]);
                }
            }
        }
        System.out.printf("Scan: %d classes; patched %d classes, %d calls%n", files, changed, calls);
        if (calls == 0)
            throw new IllegalStateException("No broken Component factory references were found");
    }
}
