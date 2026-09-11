const SESSION_KEY = "ghusoon-langfuse-session-id";

function createSessionId(): string {
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    return `session_${crypto.randomUUID()}`;
  }
  return `session_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`;
}

export function getHubSessionId(): string {
  if (typeof window === "undefined") {
    return "anonymous-session";
  }

  const existing = window.localStorage.getItem(SESSION_KEY);
  if (existing && existing.length >= 8) {
    return existing;
  }

  const sessionId = createSessionId();
  window.localStorage.setItem(SESSION_KEY, sessionId);
  return sessionId;
}
