import * as Sentry from "@sentry/node";
import { createServer } from "node:http";
import { WebSocketServer } from "ws";
import { authenticate } from "./auth.js";
import { loadConfig } from "./config.js";
import { CostGuard } from "./cost-guard.js";
import { createLogger } from "./logger.js";
import { DeviceSession } from "./session.js";

const config = loadConfig();
const log = createLogger(config.LOG_LEVEL);

if (config.SENTRY_DSN) {
  // Crash reporting only — no tracing, no dashboards, free tier.
  Sentry.init({ dsn: config.SENTRY_DSN });
}

const costGuard = new CostGuard(config.DAILY_BUDGET_USD, log);

/**
 * Session state lives in-process, keyed by deviceId.
 * Safe because Cloud Run runs with --session-affinity and min-instances=1.
 * // SCALE-SEAM: externalize session state (Redis/Firestore) when we shard
 * // across instances; DeviceSession is already self-contained to make that
 * // a move, not a rewrite.
 */
const sessions = new Map<string, DeviceSession>();

const httpServer = createServer((req, res) => {
  if (req.url === "/healthz") {
    res.writeHead(200, { "content-type": "application/json" });
    res.end(JSON.stringify({ ok: true, sessions: sessions.size, mode: config.MODE }));
    return;
  }
  res.writeHead(404);
  res.end();
});

const wss = new WebSocketServer({ noServer: true, maxPayload: 512 * 1024 });

httpServer.on("upgrade", (req, socket, head) => {
  const auth = authenticate(req, config.DEVICE_TOKENS);
  if (!auth) {
    log.warn({ event: "auth_rejected", url: req.url });
    socket.write("HTTP/1.1 401 Unauthorized\r\n\r\n");
    socket.destroy();
    return;
  }
  if (!costGuard.allowConnect(auth.deviceId)) {
    log.warn({ event: "connect_rate_limited", deviceId: auth.deviceId });
    socket.write("HTTP/1.1 429 Too Many Requests\r\n\r\n");
    socket.destroy();
    return;
  }
  if (!costGuard.withinBudget(auth.deviceId)) {
    log.warn({ event: "connect_budget_exhausted", deviceId: auth.deviceId });
    socket.write("HTTP/1.1 402 Payment Required\r\n\r\n");
    socket.destroy();
    return;
  }
  wss.handleUpgrade(req, socket, head, (ws) => {
    // One live session per device: a new connection replaces the old one
    // (robot rebooted / Wi-Fi flapped and the old socket hasn't timed out yet).
    const existing = sessions.get(auth.deviceId);
    if (existing) {
      log.info({ event: "session_replaced", deviceId: auth.deviceId });
    }
    const session = new DeviceSession(ws, auth.deviceId, config, costGuard, log, (s) => {
      if (sessions.get(s.deviceId) === s) sessions.delete(s.deviceId);
    });
    sessions.set(auth.deviceId, session);
  });
});

httpServer.listen(config.PORT, () => {
  log.info({ event: "server_listening", port: config.PORT, mode: config.MODE });
});

function shutdown(): void {
  log.info({ event: "server_shutdown" });
  wss.close();
  httpServer.close(() => process.exit(0));
  setTimeout(() => process.exit(0), 3000).unref();
}
process.on("SIGTERM", shutdown);
process.on("SIGINT", shutdown);
