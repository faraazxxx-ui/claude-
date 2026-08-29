# Sony recorder batch pipeline

For long-form speech — a five-minute design ramble, a drive, a walk. Record on the Sony, plug it in, get transcripts.

## Read this first

Two files drive this pipeline: `sony_sync.sh` and `com.faraaz.sonysync.plist`. **Neither has ever been inspected.** They were produced in an earlier session and were not available for review, so nothing below vouches for what the script does once it runs.

What *is* corrected here are the install commands, which were plainly broken as written — they pointed at the filesystem root instead of his home folder, and one of them never wrote its output file at all. Those errors are the kind that fail loudly, which is lucky. The script's internal behaviour is the part still unaudited.

If he reports the pipeline misbehaving, ask him to paste the script rather than guessing at it.

## Corrected install

### 1. Install whisper.cpp

```bash
brew install whisper-cpp
```

### 2. Enable Metal GPU acceleration

Without this, transcription falls back to CPU and runs dramatically slower. Add it to his shell profile so it persists:

```bash
echo 'export GGML_METAL_PATH_RESOURCES="$(brew --prefix whisper-cpp)/share/whisper-cpp"' >> ~/.zshrc
source ~/.zshrc
```

### 3. Download the model — 1.62 GB, one time

```bash
mkdir -p ~/.whisper/models
curl -L -o ~/.whisper/models/ggml-large-v3-turbo.bin \
  "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin"
```

Size verified 2026-08-29: 1,624,555,275 bytes.

### 4. Place the two files — corrected paths

The original instructions were broken three ways: `~` was missing so paths resolved to the filesystem root (which would need admin rights and would be wrong anyway), and the `sed` line had no `>` redirect, so the plist was printed to the screen instead of written to disk.

```bash
mkdir -p ~/scripts ~/Voice-Inbox
mv ~/Downloads/sony_sync.sh ~/scripts/ && chmod +x ~/scripts/sony_sync.sh
sed "s|HOME|$HOME|g" ~/Downloads/com.faraaz.sonysync.plist \
  > ~/Library/LaunchAgents/com.faraaz.sonysync.plist
```

### 5. Load the watcher

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.faraaz.sonysync.plist
```

The older `launchctl load` still works on current macOS but is deprecated and prints a warning. If `bootstrap` errors with "service already loaded," it is already running — nothing to do.

To remove it later:

```bash
launchctl bootout gui/$(id -u)/com.faraaz.sonysync
```

### 6. Test once, with the recorder plugged in

```bash
bash ~/scripts/sony_sync.sh
```

If transcripts appear, every future plug-in is hands-off. The log lives at `~/Voice-Inbox/sync.log`; ask for its last 10 lines when something goes wrong.

## How it is meant to behave

Plug in the Sony → it mounts → the watcher fires → new audio is mirrored from each recorder folder into `~/Voice-Inbox/<folder>/audio/` → whisper.cpp transcribes locally → `.txt` / `.srt` / `.vtt` land in `~/Voice-Inbox/<folder>/transcripts/` → a macOS notification reports how many are new.

Folder names on the recorder become the routing key automatically, so nothing needs renaming.

## Privacy hard stop

Never route a folder that may contain patient identifiers to any cloud transcription service. Local whisper.cpp only.

This is the constraint that makes the pipeline usable for clinical material at all — the moment one folder goes to a cloud API, the whole inbox has to be treated as having left the building. If he asks about cloud transcription for speed, the answer is that the speed gain does not survive that trade, and there is no partial version of it that is safe by folder.
