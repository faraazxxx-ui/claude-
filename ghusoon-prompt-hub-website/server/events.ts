import type { PromptData } from "../src/lib/promptData.ts";

export const APP_VERSION = "2.0.0";

export const TRACE_NAMES = {
  copyPrompt: "copy-prompt",
  viewPrompt: "view-prompt",
  searchPrompts: "search-prompts",
  ratePrompt: "rate-prompt",
} as const;

export const SCORE_NAMES = {
  userCopied: "user-copied",
  userThumbs: "user-thumbs",
} as const;

export type ObservabilityAction =
  | "copy-prompt"
  | "view-prompt"
  | "search-prompts"
  | "rate-prompt";

export interface CopyPromptEvent {
  action: "copy-prompt";
  promptId: number;
  sessionId: string;
}

export interface ViewPromptEvent {
  action: "view-prompt";
  promptId: number;
  sessionId: string;
}

export interface SearchPromptsEvent {
  action: "search-prompts";
  query: string;
  resultCount: number;
  sessionId: string;
}

export interface RatePromptEvent {
  action: "rate-prompt";
  promptId: number;
  sessionId: string;
  value: 0 | 1;
  comment?: string;
  traceId?: string;
}

export type ObservabilityEvent =
  | CopyPromptEvent
  | ViewPromptEvent
  | SearchPromptsEvent
  | RatePromptEvent;

export interface ObservabilityResult {
  traced: boolean;
  traceId: string | null;
  action: ObservabilityAction;
}

const SESSION_ID_PATTERN = /^[A-Za-z0-9:_-]{8,128}$/;

export function isObservabilityAction(value: unknown): value is ObservabilityAction {
  return (
    value === "copy-prompt" ||
    value === "view-prompt" ||
    value === "search-prompts" ||
    value === "rate-prompt"
  );
}

export function sanitizeSessionId(sessionId: unknown): string {
  if (typeof sessionId === "string" && SESSION_ID_PATTERN.test(sessionId)) {
    return sessionId;
  }
  return "anonymous-session";
}

export function sanitizeSearchQuery(query: unknown): string {
  if (typeof query !== "string") {
    return "";
  }
  return query.trim().slice(0, 80);
}

export function featureTags(
  category?: PromptData["category"],
  extra: string[] = [],
): string[] {
  const tags = ["feature:prompt-hub", ...extra];
  if (category) {
    tags.push(`platform:${category}`);
  }
  return tags;
}

export function parseObservabilityEvent(body: unknown): ObservabilityEvent {
  if (typeof body !== "object" || body === null) {
    throw new Error("Observability event must be an object");
  }

  const record = body as Record<string, unknown>;
  const action = record.action;
  if (!isObservabilityAction(action)) {
    throw new Error("Unknown observability action");
  }

  const sessionId = sanitizeSessionId(record.sessionId);

  if (action === "search-prompts") {
    const resultCount =
      typeof record.resultCount === "number" && Number.isFinite(record.resultCount)
        ? Math.max(0, Math.floor(record.resultCount))
        : 0;
    return {
      action,
      sessionId,
      query: sanitizeSearchQuery(record.query),
      resultCount,
    };
  }

  const promptId =
    typeof record.promptId === "number" && Number.isInteger(record.promptId)
      ? record.promptId
      : NaN;
  if (!Number.isInteger(promptId) || promptId < 1) {
    throw new Error("promptId must be a positive integer");
  }

  if (action === "rate-prompt") {
    const value = record.value;
    if (value !== 0 && value !== 1) {
      throw new Error("rate-prompt value must be 0 or 1");
    }
    const comment =
      typeof record.comment === "string" ? record.comment.slice(0, 200) : undefined;
    const traceId =
      typeof record.traceId === "string" && record.traceId.length > 0
        ? record.traceId
        : undefined;
    return { action, sessionId, promptId, value, comment, traceId };
  }

  return { action, sessionId, promptId };
}

export function maskLangfusePayload({ data }: { data: string }): string {
  return data
    .replace(/\b[\w.+-]+@[\w.-]+\.\w+\b/g, "[REDACTED_EMAIL]")
    .replace(/\b\d{3}[-.\s]?\d{2}[-.\s]?\d{4}\b/g, "[REDACTED_SSN]")
    .replace(/\b(?:\d[ -]*?){13,19}\b/g, "[REDACTED_CARD]");
}
