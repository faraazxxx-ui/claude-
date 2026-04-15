#!/usr/bin/env python3
"""
Life Intelligence Engine — Knowledge Reassembler
Takes the triage report and reassembles decomposed nodes into a coherent
knowledge structure using transformer-inspired sequential layering:
positional encoding → self-attention → cross-attention → feed-forward → output.
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def load_triage(triage_path: str) -> dict:
    with open(triage_path, "r") as f:
        return json.load(f)


def load_all_nodes(nodes_dir: str) -> dict:
    """Load all nodes from the nodes directory."""
    nodes = {}
    if not os.path.isdir(nodes_dir):
        return nodes
    for fname in os.listdir(nodes_dir):
        if fname.startswith("_") or not fname.endswith(".json"):
            continue
        fpath = os.path.join(nodes_dir, fname)
        try:
            with open(fpath, "r") as f:
                data = json.load(f)
            for node in data.get("nodes", []):
                nodes[node["node_id"]] = node
        except Exception:
            pass
    return nodes


def positional_encoding(nodes: dict, triage: dict) -> list:
    """Layer 1: Restore original document order and temporal sequence."""
    ordered = []
    assignments = triage.get("node_assignments", {})

    for node_id, node in nodes.items():
        assignment = assignments.get(node_id, {})
        ordered.append({
            "node_id": node_id,
            "source_file": node.get("source_file", ""),
            "position": node.get("position", 0),
            "content": node.get("content", ""),
            "content_type": node.get("content_type", ""),
            "token_count": node.get("token_count", 0),
            "domain": assignment.get("domain", "Reference & Archive"),
            "importance": assignment.get("importance", 3),
            "summary": assignment.get("summary", ""),
            "metadata": node.get("metadata", {}),
        })

    # Sort by source file then position (restoring document order)
    ordered.sort(key=lambda x: (x["source_file"], x["position"]))
    return ordered


def self_attention(ordered_nodes: list) -> dict:
    """Layer 2: Group nodes by semantic similarity within each domain."""
    domain_groups = defaultdict(lambda: defaultdict(list))

    for node in ordered_nodes:
        domain = node["domain"]
        # Sub-group by content type within domain
        ctype = node["content_type"]
        domain_groups[domain][ctype].append(node)

    # Within each sub-group, cluster by source file (semantic proximity)
    clustered = {}
    for domain, type_groups in domain_groups.items():
        clusters = []
        for ctype, nodes_list in type_groups.items():
            # Group by source file
            by_source = defaultdict(list)
            for n in nodes_list:
                by_source[n["source_file"]].append(n)

            for source, source_nodes in by_source.items():
                clusters.append({
                    "cluster_id": f"{domain}_{ctype}_{Path(source).stem}",
                    "content_type": ctype,
                    "source_file": source,
                    "node_count": len(source_nodes),
                    "total_tokens": sum(n["token_count"] for n in source_nodes),
                    "avg_importance": round(
                        sum(n["importance"] for n in source_nodes) / max(len(source_nodes), 1), 2
                    ),
                    "nodes": source_nodes,
                })

        # Sort clusters by importance
        clusters.sort(key=lambda x: -x["avg_importance"])
        clustered[domain] = clusters

    return clustered


def cross_attention(clustered: dict, cross_refs: list) -> dict:
    """Layer 3: Link nodes across domains that reference shared entities."""
    links = []
    for ref in cross_refs:
        entity = ref.get("entity", "")
        domains = ref.get("domains", [])
        node_ids = ref.get("node_ids", [])

        if len(domains) > 1:
            links.append({
                "entity": entity,
                "domains": domains,
                "strength": len(node_ids),
                "node_ids": node_ids[:20],  # Cap for size
            })

    return {
        "cross_domain_links": links[:200],
        "link_count": len(links),
        "most_connected_entities": [l["entity"] for l in links[:10]],
    }


def feed_forward(clustered: dict) -> dict:
    """Layer 4: Generate summaries, abstracts, and index entries per group."""
    domain_summaries = {}

    for domain, clusters in clustered.items():
        total_nodes = sum(c["node_count"] for c in clusters)
        total_tokens = sum(c["total_tokens"] for c in clusters)
        source_files = list(set(c["source_file"] for c in clusters))

        # Build content digest — first 200 chars of each cluster's top node
        digest_parts = []
        for cluster in clusters[:10]:  # Top 10 clusters
            if cluster["nodes"]:
                top_node = max(cluster["nodes"], key=lambda n: n["importance"])
                digest_parts.append(top_node.get("summary", top_node["content"][:200]))

        domain_summaries[domain] = {
            "total_nodes": total_nodes,
            "total_tokens": total_tokens,
            "cluster_count": len(clusters),
            "source_files": source_files,
            "source_file_count": len(source_files),
            "content_digest": digest_parts,
            "top_clusters": [
                {
                    "id": c["cluster_id"],
                    "type": c["content_type"],
                    "source": Path(c["source_file"]).name,
                    "nodes": c["node_count"],
                    "importance": c["avg_importance"],
                }
                for c in clusters[:5]
            ],
        }

    return domain_summaries


def output_projection(clustered: dict, domain_summaries: dict,
                      cross_links: dict, output_dir: str):
    """Layer 5: Format and save for each target database."""
    os.makedirs(output_dir, exist_ok=True)

    # 1. Knowledge graph
    graph = {"nodes": [], "edges": []}
    node_id_set = set()
    for domain, clusters in clustered.items():
        for cluster in clusters:
            for node in cluster["nodes"]:
                if node["node_id"] not in node_id_set:
                    graph["nodes"].append({
                        "id": node["node_id"],
                        "domain": domain,
                        "type": node["content_type"],
                        "importance": node["importance"],
                        "label": node.get("summary", node["content"][:80]),
                    })
                    node_id_set.add(node["node_id"])

    for link in cross_links.get("cross_domain_links", []):
        ids = link.get("node_ids", [])
        for i in range(len(ids) - 1):
            graph["edges"].append({
                "source": ids[i],
                "target": ids[i + 1],
                "entity": link["entity"],
                "weight": link["strength"],
            })

    with open(os.path.join(output_dir, "knowledge_graph.json"), "w") as f:
        json.dump(graph, f, indent=2)

    # 2. Domain index
    with open(os.path.join(output_dir, "domain_index.json"), "w") as f:
        json.dump(domain_summaries, f, indent=2)

    # 3. Cross references
    with open(os.path.join(output_dir, "cross_references.json"), "w") as f:
        json.dump(cross_links, f, indent=2)

    # 4. Per-domain directories with assembled content
    domains_dir = os.path.join(output_dir, "domains")
    os.makedirs(domains_dir, exist_ok=True)

    for domain, clusters in clustered.items():
        domain_slug = domain.lower().replace(" & ", "_").replace(" ", "_")
        domain_dir = os.path.join(domains_dir, domain_slug)
        os.makedirs(domain_dir, exist_ok=True)

        # Domain manifest
        manifest = {
            "domain": domain,
            "summary": domain_summaries.get(domain, {}),
            "clusters": [],
        }

        for cluster in clusters:
            # Save cluster content
            cluster_file = os.path.join(domain_dir, f"{cluster['cluster_id']}.json")
            with open(cluster_file, "w") as f:
                json.dump(cluster, f, indent=2, default=str)

            manifest["clusters"].append({
                "id": cluster["cluster_id"],
                "file": f"{cluster['cluster_id']}.json",
                "type": cluster["content_type"],
                "nodes": cluster["node_count"],
                "importance": cluster["avg_importance"],
            })

        with open(os.path.join(domain_dir, "_manifest.json"), "w") as f:
            json.dump(manifest, f, indent=2)

    # 5. Temporal timeline (placeholder — populated from node dates)
    timeline = []
    for domain, clusters in clustered.items():
        for cluster in clusters:
            for node in cluster["nodes"]:
                extracted_at = node.get("metadata", {}).get("date") or node.get("metadata", {}).get("modified", "")
                if extracted_at:
                    timeline.append({
                        "date": extracted_at,
                        "domain": domain,
                        "node_id": node["node_id"],
                        "summary": node.get("summary", node["content"][:100]),
                    })
    timeline.sort(key=lambda x: x.get("date", ""))
    with open(os.path.join(output_dir, "temporal_timeline.json"), "w") as f:
        json.dump(timeline, f, indent=2)

    # 6. Entity registry (from triage)
    # This is passed through from the triage report in the main flow

    print(f"  Knowledge graph: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges")
    print(f"  Domains: {len(clustered)}")
    print(f"  Timeline events: {len(timeline)}")


def main():
    parser = argparse.ArgumentParser(description="Reassemble knowledge from triage report")
    parser.add_argument("--triage", required=True, help="Path to triage_report.json")
    parser.add_argument("--nodes-dir", default=None, help="Path to nodes directory (optional, for full content)")
    parser.add_argument("--output-dir", required=True, help="Output directory for assembled knowledge")
    args = parser.parse_args()

    print("Loading triage report...")
    triage = load_triage(args.triage)

    # Load full nodes if available
    nodes = {}
    if args.nodes_dir and os.path.isdir(args.nodes_dir):
        print("Loading full nodes...")
        nodes = load_all_nodes(args.nodes_dir)
        print(f"  Loaded {len(nodes)} nodes")

    # If no full nodes, reconstruct minimal nodes from triage assignments
    if not nodes:
        print("Reconstructing nodes from triage assignments...")
        for node_id, assignment in triage.get("node_assignments", {}).items():
            nodes[node_id] = {
                "node_id": node_id,
                "source_file": "",
                "position": 0,
                "content": assignment.get("summary", ""),
                "content_type": "summary",
                "token_count": len(assignment.get("summary", "").split()),
                "metadata": {},
            }
        print(f"  Reconstructed {len(nodes)} nodes")

    print("\nLayer 1: Positional Encoding...")
    ordered = positional_encoding(nodes, triage)
    print(f"  Ordered {len(ordered)} nodes")

    print("Layer 2: Self-Attention (domain clustering)...")
    clustered = self_attention(ordered)
    for domain, clusters in clustered.items():
        total = sum(c["node_count"] for c in clusters)
        print(f"  {domain}: {len(clusters)} clusters, {total} nodes")

    print("Layer 3: Cross-Attention (inter-domain linking)...")
    cross_refs = triage.get("cross_references", [])
    cross_links = cross_attention(clustered, cross_refs)
    print(f"  {cross_links['link_count']} cross-domain links")

    print("Layer 4: Feed-Forward (summaries & indexing)...")
    domain_summaries = feed_forward(clustered)

    print("Layer 5: Output Projection...")
    output_projection(clustered, domain_summaries, cross_links, args.output_dir)

    # Save entity registry from triage
    entity_reg = triage.get("entity_registry", {})
    with open(os.path.join(args.output_dir, "entity_registry.json"), "w") as f:
        json.dump(entity_reg, f, indent=2)
    print(f"  Entity registry: {len(entity_reg)} entities")

    print(f"\nReassembly complete. Output: {args.output_dir}")


if __name__ == "__main__":
    main()
