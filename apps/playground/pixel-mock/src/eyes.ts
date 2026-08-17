import type { ThreatLevel, DeterrenceAction } from "@pixel-bot/protocol";

/** Sentry Threat Beacon & Active Radar — software mock for the GC9A01 LCD. */
export class SentryBeacon {
  private threatLevel: ThreatLevel = "CLEAR";
  private deterrence: DeterrenceAction = "IDLE_BEACON";
  private t = 0;

  constructor(private readonly ctx: CanvasRenderingContext2D) {
    requestAnimationFrame(() => this.frame());
  }

  setState(threatLevel: ThreatLevel, deterrence: DeterrenceAction): void {
    this.threatLevel = threatLevel;
    this.deterrence = deterrence;
  }

  sleep(): void {
    this.threatLevel = "CLEAR";
    this.deterrence = "IDLE_BEACON";
  }

  private frame(): void {
    this.t += 1 / 60;
    const c = this.ctx;
    const W = 300;
    c.clearRect(0, 0, W, W);

    // Dark base
    c.fillStyle = "#080c14";
    c.beginPath();
    c.arc(W / 2, W / 2, W / 2, 0, Math.PI * 2);
    c.fill();

    // Radar sweep
    const sweepAngle = (this.t * 2) % (Math.PI * 2);

    if (this.threatLevel === "HOTLIST_MATCH" || this.threatLevel === "EMERGENCY") {
      // Red/Blue Emergency Police Deterrence Strobe
      const isRed = Math.floor(this.t * 8) % 2 === 0;
      c.fillStyle = isRed ? "rgba(220, 38, 38, 0.25)" : "rgba(37, 99, 235, 0.25)";
      c.beginPath();
      c.arc(W / 2, W / 2, W / 2 - 10, 0, Math.PI * 2);
      c.fill();

      c.strokeStyle = isRed ? "#ef4444" : "#3b82f6";
      c.lineWidth = 6;
      c.beginPath();
      c.arc(W / 2, W / 2, W / 2 - 15, 0, Math.PI * 2);
      c.stroke();

      // Threat Warning Icon
      c.fillStyle = "#f87171";
      c.font = "bold 24px monospace";
      c.textAlign = "center";
      c.fillText("HOTLIST THREAT", W / 2, W / 2 - 10);
      c.font = "14px monospace";
      c.fillStyle = "#ffffff";
      c.fillText("ACOUSTIC ALARM", W / 2, W / 2 + 20);
    } else if (this.threatLevel === "SUSPICIOUS") {
      // Amber Warning Beacon
      c.strokeStyle = "#f59e0b";
      c.lineWidth = 4;
      c.beginPath();
      c.arc(W / 2, W / 2, W / 2 - 20, 0, Math.PI * 2);
      c.stroke();

      c.fillStyle = "#fbbf24";
      c.font = "bold 18px monospace";
      c.textAlign = "center";
      c.fillText("SUSPICIOUS TRANSIT", W / 2, W / 2);
    } else {
      // Normal Active Sentry Radar (Green/Cyan)
      c.strokeStyle = "rgba(16, 185, 129, 0.3)";
      c.lineWidth = 2;
      for (const r of [40, 80, 120]) {
        c.beginPath();
        c.arc(W / 2, W / 2, r, 0, Math.PI * 2);
        c.stroke();
      }

      // Radar Crosshairs
      c.strokeStyle = "rgba(16, 185, 129, 0.4)";
      c.beginPath();
      c.moveTo(W / 2, 20); c.lineTo(W / 2, W - 20);
      c.moveTo(20, W / 2); c.lineTo(W - 20, W / 2);
      c.stroke();

      // Sweeping Beam
      c.fillStyle = "rgba(16, 185, 129, 0.15)";
      c.beginPath();
      c.moveTo(W / 2, W / 2);
      c.arc(W / 2, W / 2, 130, sweepAngle, sweepAngle + 0.4);
      c.closePath();
      c.fill();

      // Center Shield Core
      c.fillStyle = "#10b981";
      c.beginPath();
      c.arc(W / 2, W / 2, 8, 0, Math.PI * 2);
      c.fill();

      c.fillStyle = "#6ee7b7";
      c.font = "bold 13px monospace";
      c.textAlign = "center";
      c.fillText("BOMASAFETY SENTRY", W / 2, W / 2 + 35);
      c.fillStyle = "#9ca3af";
      c.font = "11px monospace";
      c.fillText("ACTIVE PATROL", W / 2, W / 2 + 55);
    }

    requestAnimationFrame(() => this.frame());
  }
}
