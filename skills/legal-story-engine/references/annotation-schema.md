# Annotation schema (generalized)

## Block (unit of any time- or page-indexed source)
```json
{
  "anchor": "HH:MM:SS | p.12 | Bates 000123",
  "speakers_present": ["resolved identities"],
  "clean_summary": "faithful 2-4 sentence account, corrections applied",
  "key_quotes": [{"speaker": "...", "quote": "verbatim", "significance": "one line"}],
  "corrections": [{"raw": "...", "corrected": "...", "basis": "quoted evidence", "confidence": 0.0}],
  "tags": ["closed enum per matter, e.g. discovery|damages|admission|timeline|evidence|health|smalltalk"],
  "callout": "one-line legal significance, or null"
}
```

## Fact
```json
{"fact": "...", "anchor": "...", "quote_anchor": "short verbatim locator", "claim_links": ["cause of action / defense it feeds"]}
```

## Action item
```json
{"item": "...", "owner": "...", "deadline_stated": "... | null", "deadline_inferred": "... | null", "anchor": "..."}
```

## Research finding
```json
{"question": "...", "claim": "...",
 "authority": {"type": "case|statute|regulation|factual", "name": "...", "citation": "...",
   "court": "...", "year": 0, "database_id": "...", "verification": "VERIFIED|UNVERIFIED_WEB|NOT_FOUND"},
 "holding_or_text": "...", "relevance": "...", "cuts_against_us": false}
```

## Damages line item
```json
{"category": "...", "amount_low": 0, "amount_high": 0,
 "evidence_label": "DOCUMENTED|ESTIMABLE|ASSERTED", "evidence_ref": "...", "statute_basis": "... | null"}
```

Closed enums stay closed — a value outside the enum is a schema failure, not a new category.
`cuts_against_us: true` findings are required output; a research file with none is suspect.
