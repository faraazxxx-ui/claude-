# Export to Notion

## Table of Contents
1. Database Architecture
2. Page Structure
3. Export Workflow
4. Notion MCP Integration

## Database Architecture

Create a master Notion database with these properties:

| Property | Type | Description |
|----------|------|-------------|
| Title | Title | Node summary or document name |
| Domain | Select | Life domain (Career, Finance, Health, etc.) |
| Content Type | Select | paragraph, code, table, image_ref, etc. |
| Source File | Text | Original file path |
| Importance | Number | 1-10 score |
| Entities | Multi-select | Extracted entities |
| Tags | Multi-select | Auto-generated + manual tags |
| Created Date | Date | Original file date |
| Last Analyzed | Date | Pipeline run date |
| Status | Select | Active / Archive / Reference |
| Related Nodes | Relation | Links to related entries |

Create sub-databases per domain for focused views. Link them via the Domain property.

## Page Structure

Each Notion page represents a cluster (group of related nodes from one source file):

```
# [Cluster Title — derived from source file + domain]

## Metadata
- Domain: [domain]
- Source: [filename]
- Nodes: [count]
- Importance: [avg score]

## Content
[Reassembled content from all nodes in the cluster, in original order]

## Entities
[List of extracted entities with types]

## Cross-References
[Links to related pages in other domains]
```

## Export Workflow

Use the Notion MCP server to create pages:

```bash
# 1. Create the master database (once)
manus-mcp-cli tool call create_database --server notion --input '{
  "parent_id": "<workspace_page_id>",
  "title": "Life Intelligence Engine",
  "properties": {
    "Domain": {"type": "select", "options": ["Career & Work", "Finance & Legal", "Health & Wellness", "Learning & Education", "Personal & Identity", "Creative & Projects", "Relationships & Social", "Home & Logistics", "Digital & Technical", "Reference & Archive"]},
    "Importance": {"type": "number"},
    "Content Type": {"type": "select"},
    "Status": {"type": "select", "options": ["Active", "Archive", "Reference"]}
  }
}'

# 2. For each domain, create pages from assembled clusters
# Read assembled/domains/<domain>/_manifest.json for cluster list
# For each cluster, create a Notion page with full content
```

For bulk page creation, iterate through the domain directories and use
`create_page` for each cluster. Include the full reassembled content in
Notion-flavored Markdown format.

**Critical Notion formatting rules:**
- Tables MUST use `<table header-row="true">` format, NOT markdown pipes
- NO bold/italic inside table cells
- Each `<tr>` and `<td>` on its own line
- Content parameter is the full Markdown string, not a file path

## Notion MCP Integration

Available MCP tools for Notion export:

```bash
manus-mcp-cli tool list --server notion    # List all available tools
```

Key tools: `create_database`, `create_page`, `update_page`, `search`.
Always read the Notion-flavored Markdown spec first:

```bash
manus-mcp-cli resource read notion://docs/enhanced-markdown-spec --server notion
```
