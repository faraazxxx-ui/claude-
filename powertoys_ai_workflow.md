─────────────────────────────────────────
# PowerToys AI Workflow — Surface Laptop 7 ARM
## Version 0.98.0 | ARM64 Download: https://github.com/microsoft/PowerToys/releases/download/v0.98.0/PowerToysSetup-0.98.0-arm64.exe
─────────────────────────────────────────

### Priority First Action
Install PowerToys using the ARM64 direct download link above to establish the unified execution layer for all your AI agents.

### Module Setup Guide (GUI-only — no terminal required)

**Module 1: PowerToys Run** (Priority: Highest)
Purpose: Replaces Spotlight. Launch any AI agent by typing its name.
Shortcut: Alt+Space
Setup path: Click Settings → Select PowerToys Run → Scroll to Plugins → Expand "URI Handler" → Ensure it is turned On.
*Note: PowerToys Run does not have a native GUI for custom URI shortcuts. For one-keystroke access to your agents, use the Keyboard Manager module below.*

**Module 2: FancyZones**
Purpose: Persistent AI multi-window layout.
Setup path: Click Settings → Select FancyZones → Click "Launch layout editor"
Recommended: Create a custom 3-column layout — AI Chat (30%) | Work (50%) | Notes (20%)

**Module 3: Keyboard Manager**
Purpose: One-keystroke access per AI agent.
Setup path: Click Settings → Select Keyboard Manager → Click "Remap a shortcut"
Mapping: 
Click "+" to add a new mapping. Under "Physical Shortcut", press the keys. Under "Mapped To", select "Run Program" and enter the URL.
- Win+1 = https://claude.ai
- Win+2 = https://perplexity.ai
- Win+3 = https://grok.x.ai
- Win+4 = https://gemini.google.com
- Win+5 = https://manus.im
- Win+6 = https://comet.perplexity.ai
- Win+7 = [Path to Claude Chrome App]

**Module 4: Advanced Paste** (Win+Shift+V)
Purpose: Paste voice dictation to AI without formatting noise.
Setup path: Click Settings → Select Advanced Paste → Toggle "Enable Advanced Paste" to On.
*Note: The default shortcut is Win+Shift+V, not Win+Ctrl+V.*

**Module 5: Text Extractor** (Win+Shift+T)
Purpose: OCR any screen content → clipboard → paste to AI.
Setup path: Click Settings → Select Text Extractor → Toggle "Enable Text Extractor" to On.
Use case: Capture lab report, article, or document → send to AI for analysis.

### Voice → AI Pipeline
Step 1: Press Win+H → dictate your prompt or thought
Step 2: Press Win+Shift+V → select "Paste as Plain Text" to paste clean text (no formatting) into active AI window
Step 3: AI processes your spoken input

### API Key Storage (GUI, no terminal)
Path: Click Start Menu → Type "Control Panel" and press Enter → Click User Accounts → Click Credential Manager → Click Windows Credentials → Click "Add a generic credential"
One entry per API key (Claude, Grok, Perplexity, Gemini). Use the API endpoint as the network address, your email as the username, and the API key as the password.

### ARM64 Compatibility Status
| Module | ARM64 Status | Source |
| :--- | :--- | :--- |
| PowerToys Run | Fully Compatible | [1] |
| FancyZones | Fully Compatible | [1] |
| Keyboard Manager | Fully Compatible | [1] |
| Advanced Paste | Fully Compatible | [1] |
| Text Extractor | Fully Compatible | [1] |
| File Locksmith | May crash on launch (Exception 0xc0000409) | [2] |
| Image Resizer | May crash on launch (Exception 0xc0000409) | [2] |
| PowerRename | May crash on launch (Exception 0xc0000409) | [2] |
| Registry Preview | May crash on launch (Exception 0xc0000409) | [2] |

*Note: If PowerToys crashes on launch on your Snapdragon X Elite, a known workaround is to navigate to `C:\Program Files\PowerToys\WinUI3Apps` and rename the DLL files for the crashing modules (e.g., `PowerToys.FileLocksmithExt.dll` to `PowerToys.FileLocksmithExt.dll.bak`).*

─────────────────────────────────────────
### Research Sources
[1] Microsoft PowerToys Documentation: https://learn.microsoft.com/en-us/windows/powertoys/
[2] GitHub Issue #40205 - Snapdragon X Elite Crash: https://github.com/microsoft/PowerToys/issues/40205
[3] GitHub Releases - PowerToys v0.98.0: https://github.com/microsoft/PowerToys/releases/tag/v0.98.0
[4] Windows Credential Manager: https://support.microsoft.com/en-us/windows/credential-manager-in-windows-1b5c916a-6a16-889f-8581-fc16e8165ac0
─────────────────────────────────────────
