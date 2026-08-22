#!/usr/bin/env python3
"""
Universal File Triage & Data Warehouse Agent

Traverses directories, computes SHA-256 hashes, eliminates duplicates,
and constructs a unified catalog for BigQuery ingestion.

Features:
- Recursive directory traversal
- SHA-256 hash computation for all files
- Duplicate detection and elimination
- Unified catalog generation (JSON/CSV)
- Standardized directory restructuring
- Vector embedding preparation for semantic search

Usage:
    python3 file_catalog.py --root /path/to/directory --output catalog.json
    python3 file_catalog.py --root /path/to/directory --restructure --catalog catalog.json

Requirements:
    pip install hashlib pathlib
"""

import argparse
import hashlib
import json
import os
import sys
import csv
import logging
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('file_triage.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Standardized directory structure
STANDARD_DIRS = {
    "01_CORPUS": ["*.md", "*.txt", "*.pdf", "*.docx", "*.doc"],
    "02_CHATS": ["*.json", "*.csv"],  # AI conversations, exports
    "03_FINANCES": ["*.xlsx", "*.xls", "*.csv", "*.pdf"],  # Financial documents
    "04_EXTRACTS": ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.tiff"],  # Images, scans
    "05_ARCHIVE": [],  # Everything else
}

# Category mapping based on file content/name patterns
CATEGORY_PATTERNS = {
    "legal": ["complaint", "petition", "answer", "motion", "brief", "evidence", 
              "deposition", "interrogatory", "subpoena", "affidavit", "exhibit"],
    "financial": ["ledger", "invoice", "receipt", "statement", "bank", "wire", 
                  "zelle", "transfer", "earnings", "damages", "schedule"],
    "medical": ["patient", "chart", "diagnosis", "treatment", "ICD", "PICC", 
                "Brugada", "FMLA", "HIPAA", "ACGME", "residency"],
    "business": ["business", "model", "plan", "proposal", "network", "supply", 
                 "pharma", "zakat", "bait-ul-mal", "generic", "distribution"],
    "personal": ["family", "dad", "mother", "father", "Quran", "Islamic", 
                 "Nafaqah", "Wilayah", "qard", "debt", "agreement"],
    "technical": ["code", "script", "config", "requirements", "python", "automation"],
    "daily": ["daily", "note", "journal", "priority", "matrix", "Eisenhower"],
}


class FileCatalog:
    """Main catalog class for file triage operations."""
    
    def __init__(self, root_dir, output_dir="./triage_output"):
        self.root_dir = Path(root_dir)
        self.output_dir = Path(output_dir)
        self.catalog = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "root_directory": str(self.root_dir),
                "total_files": 0,
                "total_size_bytes": 0,
                "duplicate_files": 0,
                "unique_files": 0,
            },
            "files": [],
            "duplicates": defaultdict(list),
            "categories": defaultdict(list),
        }
        
        os.makedirs(self.output_dir, exist_ok=True)
    
    def compute_sha256(self, file_path):
        """Compute SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        
        try:
            with open(file_path, "rb") as f:
                # Read in chunks to handle large files
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            logger.error(f"Error computing hash for {file_path}: {e}")
            return None
    
    def get_file_info(self, file_path):
        """Get comprehensive file information."""
        stat = os.stat(file_path)
        
        return {
            "path": str(file_path),
            "relative_path": str(file_path.relative_to(self.root_dir)),
            "filename": file_path.name,
            "extension": file_path.suffix.lower() if file_path.suffix else "",
            "size_bytes": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
        }
    
    def categorize_file(self, file_path, filename):
        """Categorize file based on name and content patterns."""
        categories = []
        filename_lower = filename.lower()
        
        for category, patterns in CATEGORY_PATTERNS.items():
            for pattern in patterns:
                if pattern in filename_lower:
                    categories.append(category)
                    break
        
        # If no category matched, use extension-based categorization
        if not categories:
            ext = file_path.suffix.lower()
            if ext in ['.md', '.txt']:
                categories.append("document")
            elif ext in ['.pdf', '.docx', '.doc']:
                categories.append("document")
            elif ext in ['.jpg', '.jpeg', '.png', '.gif']:
                categories.append("image")
            elif ext in ['.xlsx', '.xls', '.csv']:
                categories.append("spreadsheet")
            elif ext in ['.json']:
                categories.append("data")
            else:
                categories.append("other")
        
        return categories if categories else ["uncategorized"]
    
    def scan_directory(self, dir_path=None):
        """Recursively scan directory and catalog files."""
        if dir_path is None:
            dir_path = self.root_dir
        
        dir_path = Path(dir_path)
        
        for item in dir_path.iterdir():
            if item.is_file():
                self.process_file(item)
            elif item.is_dir():
                # Skip hidden directories and common system directories
                if item.name.startswith('.') or item.name in ['__pycache__', 'node_modules', '.git']:
                    continue
                self.scan_directory(item)
    
    def process_file(self, file_path):
        """Process a single file: compute hash, categorize, add to catalog."""
        file_info = self.get_file_info(file_path)
        
        # Compute hash
        file_hash = self.compute_sha256(file_path)
        if file_hash is None:
            logger.warning(f"Skipping {file_path} - could not compute hash")
            return
        
        file_info["sha256"] = file_hash
        
        # Categorize
        categories = self.categorize_file(file_path, file_path.name)
        file_info["categories"] = categories
        
        # Add to catalog
        self.catalog["files"].append(file_info)
        self.catalog["metadata"]["total_files"] += 1
        self.catalog["metadata"]["total_size_bytes"] += file_info["size_bytes"]
        
        # Track by hash for duplicate detection
        self.catalog["duplicates"][file_hash].append(file_info["path"])
        
        # Track by category
        for category in categories:
            self.catalog["categories"][category].append(file_info["path"])
        
        logger.info(f"Processed: {file_info['relative_path']} ({file_info['size_mb']} MB)")
    
    def identify_duplicates(self):
        """Identify duplicate files based on SHA-256 hashes."""
        duplicates = {}
        
        for hash_val, paths in self.catalog["duplicates"].items():
            if len(paths) > 1:
                duplicates[hash_val] = {
                    "hash": hash_val,
                    "count": len(paths),
                    "paths": paths,
                    "size_bytes": os.path.getsize(paths[0]) if os.path.exists(paths[0]) else 0
                }
        
        self.catalog["metadata"]["duplicate_files"] = len(duplicates)
        self.catalog["metadata"]["unique_files"] = self.catalog["metadata"]["total_files"] - len(duplicates)
        
        return duplicates
    
    def generate_catalog(self, format="json"):
        """Generate catalog in specified format."""
        # First identify duplicates
        self.identify_duplicates()
        
        if format == "json":
            output_path = self.output_dir / "file_catalog.json"
            with open(output_path, 'w') as f:
                json.dump(self.catalog, f, indent=2)
            
        elif format == "csv":
            output_path = self.output_dir / "file_catalog.csv"
            with open(output_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "path", "relative_path", "filename", "extension", 
                    "size_bytes", "size_mb", "sha256", "categories",
                    "created", "modified", "accessed"
                ])
                writer.writeheader()
                writer.writerows(self.catalog["files"])
        
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return output_path
    
    def restructure_files(self, standard_dirs=None):
        """Restructure files into standardized directory structure."""
        if standard_dirs is None:
            standard_dirs = STANDARD_DIRS
        
        # Create target directories
        target_base = self.output_dir / "restructured"
        os.makedirs(target_base, exist_ok=True)
        
        for dir_name in standard_dirs.keys():
            os.makedirs(target_base / dir_name, exist_ok=True)
        
        # Move files
        moved_count = 0
        skipped_count = 0
        
        for file_info in self.catalog["files"]:
            file_path = Path(file_info["path"])
            ext = file_info["extension"].lower()
            
            # Find appropriate directory based on extension
            target_dir = None
            for dir_name, exts in standard_dirs.items():
                if ext in exts or not exts:  # Empty list means catch-all
                    target_dir = target_base / dir_name
                    break
            
            if target_dir is None:
                target_dir = target_base / "05_ARCHIVE"
            
            # Determine target path (preserve relative structure if possible)
            rel_path = file_path.relative_to(self.root_dir)
            
            # For files in subdirectories, preserve structure within target dir
            if len(rel_path.parts) > 1:
                subdirs = Path(*rel_path.parts[:-1])
                target_subdir = target_dir / subdirs
                os.makedirs(target_subdir, exist_ok=True)
                target_path = target_subdir / file_path.name
            else:
                target_path = target_dir / file_path.name
            
            # Handle duplicates by appending timestamp
            if target_path.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                target_path = target_path.with_name(
                    f"{target_path.stem}_{timestamp}{target_path.suffix}"
                )
            
            # Move file
            try:
                import shutil
                shutil.copy2(file_path, target_path)
                # Optionally: os.remove(file_path) to actually move instead of copy
                moved_count += 1
                logger.info(f"Moved: {file_info['relative_path']} -> {target_path.relative_to(target_base)}")
            except Exception as e:
                logger.error(f"Error moving {file_path}: {e}")
                skipped_count += 1
        
        # Generate restructuring report
        report = {
            "restructured_at": datetime.now().isoformat(),
            "target_directory": str(target_base),
            "files_moved": moved_count,
            "files_skipped": skipped_count,
            "directory_structure": standard_dirs,
        }
        
        report_path = target_base / "_RESTUCTURING_REPORT.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def generate_duplicate_report(self):
        """Generate report of duplicate files."""
        duplicates = self.identify_duplicates()
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_duplicates": len(duplicates),
            "duplicate_groups": []
        }
        
        for hash_val, dup_info in duplicates.items():
            report["duplicate_groups"].append({
                "sha256": hash_val,
                "count": dup_info["count"],
                "size_bytes": dup_info["size_bytes"],
                "size_mb": round(dup_info["size_bytes"] / (1024 * 1024), 2),
                "files": [
                    {
                        "path": p,
                        "relative": str(Path(p).relative_to(self.root_dir))
                    }
                    for p in dup_info["paths"]
                ]
            })
        
        report_path = self.output_dir / "duplicate_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def generate_bigquery_schema(self):
        """Generate BigQuery schema for catalog ingestion."""
        schema = [
            {"name": "path", "type": "STRING", "mode": "REQUIRED"},
            {"name": "relative_path", "type": "STRING", "mode": "NULLABLE"},
            {"name": "filename", "type": "STRING", "mode": "REQUIRED"},
            {"name": "extension", "type": "STRING", "mode": "NULLABLE"},
            {"name": "size_bytes", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "size_mb", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "sha256", "type": "STRING", "mode": "REQUIRED"},
            {"name": "created", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "modified", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "accessed", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "categories", "type": "STRING", "mode": "REPEATED"},
            {"name": "content_text", "type": "STRING", "mode": "NULLABLE"},
            {"name": "embedding", "type": "FLOAT", "mode": "REPEATED"},
        ]
        
        schema_path = self.output_dir / "bigquery_schema.json"
        with open(schema_path, 'w') as f:
            json.dump(schema, f, indent=2)
        
        return schema


def main():
    parser = argparse.ArgumentParser(
        description="Universal File Triage & Data Warehouse Agent"
    )
    parser.add_argument(
        "--root", 
        default=".",
        help="Root directory to scan"
    )
    parser.add_argument(
        "--output", 
        default="./triage_output",
        help="Output directory for catalog and reports"
    )
    parser.add_argument(
        "--format", 
        choices=["json", "csv", "both"],
        default="both",
        help="Output format for catalog"
    )
    parser.add_argument(
        "--restructure", 
        action="store_true",
        help="Restructure files into standardized directories"
    )
    parser.add_argument(
        "--duplicates", 
        action="store_true",
        help="Generate duplicate report"
    )
    parser.add_argument(
        "--bigquery-schema", 
        action="store_true",
        help="Generate BigQuery schema"
    )
    
    args = parser.parse_args()
    
    # Initialize catalog
    catalog = FileCatalog(args.root, args.output)
    
    logger.info(f"Scanning directory: {args.root}")
    
    # Scan files
    catalog.scan_directory()
    
    logger.info(f"Found {catalog.catalog['metadata']['total_files']} files")
    
    # Generate outputs
    if args.format in ["json", "both"]:
        catalog.generate_catalog("json")
    
    if args.format in ["csv", "both"]:
        catalog.generate_catalog("csv")
    
    if args.duplicates:
        catalog.generate_duplicate_report()
    
    if args.bigquery_schema:
        catalog.generate_bigquery_schema()
    
    if args.restructure:
        catalog.restructure_files()
    
    logger.info("File triage complete!")


if __name__ == "__main__":
    main()
