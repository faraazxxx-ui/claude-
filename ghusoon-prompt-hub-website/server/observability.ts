import {
  getActiveTraceId,
  propagateAttributes,
  startActiveObservation,
} from "@langfuse/tracing";
import { getPromptMetadata, searchPromptMetadata } from "./catalog.ts";
import {
  APP_VERSION,
  SCORE_NAMES,
  TRACE_NAMES,
  type ObservabilityEvent,
  type ObservabilityResult,
  featureTags,
} from "./events.ts";
import { getLangfuseClient, isTracingConfigured } from "./instrumentation.ts";

async function scoreTrace(
  traceId: string | null,
  name: string,
  value: number,
  comment?: string,
): Promise<void> {
  const client = getLangfuseClient();
  if (!client || !traceId) {
    return;
  }

  client.score.create({
    traceId,
    name,
    value,
    dataType: "BOOLEAN",
    comment,
  });
}

export async function handleObservabilityEvent(
  event: ObservabilityEvent,
): Promise<ObservabilityResult> {
  if (!isTracingConfigured()) {
    return { traced: false, traceId: null, action: event.action };
  }

  switch (event.action) {
    case "copy-prompt":
      return recordCopyPrompt(event.promptId, event.sessionId);
    case "view-prompt":
      return recordViewPrompt(event.promptId, event.sessionId);
    case "search-prompts":
      return recordSearchPrompts(event.query, event.resultCount, event.sessionId);
    case "rate-prompt":
      return recordRatePrompt(event);
    default: {
      const exhaustive: never = event;
      throw new Error(`Unhandled observability action: ${JSON.stringify(exhaustive)}`);
    }
  }
}

async function recordCopyPrompt(
  promptId: number,
  sessionId: string,
): Promise<ObservabilityResult> {
  const metadata = getPromptMetadata(promptId);
  if (!metadata) {
    throw new Error(`Prompt ${promptId} not found`);
  }

  let traceId: string | null = null;

  await startActiveObservation(TRACE_NAMES.copyPrompt, async (span) => {
    await propagateAttributes(
      {
        sessionId,
        version: APP_VERSION,
        tags: featureTags(metadata.category, ["action:copy"]),
        metadata: {
          app: "ghusoon-prompt-hub",
          platform: metadata.platform,
          severity: metadata.severity,
        },
        traceName: TRACE_NAMES.copyPrompt,
      },
      async () => {
        span.update({
          input: {
            promptId: metadata.id,
            platform: metadata.platform,
            category: metadata.category,
          },
        });

        await startActiveObservation(
          "retrieve-prompt",
          async (retriever) => {
            retriever.update({
              input: { promptId: metadata.id },
              output: {
                platform: metadata.platform,
                category: metadata.category,
                severity: metadata.severity,
                charCount: metadata.charCount,
              },
            });
          },
          { asType: "retriever" },
        );

        await startActiveObservation(
          "copy-to-clipboard",
          async (tool) => {
            tool.update({
              input: { promptId: metadata.id, platform: metadata.platform },
              output: { copied: true },
            });
          },
          { asType: "tool" },
        );

        span.update({
          output: { copied: true, platform: metadata.platform },
        });
        traceId = getActiveTraceId() ?? null;
      },
    );
  });

  await scoreTrace(traceId, SCORE_NAMES.userCopied, 1, "User copied prompt to clipboard");
  return { traced: true, traceId, action: "copy-prompt" };
}

async function recordViewPrompt(
  promptId: number,
  sessionId: string,
): Promise<ObservabilityResult> {
  const metadata = getPromptMetadata(promptId);
  if (!metadata) {
    throw new Error(`Prompt ${promptId} not found`);
  }

  let traceId: string | null = null;

  await startActiveObservation(TRACE_NAMES.viewPrompt, async (span) => {
    await propagateAttributes(
      {
        sessionId,
        version: APP_VERSION,
        tags: featureTags(metadata.category, ["action:view"]),
        metadata: {
          app: "ghusoon-prompt-hub",
          platform: metadata.platform,
          severity: metadata.severity,
        },
        traceName: TRACE_NAMES.viewPrompt,
      },
      async () => {
        span.update({
          input: {
            promptId: metadata.id,
            platform: metadata.platform,
            category: metadata.category,
          },
        });

        await startActiveObservation(
          "retrieve-prompt",
          async (retriever) => {
            retriever.update({
              input: { promptId: metadata.id },
              output: {
                platform: metadata.platform,
                category: metadata.category,
                charCount: metadata.charCount,
                redTeamFixCount: metadata.redTeamFixCount,
              },
            });
          },
          { asType: "retriever" },
        );

        span.update({
          output: { expanded: true, charCount: metadata.charCount },
        });
        traceId = getActiveTraceId() ?? null;
      },
    );
  });

  return { traced: true, traceId, action: "view-prompt" };
}

async function recordSearchPrompts(
  query: string,
  resultCount: number,
  sessionId: string,
): Promise<ObservabilityResult> {
  const matches = searchPromptMetadata(query);
  let traceId: string | null = null;

  await startActiveObservation(
    TRACE_NAMES.searchPrompts,
    async (retriever) => {
      await propagateAttributes(
        {
          sessionId,
          version: APP_VERSION,
          tags: featureTags(undefined, ["action:search"]),
          metadata: { app: "ghusoon-prompt-hub" },
          traceName: TRACE_NAMES.searchPrompts,
        },
        async () => {
          retriever.update({
            input: { query },
            output: {
              resultCount,
              matchedIds: matches.map((item) => item.id),
            },
          });
          traceId = getActiveTraceId() ?? null;
        },
      );
    },
    { asType: "retriever" },
  );

  return { traced: true, traceId, action: "search-prompts" };
}

async function recordRatePrompt(
  event: Extract<ObservabilityEvent, { action: "rate-prompt" }>,
): Promise<ObservabilityResult> {
  const metadata = getPromptMetadata(event.promptId);
  if (!metadata) {
    throw new Error(`Prompt ${event.promptId} not found`);
  }

  let traceId = event.traceId ?? null;

  if (!traceId) {
    await startActiveObservation(TRACE_NAMES.ratePrompt, async (span) => {
      await propagateAttributes(
        {
          sessionId: event.sessionId,
          version: APP_VERSION,
          tags: featureTags(metadata.category, ["action:rate"]),
          metadata: {
            app: "ghusoon-prompt-hub",
            platform: metadata.platform,
          },
          traceName: TRACE_NAMES.ratePrompt,
        },
        async () => {
          span.update({
            input: {
              promptId: metadata.id,
              platform: metadata.platform,
            },
            output: { rating: event.value === 1 ? "up" : "down" },
          });
          traceId = getActiveTraceId() ?? null;
        },
      );
    });
  }

  await scoreTrace(
    traceId,
    SCORE_NAMES.userThumbs,
    event.value,
    event.comment ?? (event.value === 1 ? "Thumbs up" : "Thumbs down"),
  );

  return { traced: true, traceId, action: "rate-prompt" };
}
