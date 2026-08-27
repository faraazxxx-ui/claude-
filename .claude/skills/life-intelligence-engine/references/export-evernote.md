# Export to Evernote

## Table of Contents
1. ENEX Format Overview
2. Notebook Structure
3. Export Script
4. Import Instructions

## ENEX Format Overview

Evernote uses ENEX (Evernote Export) XML format for bulk import. Each note is
an `<en-note>` element containing XHTML content.

Basic ENEX structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
<en-export export-date="20260415T120000Z" application="Life Intelligence Engine">
  <note>
    <title>Note Title</title>
    <content><![CDATA[<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note>
  <h2>Content here</h2>
  <p>Paragraph text...</p>
</en-note>]]></content>
    <created>20260415T120000Z</created>
    <updated>20260415T120000Z</updated>
    <tag>domain-name</tag>
    <tag>content-type</tag>
    <note-attributes>
      <source>life-intelligence-engine</source>
      <source-url>file:///original/path</source-url>
    </note-attributes>
  </note>
</en-export>
```

## Notebook Structure

Create one ENEX file per domain (Evernote notebook):

```
evernote-export/
├── Career_Work.enex
├── Finance_Legal.enex
├── Health_Wellness.enex
├── Learning_Education.enex
├── Personal_Identity.enex
├── Creative_Projects.enex
├── Relationships_Social.enex
├── Home_Logistics.enex
├── Digital_Technical.enex
├── Reference_Archive.enex
└── _Cross_References.enex
```

Each note within an ENEX file represents one cluster of related nodes.

## Export Script

Use the bundled export script:

```bash
python3 /home/ubuntu/skills/life-intelligence-engine/scripts/export_evernote.py \
  --assembled-dir /home/ubuntu/work/lie-output/assembled/ \
  --output-dir /home/ubuntu/work/lie-output/evernote-export/
```

The script:
1. Reads each domain's manifest and clusters
2. Converts node content to ENML (Evernote Markup Language)
3. Adds tags for domain, content type, entities, and importance level
4. Generates one ENEX file per domain
5. Creates a cross-references notebook linking related notes

## Import Instructions

To import into Evernote:
1. Open Evernote desktop app
2. File → Import → Evernote Export Files (.enex)
3. Select the domain ENEX files
4. Each file creates a new notebook
5. Tags are automatically applied

For Evernote Web: upload ENEX files via Settings → Import.
