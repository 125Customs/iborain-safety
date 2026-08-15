import type { Logger } from "./logger.js";

/**
 * Cost controls — our biggest COGS is Gemini Live session time.
 * In-memory per-device accounting: token bucket for connect attempts +
 * daily USD budget kill-switch fed by usageMetadata token counts.
 *
 * // SCALE-SEAM: swap for Upstash Redis when we run >1 instance region-wide.
 */

/** Rough Live API pricing (USD per 1M tokens). Adjust from the pricing page. */
const PRICE_PER_M = {
  audioIn: 3.0,
  videoIn: 3.0,
  textIn: 0.5,
  audioOut: 12.0,
  textOut: 2.0,
} as const;

interface DeviceLedger {
  day: string; // YYYY-MM-DD (UTC)
  usd: number;
  bucketTokens: number;
  bucketRefillAt: number;
}

const BUCKET_CAPACITY = 10; // connect attempts
const BUCKET_REFILL_MS = 60_000; // 1 token / minute

export class CostGuard {
  private readonly ledgers = new Map<string, DeviceLedger>();

  constructor(
    private readonly dailyBudgetUsd: number,
    private readonly log: Logger,
  ) {}

  private ledger(deviceId: string): DeviceLedger {
    const today = new Date().toISOString().slice(0, 10);
    let l = this.ledgers.get(deviceId);
    if (!l || l.day !== today) {
      l = { day: today, usd: 0, bucketTokens: BUCKET_CAPACITY, bucketRefillAt: Date.now() };
      this.ledgers.set(deviceId, l);
    }
    return l;
  }

  /** Token-bucket gate on new connections (reconnect storms, runaway firmware). */
  allowConnect(deviceId: string): boolean {
    const l = this.ledger(deviceId);
    const now = Date.now();
    const refill = Math.floor((now - l.bucketRefillAt) / BUCKET_REFILL_MS);
    if (refill > 0) {
      l.bucketTokens = Math.min(BUCKET_CAPACITY, l.bucketTokens + refill);
      l.bucketRefillAt = now;
    }
    if (l.bucketTokens <= 0) return false;
    l.bucketTokens -= 1;
    return true;
  }

  /** Daily budget kill-switch. */
  withinBudget(deviceId: string): boolean {
    return this.ledger(deviceId).usd < this.dailyBudgetUsd;
  }

  budgetRemainingUsd(deviceId: string): number {
    return Math.max(0, this.dailyBudgetUsd - this.ledger(deviceId).usd);
  }

  /** Feed from Gemini usageMetadata modality token counts. */
  recordUsage(
    deviceId: string,
    counts: { audioIn?: number; videoIn?: number; textIn?: number; audioOut?: number; textOut?: number },
  ): void {
    const usd =
      ((counts.audioIn ?? 0) * PRICE_PER_M.audioIn +
        (counts.videoIn ?? 0) * PRICE_PER_M.videoIn +
        (counts.textIn ?? 0) * PRICE_PER_M.textIn +
        (counts.audioOut ?? 0) * PRICE_PER_M.audioOut +
        (counts.textOut ?? 0) * PRICE_PER_M.textOut) /
      1_000_000;
    const l = this.ledger(deviceId);
    l.usd += usd;
    this.log.debug({ event: "cost_usage", deviceId, usdDelta: usd, usdToday: l.usd });
  }

  usdToday(deviceId: string): number {
    return this.ledger(deviceId).usd;
  }
}
