import java.nio.file.*;
import jdk.internal.org.objectweb.asm.*;
import jdk.internal.org.objectweb.asm.tree.*;

/** Patch precompiled Alpha 48.1 classes made against incorrect Minecraft API stubs.
 * Minecraft 1.21.1 Fluids.WATER is FlowingFluid, and getSource(boolean) is declared
 * by FlowingFluid rather than Fluid. Use real NeoForge APIs for normal builds.
 */
public final class PatchFluidLinkage {
    static final String FLUIDS = "net/minecraft/world/level/material/Fluids";
    static final String FLUID = "net/minecraft/world/level/material/Fluid";
    static final String FLOWING = "net/minecraft/world/level/material/FlowingFluid";
    static final String STATE = "(Z)Lnet/minecraft/world/level/material/FluidState;";
    public static void main(String[] argv) throws Exception {
        if (argv.length != 1) throw new IllegalArgumentException("Expected build/pack directory");
        Path dir = Path.of(argv[0]).resolve("com/glaziola/pixelmonrejuvenated");
        int fields = 0, methods = 0, modified = 0;
        try (var paths = Files.walk(dir)) {
            for (Path path : (Iterable<Path>) paths.filter(f -> f.toString().endsWith(".class"))::iterator) {
                ClassNode c = new ClassNode();
                new ClassReader(Files.readAllBytes(path)).accept(c, 0);
                int fc = 0, mc = 0;
                for (MethodNode method : c.methods) {
                    for (AbstractInsnNode ins = method.instructions.getFirst();
                         ins != null; ins = ins.getNext()) {
                        if (ins instanceof FieldInsnNode n && n.getOpcode() == Opcodes.GETSTATIC
                            && n.owner.equals(FLUIDS) && n.name.equals("WATER")
                            && n.desc.equals("L" + FLUID + ";")) {
                            n.desc = "L" + FLOWING + ";"; fc++;
                        }
                        if (ins instanceof MethodInsnNode n && n.getOpcode() == Opcodes.INVOKEVIRTUAL
                            && n.owner.equals(FLUID) && n.name.equals("getSource") && n.desc.equals(STATE)) {
                            n.owner = FLOWING; mc++;
                        }
                    }
                }
                if (fc + mc != 0) {
                    ClassWriter w = new ClassWriter(0); c.accept(w);
                    Files.write(path, w.toByteArray());
                    modified++; fields += fc; methods += mc;
                    System.out.println(path.getFileName() + ": " + fc + " fields, " + mc + " methods");
                }
            }
        }
        if (modified != 1 || fields != 4 || methods != 1) {
            throw new IllegalStateException("Incorrect input build: patched " + modified
                + " classes, " + fields + " fields, " + methods + " methods");
        }
        System.out.println("Patched 5 fluid linkage references.");
    }
}
