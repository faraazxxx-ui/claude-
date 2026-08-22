#!/usr/bin/env python3
"""
Brother Duplex Scanner Directory Watcher

Watches a designated directory for scanned documents from Brother scanner,
auto-performs OCR on PDFs/images, isolates highlighted excerpts, and
matches them with companion audio dictations.

Features:
- Monitors directory for new files (PDF, JPEG, PNG)
- Auto-OCR using Tesseract for text extraction
- Detects highlighted text (yellow, green, pink) using color filtering
- Matches scanned documents with audio files (MP3, WAV, M4A) by timestamp
- Outputs structured markdown with OCR text + highlights + audio transcript

Usage:
    python3 brother_scanner_watcher.py --watch /path/to/scans --output /path/to/processed

Requirements:
    pip install watchdog Pillow pytesseract opencv-python numpy
    apt install tesseract-ocr libtesseract-dev (Linux)
    brew install tesseract (Mac)
"""

import argparse
import os
import re
import sys
import time
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Optional audio transcription (requires additional dependencies)
try:
    import speech_recognition as sr
    AUDIO_SUPPORT = True
except ImportError:
    AUDIO_SUPPORT = False
    logging.warning("speech_recognition not installed. Audio matching disabled.")

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    import cv2
    import numpy as np
    from PIL import Image
    import pytesseract
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install: pip install watchdog opencv-python Pillow pytesseract")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scanner_watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
CONFIG = {
    "watch_dir": "./scans",
    "output_dir": "./processed",
    "archive_dir": "./archive",
    "audio_dir": "./audio",
    "highlight_colors": {
        "yellow": ([200, 255], [100, 150], [0, 100]),    # BGR ranges for yellow
        "green": ([0, 100], [100, 255], [0, 100]),      # Green
        "pink": ([200, 255], [0, 100], [150, 255]),     # Pink
    },
    "timestamp_window": 300,  # 5 minutes to match audio with scan
    "ocr_lang": "eng",
    "min_file_age": 2,  # seconds to wait before processing (avoid partial writes)
}


class ScannerHandler(FileSystemEventHandler):
    """Handles file creation events in watched directory."""
    
    def __init__(self, config):
        self.config = config
        self.processed_files = set()
        self.audio_files = {}
        
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            logger.info(f"Detected new file: {file_path}")
            
            # Wait for file to finish writing
            time.sleep(self.config["min_file_age"])
            
            if os.path.exists(file_path):
                self.process_file(file_path)
    
    def process_file(self, file_path):
        """Process a newly created file based on its type."""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in ['.pdf', '.jpg', '.jpeg', '.png', '.tiff']:
            logger.info(f"Processing scanned document: {file_path}")
            self.process_scan(file_path)
        elif ext in ['.mp3', '.wav', '.m4a', '.ogg'] and AUDIO_SUPPORT:
            logger.info(f"Processing audio file: {file_path}")
            self.process_audio(file_path)
        else:
            logger.debug(f"Ignoring file with extension {ext}: {file_path}")
    
    def process_scan(self, file_path):
        """Process a scanned document: OCR + highlight extraction."""
        try:
            # Extract base filename without extension
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            timestamp = datetime.fromtimestamp(os.path.getmtime(file_path))
            
            # Convert to images if PDF
            if file_path.lower().endswith('.pdf'):
                images = self.pdf_to_images(file_path)
            else:
                images = [file_path]
            
            # Process each page
            full_text = ""
            highlights = {}
            
            for i, img_path in enumerate(images):
                page_text, page_highlights = self.process_image(img_path)
                full_text += f"\n\n--- PAGE {i+1} ---\n\n{page_text}"
                highlights[f"page_{i+1}"] = page_highlights
            
            # Create output markdown
            output_path = os.path.join(
                self.config["output_dir"],
                f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{base_name}.md"
            )
            
            self.create_scan_markdown(
                file_path, output_path, full_text, highlights, timestamp
            )
            
            # Archive original
            archive_path = os.path.join(
                self.config["archive_dir"],
                timestamp.strftime('%Y%m%d'),
                os.path.basename(file_path)
            )
            os.makedirs(os.path.dirname(archive_path), exist_ok=True)
            os.rename(file_path, archive_path)
            
            logger.info(f"Processed scan: {file_path} -> {output_path}")
            
            # Check for matching audio
            self.match_audio_with_scan(output_path, timestamp)
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
    
    def process_audio(self, file_path):
        """Process an audio file: transcribe and store for matching."""
        try:
            timestamp = datetime.fromtimestamp(os.path.getmtime(file_path))
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            
            # Transcribe audio
            transcript = self.transcribe_audio(file_path)
            
            if transcript:
                # Store audio info for matching
                self.audio_files[file_path] = {
                    "timestamp": timestamp,
                    "transcript": transcript,
                    "duration": self.get_audio_duration(file_path)
                }
                
                # Save transcript
                output_path = os.path.join(
                    self.config["output_dir"],
                    f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{base_name}_AUDIO.md"
                )
                
                with open(output_path, 'w') as f:
                    f.write(f"# Audio Transcript: {base_name}\n\n")
                    f.write(f"**Timestamp:** {timestamp}\n\n")
                    f.write(f"**Duration:** {self.audio_files[file_path]['duration']}s\n\n")
                    f.write(f"---\n\n{transcript}\n")
                
                # Archive original
                archive_path = os.path.join(
                    self.config["archive_dir"],
                    timestamp.strftime('%Y%m%d'),
                    os.path.basename(file_path)
                )
                os.makedirs(os.path.dirname(archive_path), exist_ok=True)
                os.rename(file_path, archive_path)
                
                logger.info(f"Processed audio: {file_path}")
        except Exception as e:
            logger.error(f"Error processing audio {file_path}: {e}")
    
    def process_image(self, img_path):
        """Process a single image: OCR + highlight detection."""
        # Open image
        if isinstance(img_path, str):
            img = cv2.imread(img_path)
        else:
            img = img_path
        
        if img is None:
            raise ValueError(f"Could not read image: {img_path}")
        
        # Convert to RGB for OCR
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Perform OCR
        text = pytesseract.image_to_string(rgb_img, lang=self.config["ocr_lang"])
        
        # Detect highlights
        highlights = self.detect_highlights(img)
        
        return text, highlights
    
    def pdf_to_images(self, pdf_path):
        """Convert PDF to list of image paths."""
        # Simple implementation using pdf2image if available
        try:
            from pdf2image import convert_from_path
            images = convert_from_path(pdf_path)
            
            # Save as temporary PNGs
            temp_dir = os.path.join(self.config["output_dir"], "temp")
            os.makedirs(temp_dir, exist_ok=True)
            
            image_paths = []
            for i, img in enumerate(images):
                temp_path = os.path.join(temp_dir, f"{os.path.basename(pdf_path)}_{i}.png")
                img.save(temp_path, 'PNG')
                image_paths.append(temp_path)
            
            return image_paths
        except ImportError:
            logger.warning("pdf2image not installed. Processing first page only.")
            # Fallback: process first page by converting PDF to image
            # This is a simplified approach - in production, use pdf2image
            return [pdf_path]  # Will need proper PDF handling
    
    def detect_highlights(self, img):
        """Detect highlighted text regions in an image."""
        highlights = {}
        
        for color_name, (b_range, g_range, r_range) in self.config["highlight_colors"].items():
            # Create mask for this highlight color
            lower = np.array([b_range[0], g_range[0], r_range[0]])
            upper = np.array([b_range[1], g_range[1], r_range[1]])
            
            mask = cv2.inRange(img, lower, upper)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for i, contour in enumerate(contours):
                # Filter small regions
                area = cv2.contourArea(contour)
                if area < 100:  # Minimum area threshold
                    continue
                
                # Get bounding box
                x, y, w, h = cv2.boundingRect(contour)
                
                # Extract region of interest
                roi = img[y:y+h, x:x+w]
                
                # Perform OCR on highlighted region
                roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
                highlighted_text = pytesseract.image_to_string(roi_rgb, lang=self.config["ocr_lang"])
                
                if highlighted_text.strip():
                    key = f"{color_name}_{i}"
                    highlights[key] = {
                        "color": color_name,
                        "text": highlighted_text.strip(),
                        "region": {"x": x, "y": y, "width": w, "height": h}
                    }
        
        return highlights
    
    def transcribe_audio(self, audio_path):
        """Transcribe audio file to text."""
        if not AUDIO_SUPPORT:
            return ""
        
        recognizer = sr.Recognizer()
        
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                return text
            except sr.UnknownValueError:
                logger.warning(f"Could not understand audio: {audio_path}")
                return ""
            except sr.RequestError as e:
                logger.error(f"API error transcribing {audio_path}: {e}")
                return ""
    
    def get_audio_duration(self, audio_path):
        """Get duration of audio file in seconds."""
        try:
            with sr.AudioFile(audio_path) as source:
                recognizer = sr.Recognizer()
                audio_data = recognizer.record(source)
                return len(audio_data.get_raw_data()) / (
                    audio_data.sample_width * audio_data.sample_rate
                )
        except:
            return 0
    
    def match_audio_with_scan(self, scan_output_path, scan_timestamp):
        """Match scanned document with audio files based on timestamp."""
        scan_base = os.path.basename(scan_output_path)
        
        for audio_path, audio_data in list(self.audio_files.items()):
            audio_timestamp = audio_data["timestamp"]
            
            # Check if audio is within matching window
            time_diff = abs((scan_timestamp - audio_timestamp).total_seconds())
            
            if time_diff <= self.config["timestamp_window"]:
                # Found matching audio
                audio_output = os.path.join(
                    self.config["output_dir"],
                    os.path.basename(audio_path).replace('.md', '_MATCHED.md')
                )
                
                # Append audio transcript to scan markdown
                with open(scan_output_path, 'a') as f:
                    f.write(f"\n\n---\n\n")
                    f.write(f"## 🎙️ Matched Audio Dictation\n\n")
                    f.write(f"**Audio File:** {os.path.basename(audio_path)}\n\n")
                    f.write(f"**Time Difference:** {time_diff:.1f} seconds\n\n")
                    f.write(f"**Transcript:**\n\n{audio_data['transcript']}\n")
                
                logger.info(f"Matched audio {audio_path} with scan {scan_output_path}")
                
                # Remove from pending audio files
                del self.audio_files[audio_path]
                
                break  # Match one audio per scan
    
    def create_scan_markdown(self, source_path, output_path, full_text, highlights, timestamp):
        """Create structured markdown file for processed scan."""
        base_name = os.path.splitext(os.path.basename(source_path))[0]
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            # Header
            f.write(f"---\n")
            f.write(f"source: {source_path}\n")
            f.write(f"scanned: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"type: scan\n")
            f.write(f"tags: [scanned, ocr, brother]\n")
            f.write(f"---\n\n")
            
            # Title
            f.write(f"# {base_name}\n\n")
            f.write(f"*Scanned: {timestamp.strftime('%B %d, %Y at %I:%M %p')}*\n\n")
            
            # Full OCR Text
            f.write(f"## 📄 Full Text\n\n")
            f.write(f"```\n{full_text}\n```\n\n")
            
            # Highlights Section
            if highlights:
                f.write(f"## 🟡 Highlighted Excerpts\n\n")
                f.write(f"*Automatically detected highlighted text*\n\n")
                
                for page_name, page_highlights in highlights.items():
                    if page_highlights:
                        f.write(f"### {page_name.replace('_', ' ').title()}\n\n")
                        for highlight_id, highlight_data in page_highlights.items():
                            color_emoji = {
                                "yellow": "🟡",
                                "green": "🟢",
                                "pink": "🟣"
                            }.get(highlight_data["color"], "⚪")
                            
                            f.write(f"{color_emoji} **{highlight_data['color'].title()} Highlight:**\n\n")
                            f.write(f"> {highlight_data['text']}\n\n")
                        f.write(f"\n")
            
            # Metadata
            f.write(f"---\n\n")
            f.write(f"*Processed by Brother Scanner Watcher v1.0*\n")


class BrotherScannerWatcher:
    """Main watcher class."""
    
    def __init__(self, config):
        self.config = config
        self.observer = None
        self.handler = ScannerHandler(config)
    
    def start(self):
        """Start watching the directory."""
        # Create necessary directories
        for dir_key in ['output_dir', 'archive_dir', 'audio_dir']:
            os.makedirs(self.config.get(dir_key, '.'), exist_ok=True)
        
        # Start observer
        self.observer = Observer()
        self.observer.schedule(self.handler, self.config['watch_dir'], recursive=False)
        self.observer.start()
        
        logger.info(f"Watching directory: {self.config['watch_dir']}")
        logger.info(f"Output directory: {self.config['output_dir']}")
        logger.info(f"Archive directory: {self.config['archive_dir']}")
    
    def stop(self):
        """Stop watching."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
    
    def run(self):
        """Run the watcher until interrupted."""
        try:
            self.start()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
            logger.info("Watcher stopped by user")


def load_config(config_path=None):
    """Load configuration from file or use defaults."""
    config = CONFIG.copy()
    
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            custom_config = json.load(f)
            config.update(custom_config)
    
    # Ensure paths are absolute
    for key in ['watch_dir', 'output_dir', 'archive_dir', 'audio_dir']:
        if config.get(key):
            config[key] = os.path.abspath(config[key])
    
    return config


def main():
    parser = argparse.ArgumentParser(
        description="Brother Scanner Directory Watcher - Auto-OCR and Audio Matching"
    )
    parser.add_argument(
        "--watch", 
        default="./scans",
        help="Directory to watch for scanned documents"
    )
    parser.add_argument(
        "--output", 
        default="./processed",
        help="Directory for processed output"
    )
    parser.add_argument(
        "--archive", 
        default="./archive",
        help="Directory to archive original files"
    )
    parser.add_argument(
        "--audio", 
        default="./audio",
        help="Directory to watch for audio dictations"
    )
    parser.add_argument(
        "--config", 
        default="scanner_config.json",
        help="Path to JSON configuration file"
    )
    
    args = parser.parse_args()
    
    # Build config
    config = load_config(args.config)
    config.update({
        "watch_dir": args.watch,
        "output_dir": args.output,
        "archive_dir": args.archive,
        "audio_dir": args.audio,
    })
    
    # Create watcher
    watcher = BrotherScannerWatcher(config)
    
    # Also watch audio directory
    if AUDIO_SUPPORT and args.audio:
        audio_watcher = BrotherScannerWatcher(config)
        audio_watcher.config['watch_dir'] = args.audio
        audio_watcher.start()
    
    # Run
    watcher.run()


if __name__ == "__main__":
    main()
