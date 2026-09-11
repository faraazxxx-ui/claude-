import { LangfuseBrowserClient } from "@langfuse/browser";
import { getHubSessionId } from "./session";

export type ClientObservabilityAction =
  | "copy-prompt"
  | "view-prompt"
  | "search-prompts"
  | "rate-prompt";

export interface ObservabilityResponse {
  traced: boolean;
  traceId: string | null;
  action: ClientObservabilityAction;
}

interface CopyPromptPayload {
  action: "copy-prompt";
  promptId: number;
}

interface ViewPromptPayload {
  action: "view-prompt";
  promptId: number;
}

interface SearchPromptsPayload {
  action: "search-prompts";
  query: string;
  resultCount: number;
}

interface RatePromptPayload {
  action: "rate-prompt";
  promptId: number;
  value: 0 | 1;
  comment?: string;
  traceId?: string;
}

export type ObservabilityPayload =
  | CopyPromptPayload
  | ViewPromptPayload
  | SearchPromptsPayload
  | RatePromptPayload;

let browserClient: LangfuseBrowserClient | null | undefined;

function getBrowserClient(): LangfuseBrowserClient | null {
  if (browserClient !== undefined) {
    return browserClient;
  }

  const publicKey = import.meta.env.VITE_LANGFUSE_PUBLIC_KEY;
  if (!publicKey) {
    browserClient = null;
    return null;
  }

  browserClient = new LangfuseBrowserClient({
    publicKey,
    baseUrl: import.meta.env.VITE_LANGFUSE_BASE_URL,
  });
  return browserClient;
}

export async function reportObservabilityEvent(
  payload: ObservabilityPayload,
): Promise<ObservabilityResponse | null> {
  try {
    const response = await fetch("/api/observability/events", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ...payload,
        sessionId: getHubSessionId(),
      }),
    });

    if (!response.ok) {
      return null;
    }

    return (await response.json()) as ObservabilityResponse;
  } catch {
    return null;
  }
}

export async function reportBrowserScore(
  traceId: string,
  value: 0 | 1,
  comment?: string,
): Promise<void> {
  const client = getBrowserClient();
  if (!client) {
    return;
  }

  await client.score({
    id: `user-thumbs-${traceId}`,
    traceId,
    name: "user-thumbs",
    value,
    dataType: "BOOLEAN",
    comment,
  });
}
