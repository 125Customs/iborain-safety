import { z } from "zod";

const EnvSchema = z.object({
  PORT: z.coerce.number().int().default(8080),
  MODE: z.enum(["echo", "gemini"]).default("echo"),
  GEMINI_API_KEY: z.string().default(""),
  GEMINI_MODEL: z
    .string()
    .default("gemini-2.5-flash-native-audio-preview-12-2025"),
  GEMINI_VOICE: z.string().default("Puck"),
  DEVICE_TOKENS: z
    .string()
    .default('{"dev-local":"local-secret"}')
    .transform((s, ctx) => {
      try {
        return z.record(z.string(), z.string()).parse(JSON.parse(s));
      } catch {
        ctx.addIssue({ code: "custom", message: "DEVICE_TOKENS must be a JSON string map" });
        return z.NEVER;
      }
    }),
  SESSION_MAX_MS: z.coerce.number().int().default(10 * 60 * 1000),
  IDLE_TIMEOUT_MS: z.coerce.number().int().default(60 * 1000),
  DAILY_BUDGET_USD: z.coerce.number().default(5),
  HEARTBEAT_INTERVAL_MS: z.coerce.number().int().default(10_000),
  HEARTBEAT_TIMEOUT_MS: z.coerce.number().int().default(30_000),
  SENTRY_DSN: z.string().default(""),
  LOG_LEVEL: z.string().default("info"),
});

export type Config = z.infer<typeof EnvSchema>;

export function loadConfig(): Config {
  const parsed = EnvSchema.safeParse(process.env);
  if (!parsed.success) {
    // eslint-disable-next-line no-console
    console.error("Invalid environment:", parsed.error.flatten().fieldErrors);
    process.exit(1);
  }
  if (parsed.data.MODE === "gemini" && !parsed.data.GEMINI_API_KEY) {
    // eslint-disable-next-line no-console
    console.error("MODE=gemini requires GEMINI_API_KEY");
    process.exit(1);
  }
  return parsed.data;
}
