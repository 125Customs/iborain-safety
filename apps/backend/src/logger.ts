import { pino } from "pino";

/**
 * Structured logs → stdout → Cloud Logging (Cloud Run ingests JSON lines natively).
 * `severity` mapping makes Cloud Logging levels work without an agent.
 */
export function createLogger(level: string) {
  return pino({
    level,
    messageKey: "message",
    formatters: {
      level(label) {
        const map: Record<string, string> = {
          trace: "DEBUG",
          debug: "DEBUG",
          info: "INFO",
          warn: "WARNING",
          error: "ERROR",
          fatal: "CRITICAL",
        };
        return { severity: map[label] ?? "DEFAULT" };
      },
    },
  });
}

export type Logger = ReturnType<typeof createLogger>;
