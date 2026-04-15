#!/usr/bin/env python3
"""
Life Intelligence Engine — Triage Assembler
Merges parallel analysis results with original nodes and produces a unified
triage report with domain assignments, entity registry, and relationship graph.
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


DEFAULT_DOMAINS = [
    "Career & Work",
    "Finance & Legal",
    "Health & Wellness",
    "Learning & Education",
    "Personal & Identity",
    "Creative & Projects",
    "Relationships & Social",
    "Home & Logistics",
    "Digital & Technical",
    "Reference & Archive",
]


def load_nodes(nodes_dir: str) -> dict:
    """Load all node files and return a dict keyed by node_id."""
    nodes = {}
    for fname in os.listdir(nodes_dir):
        if fname.startswith("_") or not fname.endswith(".json"):
            continue
        fpath = os.path.join(nodes_dir, fname)
        try:
            with open(fpath, "r") as f:
                data = json.load(f)
            for node in data.get("nodes", []):
                nodes[node["node_id"]] = {
                    **node,
                    "source_info": data.get("source", {}),
                }
        except Exception as e:
            print(f"  WARN: Could not load {fname}: {e}", file=sys.stderr)
    return nodes


def load_analysis_results(results_path: str) -> dict:
    """Load parallel analysis results. Supports both JSON and CSV formats."""
    if results_path.endswith(".csv"):
        import csv
        results = {}
        with open(results_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                node_id = row.get("node_id", "")
                if node_id:
                    results[node_id] = row
        return results

    with open(results_path, "r") as f:
        data = json.load(f)

    # Handle various formats from parallel processing
    if isinstance(data, list):
        results = {}
        for item in data:
            if isinstance(item, dict) and "node_id" in item:
                results[item["node_id"]] = item
        return results
    elif isinstance(data, dict):
        return data
    return {}


def build_entity_registry(nodes: dict, analysis: dict) -> dict:
    """Build a unified entity registry from all extracted entities."""
    entities = defaultdict(lambda: {
        "mentions": 0,
        "domains": set(),
        "source_files": set(),
        "node_ids": [],
        "type": "unknown",
    })

    for node_id, result in analysis.items():
        extracted_entities = result.get("entities", [])
        domain = result.get("domain", "Reference & Archive")

        if isinstance(extracted_entities, str):
            try:
                extracted_entities = json.loads(extracted_entities)
            except Exception:
                extracted_entities = [e.strip() for e in extracted_entities.split(",") if e.strip()]

        node = nodes.get(node_id, {})
        source_file = node.get("source_file", "")

        for entity in extracted_entities:
            if isinstance(entity, dict):
                name = entity.get("name", str(entity))
                etype = entity.get("type", "unknown")
            else:
                name = str(entity)
                etype = "unknown"

            name = name.strip()
            if len(name) < 2 or len(name) > 200:
                continue

            entities[name]["mentions"] += 1
            entities[name]["domains"].add(domain)
            entities[name]["source_files"].add(source_file)
            entities[name]["node_ids"].append(node_id)
            if etype != "unknown":
                entities[name]["type"] = etype

    # Convert sets to lists for JSON serialization
    for name in entities:
        entities[name]["domains"] = list(entities[name]["domains"])
        entities[name]["source_files"] = list(entities[name]["source_files"])

    return dict(entities)


def build_domain_index(nodes: dict, analysis: dict) -> dict:
    """Build domain → node mapping with statistics."""
    domains = defaultdict(lambda: {
        "node_count": 0,
        "total_tokens": 0,
        "source_files": set(),
        "top_entities": defaultdict(int),
        "avg_importance": 0,
        "importance_sum": 0,
        "node_ids": [],
    })

    for node_id, result in analysis.items():
        domain = result.get("domain", "Reference & Archive")
        importance = float(result.get("importance_score", 5))
        node = nodes.get(node_id, {})

        domains[domain]["node_count"] += 1
        domains[domain]["total_tokens"] += node.get("token_count", 0)
        domains[domain]["source_files"].add(node.get("source_file", ""))
        domains[domain]["importance_sum"] += importance
        domains[domain]["node_ids"].append(node_id)

        # Track entities per domain
        entities = result.get("entities", [])
        if isinstance(entities, str):
            entities = [e.strip() for e in entities.split(",") if e.strip()]
        for entity in entities:
            name = entity.get("name", str(entity)) if isinstance(entity, dict) else str(entity)
            domains[domain]["top_entities"][name] += 1

    # Finalize
    for domain in domains:
        d = domains[domain]
        d["source_files"] = list(d["source_files"])
        d["avg_importance"] = round(d["importance_sum"] / max(d["node_count"], 1), 2)
        # Keep top 20 entities
        d["top_entities"] = dict(sorted(d["top_entities"].items(), key=lambda x: -x[1])[:20])
        del d["importance_sum"]

    return dict(domains)


def build_cross_references(analysis: dict) -> list:
    """Identify cross-domain relationships between nodes."""
    cross_refs = []
    entity_to_nodes = defaultdict(list)

    for node_id, result in analysis.items():
        entities = result.get("entities", [])
        domain = result.get("domain", "")
        if isinstance(entities, str):
            entities = [e.strip() for e in entities.split(",") if e.strip()]
        for entity in entities:
            name = entity.get("name", str(entity)) if isinstance(entity, dict) else str(entity)
            entity_to_nodes[name].append({"node_id": node_id, "domain": domain})

    # Find entities that span multiple domains
    for entity, occurrences in entity_to_nodes.items():
        domains_involved = set(o["domain"] for o in occurrences)
        if len(domains_involved) > 1:
            cross_refs.append({
                "entity": entity,
                "domains": list(domains_involved),
                "node_count": len(occurrences),
                "node_ids": [o["node_id"] for o in occurrences],
            })

    return sorted(cross_refs, key=lambda x: -x["node_count"])


def main():
    parser = argparse.ArgumentParser(description="Assemble triage report from analysis results")
    parser.add_argument("--nodes-dir", required=True, help="Directory containing node JSON files")
    parser.add_argument("--analysis-results", required=True, help="Path to analysis results (JSON or CSV)")
    parser.add_argument("--output", required=True, help="Output triage report path")
    args = parser.parse_args()

    print("Loading nodes...")
    nodes = load_nodes(args.nodes_dir)
    print(f"  Loaded {len(nodes)} nodes")

    print("Loading analysis results...")
    analysis = load_analysis_results(args.analysis_results)
    print(f"  Loaded {len(analysis)} analysis entries")

    # Match analysis to nodes
    matched = 0
    unmatched_nodes = []
    for node_id in nodes:
        if node_id in analysis:
            matched += 1
        else:
            unmatched_nodes.append(node_id)
    print(f"  Matched: {matched}, Unmatched: {len(unmatched_nodes)}")

    # Assign defaults to unmatched nodes
    for node_id in unmatched_nodes:
        analysis[node_id] = {
            "domain": "Reference & Archive",
            "entities": [],
            "relationships": [],
            "importance_score": 3,
            "summary": nodes[node_id].get("content", "")[:100],
            "auto_assigned": True,
        }

    print("Building entity registry...")
    entity_registry = build_entity_registry(nodes, analysis)
    print(f"  Found {len(entity_registry)} unique entities")

    print("Building domain index...")
    domain_index = build_domain_index(nodes, analysis)
    print(f"  Domains: {list(domain_index.keys())}")

    print("Building cross-references...")
    cross_refs = build_cross_references(analysis)
    print(f"  Found {len(cross_refs)} cross-domain links")

    # Assemble triage report
    triage = {
        "generated": datetime.now().isoformat(),
        "summary": {
            "total_nodes": len(nodes),
            "total_analyzed": len(analysis),
            "total_entities": len(entity_registry),
            "total_domains": len(domain_index),
            "cross_domain_links": len(cross_refs),
        },
        "domain_index": domain_index,
        "entity_registry": entity_registry,
        "cross_references": cross_refs[:100],  # Top 100
        "node_assignments": {
            node_id: {
                "domain": analysis.get(node_id, {}).get("domain", "Reference & Archive"),
                "importance": analysis.get(node_id, {}).get("importance_score", 3),
                "summary": analysis.get(node_id, {}).get("summary", ""),
            }
            for node_id in nodes
        },
    }

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(triage, f, indent=2, default=str)

    print(f"\nTriage report written: {args.output}")
    print(f"\nDomain breakdown:")
    for domain, info in sorted(domain_index.items(), key=lambda x: -x[1]["node_count"]):
        print(f"  {domain}: {info['node_count']} nodes, {info['total_tokens']} tokens, "
              f"avg importance: {info['avg_importance']}")


if __name__ == "__main__":
    main()
