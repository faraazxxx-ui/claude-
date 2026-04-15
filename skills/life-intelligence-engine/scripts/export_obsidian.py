#!/usr/bin/env python3
"""
Life Intelligence Engine — Obsidian Vault Exporter
Generates an Obsidian vault with interlinked Markdown files, YAML frontmatter,
wikilinks, entity pages, and domain indexes.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


DOMAIN_PREFIXES = {
    "career_work": "01-Career-Work",
    "finance_legal": "02-Finance-Legal",
    "health_wellness": "03-Health-Wellness",
    "learning_education": "04-Learning-Education",
    "personal_identity": "05-Personal-Identity",
    "creative_projects": "06-Creative-Projects",
    "relationships_social": "07-Relationships-Social",
    "home_logistics": "08-Home-Logistics",
    "digital_technical": "09-Digital-Technical",
    "reference_archive": "10-Reference-Archive",
}


def slug_to_prefix(slug: str) -> str:
    return DOMAIN_PREFIXES.get(slug, f"99-{slug}")


def make_frontmatter(domain: str, content_type: str, source_file: str,
                     importance: float, entities: list, status: str = "active") -> str:
    """Generate YAML frontmatter for an Obsidian note."""
    entities_yaml = "\n".join(f"  - {e}" for e in entities[:20]) if entities else "  []"
    return f"""---
domain: {domain}
content_type: {content_type}
source_file: {source_file}
importance: {importance}
entities:
{entities_yaml}
tags:
  - lie/{domain.lower().replace(' & ', '-').replace(' ', '-')}
created: {datetime.now().strftime('%Y-%m-%d')}
analyzed: {datetime.now().strftime('%Y-%m-%d')}
status: {status}
---
"""


def insert_wikilinks(content: str, entities: list) -> str:
    """Replace entity mentions with Obsidian wikilinks."""
    for entity in entities:
        if isinstance(entity, dict):
            name = entity.get("name", "")
            etype = entity.get("type", "Concept")
        else:
            name = str(entity)
            etype = "Concept"

        if len(name) < 3:
            continue

        # Replace whole-word mentions with wikilinks
        safe_name = re.escape(name)
        link = f"[[Entities/{etype} - {name}|{name}]]"
        content = re.sub(rf"\b{safe_name}\b", link, content, count=3)

    return content


def make_domain_index(domain: str, prefix: str, clusters: list, summary: dict) -> str:
    """Generate a domain index page with Dataview queries."""
    lines = [
        f"# {domain}\n",
        f"**Nodes:** {summary.get('total_nodes', 0)} | "
        f"**Tokens:** {summary.get('total_tokens', 0)} | "
        f"**Sources:** {summary.get('source_file_count', 0)}\n",
        "## Content\n",
    ]

    for cluster in clusters:
        cid = cluster.get("id", "unknown")
        safe_name = cid.replace("/", "-").replace(" ", "-")
        lines.append(f"- [[{prefix}/{safe_name}|{cid}]] "
                     f"({cluster.get('nodes', 0)} nodes, importance: {cluster.get('importance', 0)})")

    lines.extend([
        "\n## Dataview Query\n",
        "```dataview",
        f'TABLE importance, entities, status',
        f'FROM "{prefix}"',
        f'SORT importance DESC',
        "```\n",
    ])

    return "\n".join(lines)


def make_entity_page(name: str, etype: str, info: dict) -> str:
    """Generate an entity page with backlink info."""
    domains = info.get("domains", [])
    mentions = info.get("mentions", 0)

    lines = [
        f"---",
        f"type: entity",
        f"entity_type: {etype}",
        f"mentions: {mentions}",
        f"domains:",
    ]
    for d in domains:
        lines.append(f"  - {d}")
    lines.extend([
        f"---\n",
        f"# {name}\n",
        f"**Type:** {etype} | **Mentions:** {mentions}\n",
        f"## Appears in Domains\n",
    ])
    for d in domains:
        lines.append(f"- [[{slug_to_prefix(d.lower().replace(' & ', '_').replace(' ', '_'))}/_Index|{d}]]")

    lines.extend([
        "\n## Backlinks\n",
        "```dataview",
        f'LIST',
        f'FROM "" WHERE contains(entities, "{name}")',
        "```\n",
    ])

    return "\n".join(lines)


def make_master_index(domain_index: dict) -> str:
    """Generate the master index page."""
    lines = [
        "# Life Intelligence Engine — Master Index\n",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n",
        "## Domains\n",
    ]

    for domain, info in sorted(domain_index.items()):
        slug = domain.lower().replace(" & ", "_").replace(" ", "_")
        prefix = slug_to_prefix(slug)
        lines.append(f"- [[{prefix}/_Index|{domain}]] — "
                     f"{info.get('total_nodes', 0)} nodes, "
                     f"{info.get('source_file_count', 0)} sources")

    lines.extend([
        "\n## Quick Stats\n",
        "```dataview",
        'TABLE length(rows) as Notes, sum(rows.importance) as "Total Importance"',
        'FROM ""',
        'WHERE domain',
        'GROUP BY domain',
        "```\n",
        "\n## All Entities\n",
        "```dataview",
        'TABLE entity_type, mentions, domains',
        'FROM "Entities"',
        'SORT mentions DESC',
        'LIMIT 50',
        "```\n",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Export assembled knowledge to Obsidian vault")
    parser.add_argument("--assembled-dir", required=True, help="Path to assembled knowledge")
    parser.add_argument("--output-dir", required=True, help="Output vault directory")
    args = parser.parse_args()

    assembled = args.assembled_dir
    vault = args.output_dir

    # Load assembled data
    domain_index = {}
    di_path = os.path.join(assembled, "domain_index.json")
    if os.path.exists(di_path):
        with open(di_path, "r") as f:
            domain_index = json.load(f)

    entity_reg = {}
    er_path = os.path.join(assembled, "entity_registry.json")
    if os.path.exists(er_path):
        with open(er_path, "r") as f:
            entity_reg = json.load(f)

    domains_dir = os.path.join(assembled, "domains")

    # Create vault structure
    os.makedirs(os.path.join(vault, "00-Index"), exist_ok=True)
    os.makedirs(os.path.join(vault, "Entities"), exist_ok=True)
    os.makedirs(os.path.join(vault, "Templates"), exist_ok=True)

    total_notes = 0

    # Process each domain
    if os.path.isdir(domains_dir):
        for domain_slug in sorted(os.listdir(domains_dir)):
            domain_path = os.path.join(domains_dir, domain_slug)
            if not os.path.isdir(domain_path):
                continue

            manifest_path = os.path.join(domain_path, "_manifest.json")
            if not os.path.exists(manifest_path):
                continue

            with open(manifest_path, "r") as f:
                manifest = json.load(f)

            domain_name = manifest.get("domain", domain_slug)
            prefix = slug_to_prefix(domain_slug)
            domain_vault_dir = os.path.join(vault, prefix)
            os.makedirs(domain_vault_dir, exist_ok=True)

            summary = manifest.get("summary", domain_index.get(domain_name, {}))
            clusters = manifest.get("clusters", [])

            print(f"Processing: {domain_name} ({len(clusters)} clusters)")

            # Create cluster notes
            for cluster_info in clusters:
                cluster_file = os.path.join(domain_path, cluster_info.get("file", ""))
                if not os.path.exists(cluster_file):
                    continue

                with open(cluster_file, "r") as f:
                    cluster = json.load(f)

                # Build note content
                cid = cluster.get("cluster_id", "unknown")
                safe_name = cid.replace("/", "-").replace(" ", "-")

                content_parts = []
                all_entities = []
                for node in cluster.get("nodes", []):
                    content_parts.append(node.get("content", ""))

                content = "\n\n".join(content_parts)
                content = insert_wikilinks(content, all_entities)

                frontmatter = make_frontmatter(
                    domain=domain_name,
                    content_type=cluster.get("content_type", "mixed"),
                    source_file=cluster.get("source_file", ""),
                    importance=cluster_info.get("importance", 5),
                    entities=[str(e) for e in all_entities[:20]],
                )

                note = frontmatter + f"\n# {safe_name}\n\n{content}\n"
                note_path = os.path.join(domain_vault_dir, f"{safe_name}.md")

                with open(note_path, "w") as f:
                    f.write(note)
                total_notes += 1

            # Create domain index
            index_content = make_domain_index(domain_name, prefix, clusters, summary)
            with open(os.path.join(domain_vault_dir, "_Index.md"), "w") as f:
                f.write(index_content)

    # Create entity pages
    entity_count = 0
    for name, info in entity_reg.items():
        if info.get("mentions", 0) < 2:
            continue
        etype = info.get("type", "Concept")
        safe_name = re.sub(r'[<>:"/\\|?*]', '', f"{etype} - {name}")[:200]
        page = make_entity_page(name, etype, info)
        with open(os.path.join(vault, "Entities", f"{safe_name}.md"), "w") as f:
            f.write(page)
        entity_count += 1

    # Create master index
    master = make_master_index(domain_index)
    with open(os.path.join(vault, "00-Index", "Master Index.md"), "w") as f:
        f.write(master)

    print(f"\nVault generated: {vault}")
    print(f"  Domain notes: {total_notes}")
    print(f"  Entity pages: {entity_count}")
    print(f"  Total files: {total_notes + entity_count + len(domain_index) + 1}")


if __name__ == "__main__":
    main()
