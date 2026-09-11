import type { IncomingMessage, ServerResponse } from "node:http";
import type { Plugin } from "vite";
import { parseObservabilityEvent } from "./events.ts";
import { ensureTracingStarted } from "./instrumentation.ts";
import { handleObservabilityEvent } from "./observability.ts";

async function readJsonBody(req: IncomingMessage): Promise<unknown> {
  const chunks: Buffer[] = [];
  for await (const chunk of req) {
    chunks.push(typeof chunk === "string" ? Buffer.from(chunk) : chunk);
  }
  const raw = Buffer.concat(chunks).toString("utf8");
  if (raw.length === 0) {
    return {};
  }
  return JSON.parse(raw) as unknown;
}

function sendJson(res: ServerResponse, status: number, payload: unknown): void {
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json");
  res.end(JSON.stringify(payload));
}

function attachObservabilityMiddleware(middlewares: {
  use: (handler: (req: IncomingMessage, res: ServerResponse, next: () => void) => void) => void;
}): void {
  ensureTracingStarted();

  middlewares.use(async (req, res, next) => {
    if (req.url?.split("?")[0] !== "/api/observability/events") {
      next();
      return;
    }

    if (req.method !== "POST") {
      sendJson(res, 405, { error: "Method not allowed" });
      return;
    }

    try {
      const body = await readJsonBody(req);
      const event = parseObservabilityEvent(body);
      const result = await handleObservabilityEvent(event);
      sendJson(res, 200, result);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown error";
      sendJson(res, 400, { error: message });
    }
  });
}

export function observabilityPlugin(): Plugin {
  return {
    name: "langfuse-observability",
    configureServer(server) {
      attachObservabilityMiddleware(server.middlewares);
    },
    configurePreviewServer(server) {
      attachObservabilityMiddleware(server.middlewares);
    },
  };
}
