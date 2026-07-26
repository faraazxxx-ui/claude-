# Why wiki pages

**The short version: a wiki page is a compressed answer with a permanent address. Chat logs are
raw data with no address at all. Retrieval quality is decided by signal-per-token, and a page beats
a transcript by roughly an order of magnitude. The links between pages are the map of your thinking
you have been asking for — you do not have to infer that graph, you build it as a side effect of
writing.**

---

## The proof is already in this repository

`analysis-output/perfected/SECOND_BRAIN_ARCHITECTURE.md` contains a genuinely good deduplicated
entity registry: canonical names, aliases, relationship map, a thirteen-domain taxonomy with
evidence. Real work, correctly done.

It has been functionally lost since the day it was written.

Nothing links to it. Nothing tells a new session it exists. It sits three directories deep in a
folder called `analysis-output/perfected/`, and no future session will ever guess that path. So the
next session will rebuild it, badly, and call the result `ENTITY_REGISTRY_FINAL_v2.json`.

**The knowledge was never the bottleneck. The address was.** That is the entire case for wiki pages
in one example, drawn from your own corpus.

---

## What a page does that a transcript cannot

### 1. It gives an idea one address

Ten thousand conversations mention the residency dispute. Each mention is a fragment with different
wording, partial context, and whatever you happened to believe that day. Retrieval over those
fragments returns a scatter of contradictions.

One page called `residency-dispute.md` is the resolved position. Every future question routes to it.
Ideas need somewhere to *be*, not just somewhere to have been mentioned.

### 2. It raises signal-per-token, which is what actually decides accuracy

Retrieval pulls the top-k chunks by similarity and drops them into the context window. Whether the
model is right depends almost entirely on the density of what arrives.

| Source | Typical retrieval | Signal |
|---|---|---|
| Raw chat log | 40 fragments, ~8,000 tokens, mostly restatement and dead ends | low |
| Wiki page | 1 page, ~700 tokens, resolved and current | high |

Same question, same model. Utterly different answer. **You are not trying to give the model more of
your data. You are trying to give it the right 700 tokens.**

### 3. It is where contradictions get resolved *once*

Your view in March and your view in September will differ. In a chat corpus both survive forever and
retrieval picks whichever is textually closer to the query — often the older, wronger one.

A page holds the current position, with the change noted. Contradiction gets resolved at write time,
by you, once — instead of at read time, by a model, badly, every time.

### 4. The links are the map you have been trying to reverse-engineer

You want to see your brain's linkages. The instinct is to infer them statistically from chat history.
That is possible but noisy, and it recovers only *co-occurrence*.

Wiki links give you something better and cheaper. Every `[[link]]` you write is an edge you asserted
deliberately. Backlinks tell you which pages everything else depends on — your genuine centres of
gravity, which are reliably *not* the ones you would name if asked. `tools/wiki_lint.py` computes
this and draws it.

Statistical inference from chats tells you what you *talked about*. The link graph tells you what
you *think depends on what*. The second is the more useful object.

### 5. It makes "trained on itself" actually work

Here is the honest mechanics of what you described.

You cannot retrain the weights, and you would not want to — it is slow, expensive, and irreversible.
But the loop you are imagining is real, and it runs at Layer 8 instead:

```
session → answer → written to a page → next session retrieves the page
        → builds on it instead of rebuilding it → page improves → repeat
```

That is a learning system. The update step is **curation**, not gradient descent. The corpus gets
monotonically better because every session is required to leave it better. Slower per step than
backpropagation, but it converges on *your* judgement rather than on the average of the internet,
and you can read and correct every parameter.

The requirement is the write-back step. Miss it and the loop is open — which is precisely what
happened here for twelve sessions running. `CLAUDE.md` now enforces it.

### 6. Git gives you the retrospective and the prospective at once

Pages under version control produce a time series of your thinking. `git log` on
`residency-dispute.md` is a record of how your position moved and when.

That is the retrospective. The prospective falls out of it: a page that changes every week is
unstable and needs attention; a page untouched for six months is either settled or abandoned, and
`wiki_lint.py --stalest` tells you which pages have gone quiet.

### 7. For ADHD specifically: the page persists when the intention does not

This is the one that matters most, and it is not really about AI.

Every other capture method depends on you remembering, at the moment of need, that a thing exists.
That is the exact function that ADHD taxes hardest — not attention, *retrieval of intention*.

A page at a predictable address, linked from a hub you always start at, removes the remembering
step. You do not have to recall that you already solved this. You open `brain/index.md` and it is
there. The system holds the thread so you do not have to.

---

## What makes a page good

- **One idea.** If the title needs "and", it is two pages.
- **Answer first.** A page you have to read to the bottom of will not be read.
- **Under a thousand words.** Longer means it is really an index; split it and link.
- **Evidence separated from inference.** You are a physician. Mark which is which.
- **At least one inbound link, made in the same session it was created.** Otherwise it is an orphan
  and it does not exist.
- **Plain noun filename.** `health-analysis.md`. Not `PERFECTED_HEALTH_REPORT_v4.md` — see
  [[anti-versioning]].

## What is not a page

Raw data, transcripts, exports, generated reports. Those stay in `ingest/` and in the history
directories at the repository root. A page *points at* them and says what they mean.

Do not import 3,700 files into `brain/`. Import the sixty conclusions.

## Links

- [[index]] · [[claude-layers]] · [[anti-versioning]] · [[ai-medicine-rosetta]] · [[second-brain]]
