from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path
from PIL import Image

ICONS = {
    198: "iVBORw0KGgoAAAANSUhEUgAAAB4AAAAfCAYAAADwbH0HAAACnklEQVR4nLWXIXLrMBCGf3cKhXOBooyQkbF7gKKAHMCsZ8hoND5AkFkOEGAUZFYcZKQxygEaLK6CdPUkW+s4ee/9M5pR1rI+rbTadTL8SgjhqG+tzfCkaJ7xHGP7CxkvlwuoFUXhxhMuhZZlibIsI0dS9heChjqdTiiKwoUvz8GolWXJjrter7her5BSQgjhXsKHVVWhqioPb9vWL4BrdV2jrusJiADc4l/nvMnzHKfTyf/u+973m6bB+/s7691qtcJqtYpsEdham729vbnL5YLD4cAuIgVdr9fJsSEwtIXwV+AWaQTnoEqpaBIOOtbn56dfbAiPtvrj44OdQGvt+03TLIbmee77BDfG3MCpyB6LtlopFS0iFJ1tSnmeezjwe49DUVSPoUopKKXYieu6hjEmsjVNE8VGKJ9dUl6HZ0teNk3jz22szWYDKeVkceE5A8DX19efM6YAA253kDS+TuNrEaptW2w2GwBxZKdiIgouyqPGGO99VVU4HA7o+957RKLAWQIfa3LGY4XQMPGnoGRv2xbGmNndSWaucNtDG4BJAHFwbqwxBtbajPXYWpuFLbQrpdhoHc/BLXQ2V3M1eonXUkqcz2eCL6/1Qgi33+9d13Vuv99PqkxRFO77+5ttXdctKqsslKvLQgjXdd3T8MkZU41dr9dQSuF8PmfPfgrleR5dv1mwlNJXnrmzpCC7J601Ul5HYCGE2263dyf7F5p4TN7ObdN/AYfSWrNfnEVROK48LtHdby6tNZRSE7jWmk2bfw0meFihHlHf9xiGIflsstU0cElKvAcFgOPxmMxWEdham+12u8nLz0KHYWCvZDIxhEnkWQ3DgN1ux+ZmNiMJIZyUEtvt9qEFDMOA4/Hoyx837m4qfDjRY9m/zR8wC+IqG89h8QAAAABJRU5ErkJggg==",
    199: "iVBORw0KGgoAAAANSUhEUgAAAB4AAAAfCAYAAADwbH0HAAACc0lEQVR4nLWWMa6jMBCGf6ItLZcUSD5BqugV1DkAXY6QjvPQcQsOwAmQK05AhUvk3lu8jNfgsUPe7v4SEjLgb/7xjE2Bl5qmcQAwDEOBQKnxTySEcHRvrf0zT9M0bl1Xt66rC18KxymAT1XXtWuaxl80/6VpGte2LbTW0FonJ+j7HkIIR9cZl3Vdu7Isd+P3+x1CCPfr+MH9fgcABwBt20YTSinpNgm/Xq8AAIL2fQ8AeD6f/p0ITC+RtNa43W7JAJRSfuzoLqcdmAMcx0LQsixYlsWPGWNYeOh0HEdYawsPJgC9dHTOSSnl4aFSzgkKvByHUGOMvz8DpwBIXCCcvOMQyilV8eSa4F9fX1ngOI7OWltcuIdlWUZuu64LKzoSOeWC5zJ3CR+WZclCtdYYx3GX0qOUUt79NE27AKhuojXORaa1xuPx8L2ZEwUOANM0+bXetg3AfruM+jgF5So1dDXPs4f3fc+6DMWuMUG7rktCCUKy1hbzPMMYs+vblArg+zA4bo9d12EcR9pCkzLGYJ5n7+q4j3NugUSqu67DMAzFu8PAGINlWXaTp0As+HXWegidvbn2IVHhkJJnLwcOYeEEufYBELkVQjgppW8rAC4FZ4tLCOFyRQV8p/no1lpbbNvmdzIpZbTmJHaNpZQfHXFHuLUWAFzOeeT4TIqBOM1HUTbI+VHJPv7XOqb8v4HD5eIy+GOwUgpVVbGFU1XV2+XK7tU5BcUXwZVSb4uTBdOp8u7j8DT6VFGqw0rN/ZGcEX3P/Qqxa0ybwN/Aw++2bYtaL9mH4fb3Uy3LwkKz4BAO8C2RAwK801PgMIDT1JfeHY+/AeS8h3SaEoA0AAAAAElFTkSuQmCC",
}

def write_fallback(species_id: int, out_dir: Path) -> None:
    icon = Image.open(BytesIO(base64.b64decode(ICONS[species_id]))).convert("RGBA")
    icon = icon.resize((icon.width * 2, icon.height * 2), Image.Resampling.NEAREST)
    canvas = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
    canvas.alpha_composite(icon, ((80 - icon.width) // 2, (80 - icon.height) // 2))
    target = out_dir / f"{species_id:03d}.png"
    canvas.save(target, format="PNG", optimize=True)

    if canvas.getchannel("A").getbbox() is None:
        raise RuntimeError(f"Fallback front sprite {species_id} is still transparent")

if __name__ == "__main__":
    root = Path("pkvault-src/frontend/public/romhacks/uranium/front")
    root.mkdir(parents=True, exist_ok=True)
    for species_id in sorted(ICONS):
        write_fallback(species_id, root)
        print(f"Replaced transparent Uranium front sprite {species_id:03d}.png")
