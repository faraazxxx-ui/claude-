# Corpus Forensics

*Structural metrics for `.` — 259 files.*

## 1. Finality claims

Files whose names assert they are the last word: `FINAL`, `PERFECTED`, `MASTER`, `_v3`.
A high rate means each session declared victory and the next session disagreed.

- **29 files (11.2% of corpus)** carry a finality or version token.

## 2. Byte-identical duplicates

- **3 groups** of files with identical content at different paths.

```
  health_analysis_v2/red_team_analysis.md
  prompts/red_team_analysis.md
```

```
  skill/health-data-analyst/references/compass_artifact.md
  skill/references/compass_artifact.md
```

```
  skill/health-data-analyst/references/unified_model.md
  skill/references/unified_model.md
```

## 3. Version families

Files that collapse to the same name once version and finality tokens are stripped.
Each family is one idea stored in N places, with no page saying which one is true.

- **5 families** covering **14 files**.

| Canonical idea | Copies | Paths |
|---|---:|---|
| `red_team_analysis.md` | 4 | daily-note-ai-integration/RED_TEAM_ANALYSIS.md<br>health_analysis_v2/red_team_analysis.md<br>optimized-prompts/red_team_analysis.md<br>prompts/red_team_analysis.md |
| `report.md` | 3 | analysis-output/master_report.md<br>analysis-output/perfected/PERFECTED_MASTER_REPORT.md<br>health_analysis_v2/PERFECTED_REPORT.md |
| `prompts.md` | 3 | daily-workflow-optimizer/PERFECTED_PROMPTS.md<br>prompts/FINAL_OPTIMIZED_PROMPTS.md<br>prompts/PERFECTED_PROMPTS.md |
| `medication_adherence.json` | 2 | autonomic_intelligence_v3/medication_adherence_v3.json<br>health_analysis_v2/medication_adherence.json |
| `ghusoon_prompts.md` | 2 | optimized-prompts/Ghusoon_Optimized_Prompts_Final.md<br>optimized-prompts/Ghusoon_Perfected_Prompts_v2.md |

> Every family above is a wiki page waiting to exist. Pick the best copy, promote it
> to `brain/`, and leave the rest as history. The point is not tidiness — it is that the
> next session can find the answer instead of regenerating it.
