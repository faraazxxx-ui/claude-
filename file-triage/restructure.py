#!/usr/bin/env python3
"""
File Restructuring Script

Restructures files from the repository into standardized top-level directories:
- 01_CORPUS: Core documents (MD, TXT, PDF, DOCX)
- 02_CHATS: AI conversations and chat exports
- 03_FINANCES: Financial documents and ledgers
- 04_EXTRACTS: Images, scans, and extracted content
- 05_ARCHIVE: Everything else

Usage:
    python3 restructure.py --dry-run  # Preview changes
    python3 restructure.py --execute  # Execute restructuring

Requirements:
    pip install pathlib
"""

import argparse
import os
import shutil
import json
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('restructure.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Category definitions with file patterns
CATEGORIES = {
    "01_CORPUS": {
        "description": "Core documents, reports, and structured content",
        "extensions": [".md", ".txt", ".pdf", ".docx", ".doc", ".rtf"],
        "patterns": [
            "report", "analysis", "synthesis", "briefing", "document",
            "case", "legal", "medical", "clinical", "strategy"
        ],
        "exclude_patterns": ["export", "chat", "conversation", "transcript"]
    },
    "02_CHATS": {
        "description": "AI conversations, chat exports, and transcripts",
        "extensions": [".json", ".csv", ".md", ".txt"],
        "patterns": [
            "chat", "conversation", "ai", "claude", "grok", "gemini",
            "export", "transcript", "pactify", "notebooklm"
        ],
        "exclude_patterns": []
    },
    "03_FINANCES": {
        "description": "Financial documents, ledgers, and economic data",
        "extensions": [".xlsx", ".xls", ".csv", ".pdf", ".md", ".txt"],
        "patterns": [
            "finance", "ledger", "damage", "schedule", "earning",
            "wire", "zelle", "bank", "invoice", "receipt", "transfer",
            "qard", "debt", "nafaqah", "wilayah"
        ],
        "exclude_patterns": []
    },
    "04_EXTRACTS": {
        "description": "Images, scans, charts, and visual content",
        "extensions": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".svg"],
        "patterns": ["chart", "graph", "scan", "image", "diagram", "figure"],
        "exclude_patterns": []
    },
    "05_ARCHIVE": {
        "description": "Everything else",
        "extensions": [],
        "patterns": [],
        "exclude_patterns": []
    }
}

# Directories to skip
SKIP_DIRS = [
    ".git", "__pycache__", "node_modules", ".vscode", ".idea",
    "01_CORPUS", "02_CHATS", "03_FINANCES", "04_EXTRACTS", "05_ARCHIVE",
    "file-triage", "scanner-config", "daily-workflow-optimizer"
]


class FileRestructurer:
    """Handles file restructuring operations."""
    
    def __init__(self, root_dir=".", dry_run=True):
        self.root_dir = Path(root_dir)
        self.dry_run = dry_run
        self.stats = {
            "total_files": 0,
            "moved": 0,
            "skipped": 0,
            "by_category": {cat: 0 for cat in CATEGORIES.keys()}
        }
        self.move_plan = []
    
    def categorize_file(self, file_path):
        """Determine which category a file belongs to."""
        filename = file_path.name.lower()
        
        # Check each category in order of priority
        for category, config in CATEGORIES.items():
            ext = file_path.suffix.lower()
            
            # Check extension
            if ext in config["extensions"]:
                # Check exclude patterns
                if any(pattern in filename for pattern in config.get("exclude_patterns", [])):
                    continue
                return category
            
            # Check filename patterns
            if any(pattern in filename for pattern in config.get("patterns", [])):
                return category
        
        # Default to ARCHIVE
        return "05_ARCHIVE"
    
    def get_target_path(self, file_path):
        """Get target path for a file based on its category."""
        category = self.categorize_file(file_path)
        
        # Get relative path from root
        rel_path = file_path.relative_to(self.root_dir)
        
        # For files in subdirectories, preserve structure within category
        if len(rel_path.parts) > 1:
            # Skip the first part (current directory)
            subdirs = Path(*rel_path.parts[1:-1]) if len(rel_path.parts) > 2 else Path()
            target = self.root_dir / category / subdirs / file_path.name
        else:
            target = self.root_dir / category / file_path.name
        
        return target, category
    
    def scan_files(self):
        """Scan all files and create move plan."""
        logger.info(f"Scanning directory: {self.root_dir}")
        
        for item in self.root_dir.rglob("*"):
            if item.is_file():
                # Skip files in target directories or skip directories
                if any(skip_dir in item.parts for skip_dir in SKIP_DIRS):
                    continue
                
                self.stats["total_files"] += 1
                
                # Get target path
                target, category = self.get_target_path(item)
                
                # Only add to plan if source != target
                if str(item) != str(target):
                    self.move_plan.append({
                        "source": str(item),
                        "target": str(target),
                        "category": category
                    })
                    self.stats["by_category"][category] += 1
                else:
                    self.stats["skipped"] += 1
        
        logger.info(f"Found {self.stats['total_files']} files")
        logger.info(f"Created move plan with {len(self.move_plan)} moves")
        
        return self.move_plan
    
    def execute_plan(self):
        """Execute the move plan."""
        if self.dry_run:
            logger.info("DRY RUN: Would perform the following moves:")
            for i, move in enumerate(self.move_plan[:20], 1):  # Show first 20
                logger.info(f"  {i}. {move['source']} -> {move['target']}")
            if len(self.move_plan) > 20:
                logger.info(f"  ... and {len(self.move_plan) - 20} more")
            return
        
        logger.info("Executing move plan...")
        
        for move in self.move_plan:
            source = Path(move["source"])
            target = Path(move["target"])
            
            try:
                # Create parent directories
                target.parent.mkdir(parents=True, exist_ok=True)
                
                # Handle duplicate filenames
                if target.exists():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    target = target.with_name(f"{target.stem}_{timestamp}{target.suffix}")
                
                # Move file
                shutil.move(str(source), str(target))
                self.stats["moved"] += 1
                
                if self.stats["moved"] % 10 == 0:
                    logger.info(f"Moved {self.stats['moved']} files...")
                
            except Exception as e:
                logger.error(f"Error moving {source} to {target}: {e}")
        
        logger.info(f"Restructuring complete!")
        logger.info(f"Total files: {self.stats['total_files']}")
        logger.info(f"Moved: {self.stats['moved']}")
        logger.info(f"Skipped: {self.stats['skipped']}")
        logger.info(f"By category:")
        for category, count in self.stats["by_category"].items():
            logger.info(f"  {category}: {count}")
    
    def save_plan(self, output_path):
        """Save move plan to JSON file."""
        plan_data = {
            "generated_at": datetime.now().isoformat(),
            "root_directory": str(self.root_dir),
            "dry_run": self.dry_run,
            "stats": self.stats,
            "moves": self.move_plan
        }
        
        with open(output_path, 'w') as f:
            json.dump(plan_data, f, indent=2)
        
        logger.info(f"Move plan saved to {output_path}")
        return output_path
    
    def load_plan(self, input_path):
        """Load move plan from JSON file."""
        with open(input_path, 'r') as f:
            plan_data = json.load(f)
        
        self.root_dir = Path(plan_data["root_directory"])
        self.dry_run = plan_data.get("dry_run", True)
        self.stats = plan_data.get("stats", self.stats)
        self.move_plan = plan_data.get("moves", [])
        
        logger.info(f"Move plan loaded from {input_path}")
        return self.move_plan


def main():
    parser = argparse.ArgumentParser(
        description="File Restructuring Script - Organize files into standardized directories"
    )
    parser.add_argument(
        "--root", 
        default=".",
        help="Root directory to restructure"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        default=True,
        help="Preview changes without moving files (default)"
    )
    parser.add_argument(
        "--execute", 
        action="store_true",
        help="Execute restructuring (actually move files)"
    )
    parser.add_argument(
        "--save-plan", 
        type=str,
        default="move_plan.json",
        help="Save move plan to JSON file"
    )
    parser.add_argument(
        "--load-plan", 
        type=str,
        help="Load move plan from JSON file"
    )
    
    args = parser.parse_args()
    
    # Determine if we're executing or dry-running
    dry_run = not args.execute
    
    # Initialize restructurer
    restructurer = FileRestructurer(args.root, dry_run)
    
    if args.load_plan:
        # Load existing plan
        restructurer.load_plan(args.load_plan)
    else:
        # Scan and create new plan
        restructurer.scan_files()
    
    # Save plan if requested
    if args.save_plan:
        restructurer.save_plan(args.save_plan)
    
    # Execute or preview
    restructurer.execute_plan()


if __name__ == "__main__":
    main()
