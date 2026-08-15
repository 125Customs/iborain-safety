import type { Expression } from "@pixel-bot/protocol";

/** Animated round-face eyes — a stand-in for the GC9A01 LCD. */
export class Eyes {
  private expression: Expression = "neutral";
  private blinkPhase = 0;
  private t = 0;

  constructor(private readonly ctx: CanvasRenderingContext2D) {
    requestAnimationFrame(() => this.frame());
  }

  set(expression: Expression): void {
    this.expression = expression;
  }

  /** Degraded mode: socket down → sleepy face, per spec. */
  sleep(): void {
    this.expression = "sleepy";
  }

  private frame(): void {
    this.t += 1 / 60;
    // Occasional blink
    if (Math.random() < 0.005 && this.blinkPhase === 0) this.blinkPhase = 1;
    if (this.blinkPhase > 0) this.blinkPhase = this.blinkPhase >= 12 ? 0 : this.blinkPhase + 1;

    const c = this.ctx;
    const W = 320;
    c.clearRect(0, 0, W, W);
    c.fillStyle = "#10151c";
    c.beginPath();
    c.arc(W / 2, W / 2, W / 2, 0, Math.PI * 2);
    c.fill();

    const blink = this.blinkPhase > 0 ? Math.abs(Math.sin((this.blinkPhase / 12) * Math.PI)) : 0;
    const bob = Math.sin(this.t * 1.5) * 3;

    for (const side of [-1, 1] as const) {
      const x = W / 2 + side * 58;
      const y = W / 2 - 15 + bob;
      c.fillStyle = "#58a6ff";
      c.save();
      c.translate(x, y);
      const openness = 1 - blink;
      switch (this.expression) {
        case "happy":
          c.scale(1, 0.55 * openness + 0.05);
          c.beginPath();
          c.arc(0, 0, 34, Math.PI, 0);
          c.fill();
          break;
        case "sad":
          c.rotate(side * -0.35);
          c.scale(1, openness);
          c.beginPath();
          c.ellipse(0, 6, 26, 30, 0, 0, Math.PI * 2);
          c.fill();
          break;
        case "curious":
          c.scale(1, openness);
          c.beginPath();
          c.arc(0, side === 1 ? -6 : 4, side === 1 ? 38 : 26, 0, Math.PI * 2);
          c.fill();
          break;
        case "surprised":
          c.scale(1, openness);
          c.beginPath();
          c.arc(0, 0, 40, 0, Math.PI * 2);
          c.fill();
          c.fillStyle = "#10151c";
          c.beginPath();
          c.arc(0, 0, 14, 0, Math.PI * 2);
          c.fill();
          break;
        case "thinking":
          c.scale(1, 0.35 * openness + 0.05);
          c.beginPath();
          c.arc(Math.sin(this.t * 3) * 8, 0, 30, 0, Math.PI * 2);
          c.fill();
          break;
        case "sleepy":
          c.scale(1, 0.12);
          c.beginPath();
          c.arc(0, 0, 32, 0, Math.PI * 2);
          c.fill();
          break;
        default: // neutral
          c.scale(1, openness);
          c.beginPath();
          c.ellipse(0, 0, 28, 34, 0, 0, Math.PI * 2);
          c.fill();
      }
      c.restore();
    }

    if (this.expression === "sleepy") {
      c.fillStyle = "#8b949e";
      c.font = "20px ui-monospace";
      const zOffset = (this.t * 20) % 40;
      c.fillText("z", 225, 95 - zOffset / 2);
      c.fillText("Z", 245, 75 - zOffset / 3);
    }

    requestAnimationFrame(() => this.frame());
  }
}
