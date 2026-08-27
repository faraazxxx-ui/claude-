#!/usr/bin/env python3
"""
Life Intelligence Engine — Master Report Generator
Reads the assembled knowledge structure and produces a comprehensive
Markdown analysis report with domain breakdowns, knowledge graph stats,
temporal analysis, and actionable recommendations.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def load_json(filepath: str) -> dict:
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)


def generate_executive_summary(domain_index: dict, entity_reg: dict,
                                cross_refs: dict, graph: dict) -> str:
    """Generate the executive summary section."""
    total_nodes = sum(d.get("total_nodes", 0) for d in domain_index.values())
    total_tokens = sum(d.get("total_tokens", 0) for d in domain_index.values())
    total_domains = len(domain_index)
    total_entities = len(entity_reg)
    total_links = cross_refs.get("link_count", 0)
    graph_nodes = len(graph.get("nodes", []))
    graph_edges = len(graph.get("edges", []))

    lines = [
        "## Executive Summary\n",
        f"This analysis processed **{total_nodes:,} content nodes** containing approximately "
        f"**{total_tokens:,} tokens** across **{total_domains} life domains**.\n",
        f"The extraction pipeline identified **{total_entities:,} unique entities** "
        f"(people, organizations, concepts, dates, locations) and established "
        f"**{total_links:,} cross-domain relationships**.\n",
        f"The knowledge graph contains **{graph_nodes:,} nodes** connected by "
        f"**{graph_edges:,} edges**, forming a comprehensive map of your digital life.\n",
    ]

    # Top domains by size
    sorted_domains = sorted(domain_index.items(), key=lambda x: -x[1].get("total_nodes", 0))
    lines.append("**Largest domains by content volume:**\n")
    lines.append("| Domain | Nodes | Tokens | Source Files |")
    lines.append("|--------|-------|--------|-------------|")
    for domain, info in sorted_domains[:5]:
        lines.append(f"| {domain} | {info.get('total_nodes', 0):,} | "
                     f"{info.get('total_tokens', 0):,} | {info.get('source_file_count', 0)} |")
    lines.append("")

    return "\n".join(lines)


def generate_domain_breakdown(domain_index: dict) -> str:
    """Generate per-domain detailed breakdown."""
    lines = ["## Domain Breakdown\n"]

    for domain, info in sorted(domain_index.items(), key=lambda x: -x[1].get("total_nodes", 0)):
        lines.append(f"### {domain}\n")
        lines.append(f"- **Nodes:** {info.get('total_nodes', 0):,}")
        lines.append(f"- **Tokens:** {info.get('total_tokens', 0):,}")
        lines.append(f"- **Clusters:** {info.get('cluster_count', 0)}")
        lines.append(f"- **Source files:** {info.get('source_file_count', 0)}")
        lines.append("")

        # Top clusters
        top_clusters = info.get("top_clusters", [])
        if top_clusters:
            lines.append("**Top content clusters:**\n")
            lines.append("| Source | Type | Nodes | Importance |")
            lines.append("|--------|------|-------|------------|")
            for c in top_clusters:
                lines.append(f"| {c.get('source', 'N/A')} | {c.get('type', 'N/A')} | "
                             f"{c.get('nodes', 0)} | {c.get('importance', 0)} |")
            lines.append("")

        # Content digest
        digest = info.get("content_digest", [])
        if digest:
            lines.append("**Content preview:**\n")
            for d in digest[:3]:
                lines.append(f"> {d[:200]}...\n")
            lines.append("")

    return "\n".join(lines)


def generate_knowledge_graph_overview(graph: dict, cross_refs: dict) -> str:
    """Generate knowledge graph statistics and highlights."""
    lines = ["## Knowledge Graph Overview\n"]

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    lines.append(f"The knowledge graph contains **{len(nodes):,} nodes** and "
                 f"**{len(edges):,} edges**.\n")

    # Node distribution by domain
    domain_counts = {}
    for n in nodes:
        d = n.get("domain", "Unknown")
        domain_counts[d] = domain_counts.get(d, 0) + 1

    if domain_counts:
        lines.append("**Node distribution by domain:**\n")
        lines.append("| Domain | Nodes | % of Total |")
        lines.append("|--------|-------|------------|")
        total = len(nodes) or 1
        for domain, count in sorted(domain_counts.items(), key=lambda x: -x[1]):
            pct = round(count / total * 100, 1)
            lines.append(f"| {domain} | {count:,} | {pct}% |")
        lines.append("")

    # Most connected entities
    most_connected = cross_refs.get("most_connected_entities", [])
    if most_connected:
        lines.append("**Most connected entities (spanning multiple domains):**\n")
        for i, entity in enumerate(most_connected[:10], 1):
            lines.append(f"{i}. {entity}")
        lines.append("")

    # Cross-domain links
    links = cross_refs.get("cross_domain_links", [])
    if links:
        lines.append("**Top cross-domain connections:**\n")
        lines.append("| Entity | Domains | Strength |")
        lines.append("|--------|---------|----------|")
        for link in links[:10]:
            domains_str = ", ".join(link.get("domains", []))
            lines.append(f"| {link.get('entity', 'N/A')} | {domains_str} | "
                         f"{link.get('strength', 0)} |")
        lines.append("")

    return "\n".join(lines)


def generate_temporal_analysis(timeline: list) -> str:
    """Generate temporal analysis from timeline events."""
    lines = ["## Temporal Analysis\n"]

    if not timeline:
        lines.append("No temporal data available. Dates will be populated as files with "
                     "date metadata are processed.\n")
        return "\n".join(lines)

    # Group by year-month
    monthly = {}
    for event in timeline:
        date = event.get("date", "")
        if len(date) >= 7:
            month_key = date[:7]
            monthly[month_key] = monthly.get(month_key, 0) + 1

    if monthly:
        lines.append("**Content creation timeline (by month):**\n")
        lines.append("| Month | Events |")
        lines.append("|-------|--------|")
        for month, count in sorted(monthly.items()):
            lines.append(f"| {month} | {count} |")
        lines.append("")

    return "\n".join(lines)


def generate_recommendations(domain_index: dict, entity_reg: dict, cross_refs: dict) -> str:
    """Generate actionable recommendations based on the analysis."""
    lines = ["## Recommended Actions\n"]

    # Find underrepresented domains
    all_domains = [
        "Career & Work", "Finance & Legal", "Health & Wellness",
        "Learning & Education", "Personal & Identity", "Creative & Projects",
        "Relationships & Social", "Home & Logistics", "Digital & Technical",
        "Reference & Archive",
    ]
    present_domains = set(domain_index.keys())
    missing = [d for d in all_domains if d not in present_domains]

    if missing:
        lines.append("**Gaps detected — these life domains have no content:**\n")
        for d in missing:
            lines.append(f"- {d}")
        lines.append("\nConsider adding documents for these areas to build a complete second brain.\n")

    # Find domains with low node counts
    thin_domains = [(d, info) for d, info in domain_index.items()
                    if info.get("total_nodes", 0) < 10]
    if thin_domains:
        lines.append("**Thin domains (fewer than 10 nodes):**\n")
        for d, info in thin_domains:
            lines.append(f"- {d}: {info.get('total_nodes', 0)} nodes — consider adding more content")
        lines.append("")

    # High-importance entities that appear in only one domain
    single_domain_important = []
    for entity, info in entity_reg.items():
        if info.get("mentions", 0) >= 3 and len(info.get("domains", [])) == 1:
            single_domain_important.append(entity)
    if single_domain_important:
        lines.append("**Frequently mentioned entities confined to a single domain:**\n")
        for e in single_domain_important[:10]:
            lines.append(f"- {e}")
        lines.append("\nThese may benefit from cross-referencing in other domains.\n")

    lines.append("**General recommendations:**\n")
    lines.append("1. Review the cross-domain connections for unexpected insights")
    lines.append("2. Add date metadata to undated files for better temporal analysis")
    lines.append("3. Re-run the pipeline periodically as new files are added")
    lines.append("4. Use the knowledge graph to identify central concepts in your life")
    lines.append("5. Export to all four databases and review the organization in each\n")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate master analysis report")
    parser.add_argument("--assembled-dir", required=True, help="Path to assembled knowledge directory")
    parser.add_argument("--output", required=True, help="Output report path (.md)")
    args = parser.parse_args()

    assembled = args.assembled_dir

    print("Loading assembled knowledge...")
    domain_index = load_json(os.path.join(assembled, "domain_index.json"))
    entity_reg = load_json(os.path.join(assembled, "entity_registry.json"))
    cross_refs = load_json(os.path.join(assembled, "cross_references.json"))
    graph = load_json(os.path.join(assembled, "knowledge_graph.json"))
    timeline = load_json(os.path.join(assembled, "temporal_timeline.json"))
    if not isinstance(timeline, list):
        timeline = []

    print(f"  Domains: {len(domain_index)}")
    print(f"  Entities: {len(entity_reg)}")
    print(f"  Graph nodes: {len(graph.get('nodes', []))}")

    # Build report
    report_parts = [
        f"# Life Intelligence Engine — Master Analysis Report\n",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n",
        "---\n",
        generate_executive_summary(domain_index, entity_reg, cross_refs, graph),
        generate_domain_breakdown(domain_index),
        generate_knowledge_graph_overview(graph, cross_refs),
        generate_temporal_analysis(timeline),
        generate_recommendations(domain_index, entity_reg, cross_refs),
        "## Database Sync Status\n",
        "| Target | Status | Notes |",
        "|--------|--------|-------|",
        "| Notion | Pending | Run export-notion workflow |",
        "| Evernote | Pending | Run export-evernote workflow |",
        "| Obsidian | Pending | Run export-obsidian workflow |",
        "| NotebookLM | Pending | Run export-notebooklm workflow |",
        "",
        "---\n",
        "*Report generated by Life Intelligence Engine*\n",
    ]

    report = "\n".join(report_parts)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w") as f:
        f.write(report)

    print(f"\nReport written: {args.output}")
    print(f"  Size: {len(report):,} characters")


if __name__ == "__main__":
    main()
