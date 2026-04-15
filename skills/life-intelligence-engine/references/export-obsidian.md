# Export to Obsidian

## Table of Contents
1. Vault Structure
2. Frontmatter Schema
3. Wikilink Strategy
4. Export Workflow
5. Recommended Plugins

## Vault Structure

```
obsidian-vault/
├── 00-Index/
│   ├── Master Index.md          # Links to all domain indexes
│   ├── Entity Registry.md       # All entities with backlinks
│   └── Knowledge Graph Notes.md # Cross-domain connections
├── 01-Career-Work/
│   ├── _Index.md                # Domain overview + links
│   ├── cluster-name-1.md
│   └── cluster-name-2.md
├── 02-Finance-Legal/
├── 03-Health-Wellness/
├── 04-Learning-Education/
├── 05-Personal-Identity/
├── 06-Creative-Projects/
├── 07-Relationships-Social/
├── 08-Home-Logistics/
├── 09-Digital-Technical/
├── 10-Reference-Archive/
├── Entities/
│   ├── Person - Name.md         # Per-entity pages
│   ├── Org - Company.md
│   └── Concept - Topic.md
└── Templates/
    ├── cluster-template.md
    └── entity-template.md
```

## Frontmatter Schema

Every note uses YAML frontmatter for Dataview queries:

```yaml
---
domain: Career & Work
content_type: paragraph
source_file: original-filename.pdf
importance: 8
entities:
  - Entity Name 1
  - Entity Name 2
tags:
  - lie/career
  - lie/project-x
created: 2026-04-15
analyzed: 2026-04-15
status: active
aliases:
  - alternate name
---
```

Tag convention: `lie/<domain-slug>`, `lie/entity/<name>`, `lie/type/<content-type>`

## Wikilink Strategy

Use wikilinks to create the knowledge graph:

- **Domain links**: `[[01-Career-Work/_Index|Career & Work]]`
- **Entity links**: `[[Entities/Person - John Smith|John Smith]]`
- **Cross-references**: `[[02-Finance-Legal/tax-docs|Related: Tax Documents]]`
- **Cluster links**: `[[01-Career-Work/project-alpha|Project Alpha Notes]]`

Every entity mention in content should be wrapped in `[[Entities/Type - Name|Name]]`
to build the graph automatically.

## Export Workflow

```bash
python3 /home/ubuntu/skills/life-intelligence-engine/scripts/export_obsidian.py \
  --assembled-dir /home/ubuntu/work/lie-output/assembled/ \
  --output-dir /home/ubuntu/work/lie-output/obsidian-vault/
```

The script:
1. Creates the vault directory structure
2. Generates frontmatter for each cluster note
3. Converts node content to Obsidian-flavored Markdown
4. Inserts wikilinks for all entity mentions
5. Creates entity pages with backlink summaries
6. Generates domain index pages with Dataview queries
7. Creates the master index

## Recommended Plugins

| Plugin | Purpose |
|--------|---------|
| Dataview | Query notes by frontmatter properties |
| Graph Analysis | Enhanced graph view with clustering |
| Templater | Auto-generate notes from templates |
| Juggl | Interactive graph exploration |
| ExcaliBrain | Mind-map visualization of connections |
| Tag Wrangler | Manage the lie/* tag hierarchy |
| Calendar | Navigate notes by date |
| Breadcrumbs | Hierarchical navigation between domains |

Dataview query example for domain overview:

```dataview
TABLE importance, entities, status
FROM "01-Career-Work"
SORT importance DESC
LIMIT 20
```
