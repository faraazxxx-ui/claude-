import { NodeSDK } from "@opentelemetry/sdk-node";
import { LangfuseSpanProcessor } from "@langfuse/otel";
import { LangfuseClient } from "@langfuse/client";
import { maskLangfusePayload } from "./events.ts";

let sdk: NodeSDK | null = null;
let client: LangfuseClient | null = null;
let started = false;

export function isTracingConfigured(): boolean {
  return Boolean(process.env.LANGFUSE_PUBLIC_KEY && process.env.LANGFUSE_SECRET_KEY);
}

export function getTracingEnvironment(): string {
  return process.env.LANGFUSE_TRACING_ENVIRONMENT ?? "development";
}

export function getLangfuseClient(): LangfuseClient | null {
  if (!isTracingConfigured()) {
    return null;
  }
  if (!client) {
    client = new LangfuseClient();
  }
  return client;
}

export function ensureTracingStarted(): boolean {
  if (!isTracingConfigured()) {
    return false;
  }
  if (started) {
    return true;
  }

  sdk = new NodeSDK({
    spanProcessors: [
      new LangfuseSpanProcessor({
        mask: maskLangfusePayload,
        environment: getTracingEnvironment(),
      }),
    ],
  });
  sdk.start();
  started = true;
  return true;
}

export async function shutdownTracing(): Promise<void> {
  const activeClient = client;
  if (activeClient) {
    await activeClient.flush();
  }
  if (sdk) {
    await sdk.shutdown();
    sdk = null;
  }
  started = false;
}
