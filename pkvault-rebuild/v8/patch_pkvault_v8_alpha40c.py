from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
path = root / "frontend/src/quests/quest-toast.tsx"
text = path.read_text(encoding="utf-8")

old = """  React.useEffect(() => {
    if (current || queue.length === 0)
      return;
    setCurrent(queue[0]);
    setQueue(old => old.slice(1));
  }, [current, queue]);
"""

new = """  React.useEffect(() => {
    if (current || queue.length === 0)
      return;

    const timer = window.setTimeout(() => {
      setCurrent(queue[0]);
      setQueue(old => old.slice(1));
    }, 0);

    return () => window.clearTimeout(timer);
  }, [current, queue]);
"""

if old not in text:
    raise RuntimeError("alpha40c quest-toast queue anchor missing")

path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("PKVault V8 alpha40c quest toast queue lint fix applied")
