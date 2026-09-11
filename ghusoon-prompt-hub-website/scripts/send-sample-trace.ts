import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { parseObservabilityEvent } from "../server/events.ts";
import { ensureTracingStarted, shutdownTracing } from "../server/instrumentation.ts";
import { handleObservabilityEvent } from "../server/observability.ts";

function loadLocalEnv(): void {
  const envPath = resolve(process.cwd(), ".env");
  if (!existsSync(envPath)) {
    return;
  }

  for (const line of readFileSync(envPath, "utf8").split("\n")) {
    const trimmed = line.trim();
    if (trimmed.length === 0 || trimmed.startsWith("#") || !trimmed.includes("=")) {
      continue;
    }
    const separator = trimmed.indexOf("=");
    const key = trimmed.slice(0, separator).trim();
    const value = trimmed.slice(separator + 1).trim().replace(/^['"]|['"]$/g, "");
    if (key && process.env[key] === undefined) {
      process.env[key] = value;
    }
  }
}

loadLocalEnv();

async function main(): Promise<void> {
  const configured = ensureTracingStarted();
  if (!configured) {
    console.log(
      [
        "Langfuse keys are not set, so no live trace was sent.",
        "Add LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, and LANGFUSE_BASE_URL",
        "to ghusoon-prompt-hub-website/.env (see .env.example), then rerun:",
        "  npm run trace:sample",
      ].join("\n"),
    );
    return;
  }

  const event = parseObservabilityEvent({
    action: "copy-prompt",
    promptId: 1,
    sessionId: "session_sample-trace",
  });
  const result = await handleObservabilityEvent(event);
  await shutdownTracing();

  console.log(
    JSON.stringify(
      {
        ...result,
        hint: "Open the Langfuse Traces view and filter by name copy-prompt.",
      },
      null,
      2,
    ),
  );
}

void main().catch(async (error: unknown) => {
  await shutdownTracing().catch(() => undefined);
  console.error(error instanceof Error ? error.message : error);
  process.exitCode = 1;
});
