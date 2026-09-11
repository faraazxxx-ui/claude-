import { describe, expect, it } from "vitest";
import { getPromptMetadata, searchPromptMetadata } from "../server/catalog.ts";
import {
  SCORE_NAMES,
  TRACE_NAMES,
  featureTags,
  maskLangfusePayload,
  parseObservabilityEvent,
  sanitizeSearchQuery,
  sanitizeSessionId,
} from "../server/events.ts";

describe("observability event parsing", () => {
  it("accepts a copy-prompt event and keeps a valid session id", () => {
    const event = parseObservabilityEvent({
      action: "copy-prompt",
      promptId: 1,
      sessionId: "session_abc-123",
    });

    expect(event).toEqual({
      action: "copy-prompt",
      promptId: 1,
      sessionId: "session_abc-123",
    });
  });

  it("rejects unknown actions", () => {
    expect(() =>
      parseObservabilityEvent({ action: "trace-1", promptId: 1, sessionId: "session_abc" }),
    ).toThrow("Unknown observability action");
  });

  it("truncates search queries so raw user text stays low-cardinality", () => {
    expect(sanitizeSearchQuery("  olive oil ".repeat(20)).length).toBeLessThanOrEqual(80);
  });

  it("falls back when the session id is missing", () => {
    expect(sanitizeSessionId(undefined)).toBe("anonymous-session");
  });
});

describe("catalog metadata", () => {
  it("returns prompt metadata without the prompt body", () => {
    const metadata = getPromptMetadata(1);
    expect(metadata).not.toBeNull();
    expect(metadata?.platform).toBe("Manus AI");
    expect(metadata?.charCount).toBeGreaterThan(0);
    expect(JSON.stringify(metadata)).not.toMatch(/SSN|EIN|severe back pain/i);
  });

  it("searches by platform without exposing prompt text", () => {
    const results = searchPromptMetadata("claude");
    expect(results.length).toBeGreaterThan(0);
    for (const result of results) {
      expect(result).not.toHaveProperty("prompt");
    }
  });
});

describe("trace naming and masking", () => {
  it("uses stable verb-first trace and score names", () => {
    expect(TRACE_NAMES.copyPrompt).toBe("copy-prompt");
    expect(TRACE_NAMES.viewPrompt).toBe("view-prompt");
    expect(TRACE_NAMES.searchPrompts).toBe("search-prompts");
    expect(SCORE_NAMES.userCopied).toBe("user-copied");
    expect(SCORE_NAMES.userThumbs).toBe("user-thumbs");
  });

  it("tags traces by feature and platform", () => {
    expect(featureTags("anthropic", ["action:copy"])).toEqual([
      "feature:prompt-hub",
      "action:copy",
      "platform:anthropic",
    ]);
  });

  it("redacts emails and card numbers before export", () => {
    const masked = maskLangfusePayload({
      data: JSON.stringify({
        email: "founder@example.com",
        card: "4111 1111 1111 1111",
      }),
    });
    expect(masked).toContain("[REDACTED_EMAIL]");
    expect(masked).toContain("[REDACTED_CARD]");
    expect(masked).not.toContain("founder@example.com");
  });
});
