import { timingSafeEqual } from "node:crypto";
import type { IncomingMessage } from "node:http";

/**
 * Minimum-viable device auth: static per-device bearer tokens.
 * Token via `Authorization: Bearer <token>` header or `?token=` query param
 * (ESP32 WS clients handle query params more easily than headers).
 *
 * // SCALE-SEAM: replace with ephemeral tokens + device provisioning service.
 */
export function authenticate(
  req: IncomingMessage,
  tokens: Record<string, string>,
): { deviceId: string } | null {
  const url = new URL(req.url ?? "/", "http://localhost");
  const deviceId = url.searchParams.get("device");
  if (!deviceId) return null;

  const header = req.headers.authorization;
  const presented =
    header?.startsWith("Bearer ") === true
      ? header.slice("Bearer ".length)
      : (url.searchParams.get("token") ?? "");

  const expected = tokens[deviceId];
  if (expected === undefined || presented.length === 0) return null;

  const a = Buffer.from(presented);
  const b = Buffer.from(expected);
  if (a.length !== b.length || !timingSafeEqual(a, b)) return null;
  return { deviceId };
}
