// Relay-loop skeletons for the Workflow tool. Copy, rename, fill prompts.
// Conventions: agents WRITE payloads to disk, RETURN compact receipts; checkers REJECT by default;
// repair loops are bounded (2); main loop runs scripted gates between workflows.

export const meta = {
  name: 'relay-template',
  description: 'Skeleton: sectioned analysis → merge → evaluator loop',
  phases: [{ title: 'Attempt' }, { title: 'Check' }],
}

const RECEIPT = {
  type: 'object', required: ['output_file', 'headline'],
  properties: {
    output_file: { type: 'string' },
    headline: { type: 'array', items: { type: 'string' }, maxItems: 6 },
    warnings: { type: 'array', items: { type: 'string' } },
  },
}

const VERDICT = {
  type: 'object', required: ['pass', 'issues', 'required_fixes'],
  properties: {
    pass: { type: 'boolean' },
    issues: { type: 'array', items: { type: 'string' } },
    required_fixes: { type: 'array', items: { type: 'object', required: ['file', 'fix'],
      properties: { file: { type: 'string' }, fix: { type: 'string' } } } },
  },
}

// ---- 3. Parallelization (sectioning): one agent per pre-cut segment ----
phase('Attempt')
const SEGMENTS = ['seg-01', 'seg-02', 'seg-03'] // cut deterministically in the main loop, with overlap
const receipts = (await parallel(SEGMENTS.map(s => () => agent(
  `Analyze <dir>/${s}.txt. HARD RULES: never invent; every claim keeps its anchor. ` +
  `Write full JSON to <dir>/analysis/${s}.json. Return the compact receipt only.`,
  { label: `analyst:${s}`, schema: RECEIPT }
)))).filter(Boolean)

// ---- 1. Chaining: merge consumes the sectioned outputs ----
const merge = await agent(
  `Read all files in <dir>/analysis/. Dedupe seam overlaps (keep the richer twin). ` +
  `Write canon to <dir>/canon.json. Return receipt.`,
  { label: 'merge', schema: RECEIPT }
)

// ---- 5. Evaluator-optimizer: adversarial check + bounded repair ----
phase('Check')
const CHECK = `You are an adversarial checker. REJECT unless every sampled claim matches ground truth ` +
  `at <dir>/raw.txt. Sample >= 15 anchors. Findings that cut against the goal are mandatory to record.`
let verdict = await agent(CHECK, { label: 'checker', schema: VERDICT })
let rounds = 0
while (verdict && !verdict.pass && rounds < 2) {
  rounds++
  await parallel(verdict.required_fixes.map(f => () => agent(
    `Edit ${f.file} in place: ${f.fix}. Minimal targeted change; do not touch verified content. Return receipt.`,
    { label: `fixer:${rounds}`, schema: RECEIPT }
  )))
  verdict = await agent(CHECK, { label: `checker:re${rounds}`, schema: VERDICT })
}
// exit rule: second failure escalates — return the verdict, the human decides
return { merge, verdict, rounds }

// ---- 3b. Voting variant (drop-in): N distinct lenses on one question ----
// const votes = (await parallel(['correctness','sourcing','adversarial'].map(lens => () => agent(
//   `Judge <claim> through the ${lens} lens. Default to refuted=true when uncertain.`,
//   { label: `vote:${lens}`, schema: { type:'object', required:['refuted','why'],
//     properties:{ refuted:{type:'boolean'}, why:{type:'string'} } } }
// )))).filter(Boolean)
// const survives = votes.filter(v => !v.refuted).length >= 2

// ---- 4. Orchestrator-workers (drop-in): typed work-list, capped ----
// const plan = await agent('Decompose <mission> into <=6 work items with rationale.',
//   { label:'orchestrator', schema:{ type:'object', required:['items'], properties:{ items:{
//     type:'array', maxItems:6, items:{ type:'object', required:['id','brief','rationale'],
//       properties:{ id:{type:'string'}, brief:{type:'string'}, rationale:{type:'string'} } } } } } })
// const results = await parallel(plan.items.map(it => () => agent(it.brief, { label:it.id, schema:RECEIPT })))
