import { prompts, type PromptData } from "../src/lib/promptData.ts";

export interface PromptMetadata {
  id: number;
  platform: string;
  shortName: string;
  category: PromptData["category"];
  severity: PromptData["severity"];
  description: string;
  charCount: number;
  redTeamFixCount: number;
}

export function getPromptMetadata(promptId: number): PromptMetadata | null {
  const prompt = prompts.find((item) => item.id === promptId);
  if (!prompt) {
    return null;
  }

  return {
    id: prompt.id,
    platform: prompt.platform,
    shortName: prompt.shortName,
    category: prompt.category,
    severity: prompt.severity,
    description: prompt.description,
    charCount: prompt.prompt.length,
    redTeamFixCount: prompt.redTeamFixes.length,
  };
}

export function searchPromptMetadata(query: string): PromptMetadata[] {
  const normalized = query.trim().toLowerCase();
  if (normalized.length === 0) {
    return prompts.map((prompt) => getPromptMetadata(prompt.id)).filter(
      (item): item is PromptMetadata => item !== null,
    );
  }

  return prompts
    .filter((prompt) => {
      return (
        prompt.platform.toLowerCase().includes(normalized) ||
        prompt.description.toLowerCase().includes(normalized) ||
        prompt.shortName.toLowerCase().includes(normalized)
      );
    })
    .map((prompt) => getPromptMetadata(prompt.id))
    .filter((item): item is PromptMetadata => item !== null);
}
