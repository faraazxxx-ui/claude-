---
title: Gaming + Triple-Monitor Setup Architecture
type: deliverable
domain: workspace-architecture
tags: [setup, hardware, gaming, triple-monitor, kvm, cross-os, macos, windows, second-brain]
devices: [macbook-pro-m4, surface-book, gaming-desktop]
status: decision-ready
created: 2026-06-25
---

# 🎛️ Gaming + Triple-Monitor Workspace Architecture

> [!abstract] TL;DR — The One-Sentence Verdict
> Buy a **Lenovo Legion desktop** (not the ThinkBook laptop) as a permanent third compute node, anchor it to a **matched triple-monitor set** as the durable backbone, bridge productivity-to-gaming with the **Razer Basilisk V3 Pro**, and stitch macOS ↔ Windows together with **software cursor-sharing (Flow / Deskflow) for work + a hardware KVM dock (AV-Access iDock B-series) for full-screen gaming**.

This note is structured as four self-contained modules — one per question — so each can be linked, transcluded, or extracted independently into your vault.

- [[#1 · Compute & Expansion Strategy — Laptop vs Desktop]]
- [[#2 · Setup Architecture & Deal Optimization]]
- [[#3 · Ergonomic Mouse Evolution]]
- [[#4 · Frictionless Cross-OS Synergy]]
- [[#🧱 Master Architecture — The Assembled System]]
- [[#✅ Action Checklist (Sequenced)]]

---

# 1 · Compute & Expansion Strategy — Laptop vs Desktop

## 1.1 The Core Diagnosis

Your Surface Book is "stuck" on the monitors because it is currently doing **two jobs at once**: it is your *Windows compute* **and** your *display anchor*. The moment you unplug it to be portable, your monitors go dark. That is the real problem to solve — not "which new laptop," but **decoupling the display anchor from a portable machine.**

> [!key] Reframe
> You do not need a *third portable computer*. You already have two laptops. You need a **stationary compute node** that permanently owns the monitors and adds gaming horsepower — which frees the Surface Book to become portable again.

## 1.2 The Verdict: Desktop, Decisively

| Factor | High-End ThinkBook (Laptop) | Legion Tower (Desktop) | Winner |
|---|---|---|---|
| **Purpose fit** | Business/productivity ultrabook — weak or no gaming GPU | Purpose-built gaming GPU + CPU | 🖥️ Desktop |
| **Real GPU power** | A laptop "RTX 5080" runs at ~80–175 W (throttled) | A desktop RTX 5080 runs at ~250–360 W — *much* faster at the same name | 🖥️ Desktop |
| **Sim-racing / flight at triple-screen** | Struggles — 3× the pixels at sustained load | Designed for exactly this sustained load | 🖥️ Desktop |
| **Thermals (sustained)** | Throttles after minutes; loud, hot | Large air/AIO cooling; sustained boost; quieter | 🖥️ Desktop |
| **Upgradeability** | Soldered GPU/RAM = dead-end | Swap GPU, RAM, SSD, PSU for ~6–8 yrs | 🖥️ Desktop |
| **Cost per frame** | Pays a "portability tax" you don't need | Far more performance per dollar | 🖥️ Desktop |
| **Solves the "stuck Surface Book"** | No — adds a 3rd laptop to juggle | **Yes** — becomes the permanent anchor | 🖥️ Desktop |
| **Portability** | Yes | No (irrelevant — you have 2 laptops) | 💻 Laptop |

**A ThinkBook only makes sense if** your genuine need is a third *travel* machine with better specs than the Surface Book. For **gaming + triple-monitor anchoring, it is the wrong tool** — it pays a thermal/price penalty for portability you already have covered twice over.

## 1.3 Why a Desktop Solves the "Third Screen" Problem

```
BEFORE  ─ Surface Book is the anchor (can't leave the desk)
  Surface Book ──┬── Monitor 1
                 ├── Monitor 2
                 └── (you, tethered)

AFTER  ─ Legion desktop is the anchor (Surface Book is free)
  Legion Desktop ──┬── Monitor 1
                   ├── Monitor 2          ← desktop drives all 3
                   └── Monitor 3            with one GPU, easily
  MacBook M4  ─────┤  (joins via dock/KVM when you want it)
  Surface Book ────┘  (now portable again — grab & go)
```

The desktop becomes the **always-on owner of the monitors**. The Mac and Surface Book *visit* the screens via dock/KVM (see [[#4 · Frictionless Cross-OS Synergy]]).

## 1.4 The Hidden Constraint: Your Mac Caps at 2 External Displays

> [!warning] Critical spec for a "triple-monitor workflow"
> A **MacBook Pro with the base M4 *or* M4 Pro chip supports only TWO external displays** (plus its built-in screen). Only the **M4 Max drives four external displays.**

What this means for your triple setup:

| Source machine | Native external-display reach | Triple-screen reality |
|---|---|---|
| **Legion Desktop** | Limited only by the GPU (3–4 outputs trivial) | ✅ Drives all 3 monitors natively |
| **MacBook Pro M4 / M4 Pro** | **2 external** + built-in | ⚠️ 2 external monitors + laptop screen = "triple," OR add a **DisplayLink** dock to push a 3rd |
| **MacBook Pro M4 Max** | 4 external | ✅ Drives all 3 natively |

This is the single biggest reason the desktop is the right anchor: **it has no display ceiling for your triple goal, while the Mac does.**

## 1.5 Recommended Spec Targets (Legion Desktop)

> [!tip] Sim-racing/flight at triple-screen is GPU-bound on pixel count
> Triple 1440p (≈11M px) is **~3× the load** of single 1440p; triple 4K is ~12M×3. Right-size the GPU to your monitor choice (see Module 2).

- **GPU:** RTX 5070 Ti / 5080 class for triple **1440p 144–165 Hz**; RTX 5090 class if you insist on triple **4K**.
- **CPU:** Modern 8-core+ (sims like F1 are also CPU/physics-sensitive).
- **RAM:** 32 GB (sims + your PKM stack + browser tabs).
- **Outputs:** Confirm **3× DisplayPort 1.4 (DSC)** or mixed **DP 1.4 + HDMI 2.1** on the GPU.
- **PSU headroom:** Leave room for a future GPU swap (the upgrade path you're buying into).

---

# 2 · Setup Architecture & Deal Optimization

## 2.1 Architecture-First Mindset (Spend Priority)

Don't optimize the *purchase* — optimize the **layer that outlives every purchase.** Rank your spend by lifespan:

```
LONGEST-LIVED (buy best, buy once) ───────────► SHORTEST-LIVED (ride the deals)

 Monitors  >  Dock/KVM  >  Desk/Mount/Cabling  >  GPU  >  Peripherals
 (7–10 yr)   (5–7 yr)      (5–10 yr)             (3–4 yr) (2–4 yr)
```

> [!key] Deal strategy in one line
> **Spend deal-money on the durable backbone (monitors + dock/KVM), buy the GPU at mid-high tier on sale, and don't sink budget into a dead-end laptop.**

- **Buy monitors as a matched set** — identical model = uniform color, bezel width, and stand height (essential for a clean triple array and a minimalist aesthetic).
- **Monitor arm / VESA mount** (single triple-arm or three single arms) clears the desk for the minimalist look and lets you angle the side monitors inward for sim-racing wrap.
- **Cable management + Philips Hue** is the *last* 10% — but it's what makes the build feel "cohesive." Hue gradient lightstrip behind the triple array + Hue Sync (Windows) for game-reactive bias lighting.

## 2.2 Triple vs Ultrawide — Decide This First

| | True Triple (3 panels) | Single 49" Super-Ultrawide |
|---|---|---|
| **Sim-racing immersion** | ✅ Best — angle side panels for peripheral vision | Good, but flat-ish wrap |
| **Bezels** | Thin gaps between panels | ✅ None |
| **Productivity tiling** | ✅ 3 clean workspaces | Needs window-management (FancyZones) |
| **macOS support** | ✅ Treated as 2–3 displays | ✅ One display |
| **GPU load** | Higher (3 panels) | Slightly lower |
| **Cost / desk space** | Higher / wider | Often cheaper / tidier |

> [!tip] Recommendation
> For **F1 25 + Ace Combat 7 immersion**, go **true triple** and angle the wings. If minimalism trumps cockpit wrap, a single 49" 5120×1440 ultrawide is the cleaner, simpler alternative.

## 2.3 Technical Standards Checklist

> [!warning] The macOS daisy-chain trap — read this first
> **Apple Silicon Macs (M-series) do NOT support DisplayPort MST daisy-chaining.** A daisy-chained 2nd monitor will only **mirror**, not extend. **Do not architect your Mac side around daisy-chaining.** Daisy-chaining works on **Windows only**.

| Standard | What to look for | Why it matters for you |
|---|---|---|
| **Thunderbolt 4 / USB4** | On the Mac side; **one cable = 2 displays + power (PD) + data** | Single-cable dock for the MacBook (cleanest, most minimalist) |
| **Thunderbolt 5** | Emerging; ~80–120 Gbps | Future-proofing if buying a new dock now |
| **DisplayPort 1.4 + DSC** | Per monitor; enables **4K@144Hz** or **1440p@165Hz+** | The backbone standard for the desktop's high-refresh outputs |
| **DisplayPort 2.1 / UHBR** | Newer GPUs/monitors | Higher headroom for 4K 240Hz, future triple-4K |
| **HDMI 2.1** | 48 Gbps; **4K@120/144Hz, VRR, ALLM** | Mixed-input KVMs + console-class refresh |
| **USB-C DP-Alt + PD ≥ 90W** | On at least one monitor | Lets the monitor power + drive the MacBook over one cable |
| **DP MST (daisy-chain)** | DP-out passthrough port | ✅ Windows desktop only — ❌ never rely on it for the Mac |
| **VRR (G-Sync / FreeSync)** | GPU + monitor + KVM must all pass it | Tear-free sim racing; confirm your KVM passes VRR |
| **EDID emulation** | On the dock/KVM | Stops windows from rearranging when you switch machines |

> [!key] The non-obvious buying rule
> Pick monitors that expose **both** a USB-C (DP-Alt + ≥90W PD) port **and** standard DP 1.4 / HDMI 2.1. Then the **MacBook uses USB-C (one cable)** and the **desktop uses DP/HDMI** — the same panels serve both worlds without compromise.

---

# 3 · Ergonomic Mouse Evolution

## 3.1 Why the MX Master Falls Short for Gaming

You love the MX Master's tall, palm-filling ergonomic hump and free-spin wheel — but it runs a **~1000 Hz polling, productivity-tuned sensor**, has a relatively **heavy/slow click latency**, and its weight + Bluetooth-first design make it imprecise for fast tracking and simulation inputs. You want a mouse that **keeps the ergonomic comfort but adds a true gaming sensor, low latency, and high polling.**

## 3.2 Comparative Table — The Three Bridges

| Spec | 🟢 Razer Basilisk V3 Pro | 🔵 Logitech G502 X PLUS | ⚪ Keychron M6 (8K) |
|---|---|---|---|
| **Shape / ergonomics** | Large, tall, palm-fill + thumb rest — **closest to MX Master feel** | Medium-large, classic G502 hump + thumb wing | Medium ergonomic, lighter/minimal |
| **Weight** | ~112–115 g | ~106 g | **~78 g** (lightest) |
| **Sensor** | Focus Pro 30K (30,000 DPI; 35K variant exists) | HERO 25K (25,600 DPI) | **PixArt 3950 (30,000 DPI)** |
| **Max polling** | 1,000 Hz (**4,000 Hz** w/ Dock Pro) | 1,000 Hz | **8,000 Hz** (highest) |
| **Scroll wheel** | **HyperScroll Tilt** — free-spin ↔ tactile + tilt (MX-like) | Dual-mode free/ratchet **toggle** + tilt | Magnetic metal wheel |
| **Connectivity** | 2.4 GHz / BT / wired | LIGHTSPEED 2.4 GHz / wired | 2.4 GHz / BT 5.x / wired (tri-mode) |
| **Programmable buttons** | 13 | 13 | ~6 |
| **OS / ecosystem** | Razer Synapse (Win-centric) | Logi G HUB; **also Logi Options+ → Flow** | **Mac-friendly**, cross-OS, on-board memory |
| **Best for** | Comfort-first bridge + RGB ecosystem | All-round veteran w/ great scroll | Lightweight tracking + Mac-native + 8K polling |

## 3.3 Recommendation Ranked to Your Profile

> [!tip] Pick by what you value most
> 1. **🥇 Razer Basilisk V3 Pro — your best "MX Master → gaming" bridge.** Big ergonomic palm-fill shape and a free-spin tilt wheel that mirror the MX Master you already love, but with a real 30K gaming sensor and (with the dock) 4,000 Hz. Most *comfort continuity*.
> 2. **🥈 Keychron M6 (8K) — if Mac-native + lightweight + max precision win.** 8,000 Hz polling and 78 g make it the most precise tracker here, and Keychron is built cross-OS so it behaves well on macOS. Less palm-fill than the MX Master.
> 3. **🥉 Logitech G502 X PLUS — the balanced veteran.** Excellent dual-mode scroll, stays inside the **Logitech ecosystem so it works with Logi Flow** (relevant to Module 4). Slightly less ergonomic hump than the Basilisk.

> [!note] Sim-specific reality check
> For **sim-racing (wheel) and flight (HOTAS/throttle)**, the mouse is mostly a *menu and aux* device — so **ergonomic comfort + reliable clicks** matter more than 8K polling. That tilts the pick toward the **Basilisk V3 Pro** for you. Reserve the 8K-polling argument for if you also play FPS/twitch titles.

---

# 4 · Frictionless Cross-OS Synergy

## 4.1 Two Different Problems — Don't Conflate Them

| Layer | What it moves | Tool type | Use when… |
|---|---|---|---|
| **Software KVM** | Keyboard + mouse + **clipboard** *(no video)* | Logitech Flow / Deskflow / Synergy | Both screens visible at once; gliding cursor between Mac & PC for **work** |
| **Hardware KVM/Dock** | **Displays** + USB peripherals + audio | AV-Access iDock / TESmart | You want **one machine on all 3 screens** (full-screen sim racing) |

> [!key] The winning pattern is HYBRID
> Use **software** to glide between machines during productivity, and a **hardware KVM** to hand the whole monitor array to one machine for gaming. They cover each other's blind spots.

## 4.2 Software Options Compared

| | Logitech Flow | Deskflow (open-source) | Synergy (paid) |
|---|---|---|---|
| **Cost** | Free (with Logi gear) | **Free / OSS** | Paid license |
| **Cross-OS (Mac↔Win)** | ✅ | ✅ | ✅ |
| **Clipboard sync** | ✅ text/img/files | ✅ (TLS-encrypted) | ✅ |
| **Hardware needed** | A Logitech Flow mouse | **Any mouse/keyboard** | Any |
| **Upstream relationship** | Logi-only | **Upstream of Synergy** | Polished Deskflow |
| **Best for** | You stay all-Logitech | Cross-brand, free, private | Want paid polish/support |

> [!tip] Software pick
> - If your mouse is the **Logitech G502 X PLUS** (or any Flow mouse) → use **Logitech Flow** (zero extra software, built into Logi Options+).
> - If you pick the **Basilisk** or **Keychron** → use **Deskflow** (free, open-source, TLS, clipboard sharing, works with any device).
> - ⚠️ **Never use software KVM as your *gaming* input** — the tiny network latency is fine for work, bad for sims. Game on the desktop's *directly attached* mouse.

## 4.3 Hardware KVM / Dock Options

| Device | Displays / Refresh | Inputs | Notably good for |
|---|---|---|---|
| **AV-Access iDock B10** | Dual — up to **4K@165Hz** / dual 8K@60 | USB-C (MST) laptop **+** HDMI/DP desktop | **Gaming PC + laptop** hybrid (matches your exact case) |
| **AV-Access iDock B23** | **Triple monitor** KVM | Desktop **+** laptop | True triple switching for desktop↔laptop |
| **AV-Access iDock M10** | Dual | **MacBook + PC** focused | Mac-first switching/docking |
| **TESmart HDK202-M24** | Dual **4K@144Hz**, HDMI 2.1 + DP 1.4, **VRR/HDR/ALLM** | 2 PCs / 2 monitors | Highest-refresh gaming KVM w/ VRR |
| **TESmart HDC202-P23** | Dual 4K@60 hybrid, **USB-C + MST** | 1 laptop + 1 desktop | USB-C-forward laptop docking |

> [!key] Hardware pick for your scenario
> Your case is literally **"one gaming desktop + one laptop sharing monitors"** — that is the **AV-Access iDock B-series** sweet spot (B10 for dual at gaming refresh; **B23 for true triple**). If VRR-passthrough for tear-free sims is your top priority on dual screens, the **TESmart HDK202-M24** leads on refresh + VRR.

## 4.4 Logical Diagram — Recommended Hybrid Architecture

```
                         ┌─────────────────────────────┐
                         │   TRIPLE MONITOR ARRAY      │
                         │  [Mon 1]  [Mon 2]  [Mon 3]  │
                         └────▲────────▲────────▲───────┘
                              │        │        │
                  ┌───────────┴────────┴────────┴───────────┐
                  │     HARDWARE KVM / DOCK (iDock B23)      │
                  │   - switches DISPLAYS + USB + audio      │
                  │   - EDID emulation, VRR passthrough      │
                  └───▲───────────────────────────────▲─────┘
        HDMI/DP ×3    │                                │   USB-C (1 cable:
        (gaming)      │                                │   video + data + PD)
                ┌─────┴──────┐                  ┌──────┴───────┐
                │  LEGION    │                  │  MacBook Pro │
                │  DESKTOP   │                  │   M4         │
                │ (Windows)  │                  │  (macOS)     │
                └─────┬──────┘                  └──────┬───────┘
                      │                                │
                      └──────────┬─────────────────────┘
                                 │  SOFTWARE LAYER
                       ┌─────────┴──────────┐
                       │ Deskflow / Logi    │  ← keyboard + mouse + clipboard
                       │ Flow (over LAN)    │     glide between Mac & PC for WORK
                       └────────────────────┘

   Surface Book ── now FREE / portable (joins KVM only if/when needed)

   Philips Hue ── gradient strip behind array + Hue Sync (Windows, game-reactive)
```

## 4.5 Two Operating Modes (How You'll Actually Use It)

```
MODE A — "Work / Second Brain"  (both machines live)
  • Mac on Mon 1+2 (its native 2-display max) ; Desktop on Mon 3
  • Deskflow/Flow → one keyboard+mouse glides across all screens
  • Clipboard syncs Mac ↔ Windows ; NotePlan/Obsidian/Notion flow freely

MODE B — "Sim Cockpit"  (gaming)
  • Press KVM hotkey → Desktop seizes ALL 3 monitors
  • Wheel/HOTAS + desktop's directly-attached mouse (no software KVM latency)
  • Hue Sync bias lighting reacts to F1 25 / Ace Combat 7
  • Mac idles ; Surface Book is elsewhere / portable
```

---

# 🧱 Master Architecture — The Assembled System

| Layer | Recommendation | Why |
|---|---|---|
| **Compute anchor** | **Lenovo Legion desktop** (RTX 5070 Ti/5080 class) | Power, thermals, upgradeability; frees the Surface Book |
| **Displays** | **Matched triple** 1440p **144–165 Hz** (DP 1.4 + DSC; one panel w/ USB-C PD) | Durable backbone; immersion; macOS-friendly |
| **Mac connection** | **Thunderbolt 4 / USB4 dock** (single cable) | Cleanest, most minimalist Mac integration |
| **Machine switching** | **AV-Access iDock B23** (triple) or **B10/TESmart M24** (dual + VRR) | Hand all screens to one machine on demand |
| **Software glide** | **Deskflow** (or **Logi Flow** if Logitech mouse) | Keyboard/mouse/clipboard across OSes for work |
| **Mouse** | **Razer Basilisk V3 Pro** (comfort bridge) | MX-Master-like ergonomics + real gaming sensor |
| **Ambiance** | **Philips Hue** gradient strip + **Hue Sync** | Cohesive minimalist + game-reactive lighting |
| **Surface Book** | Demoted to **portable** role | Problem solved — no longer "stuck" |

---

# ✅ Action Checklist (Sequenced)

> [!todo] Buy & build in this order — backbone first, peripherals last
> - [ ] **Confirm your MacBook's exact chip** (base M4 / M4 Pro = 2 external displays; M4 Max = 4). Decides whether you need a DisplayLink dock for a 3rd Mac display.
> - [ ] **Pick triple vs 49" ultrawide** (immersion vs minimalism) — §2.2.
> - [ ] **Buy the matched monitor set** on deal — require DP 1.4+DSC and ≥1 USB-C PD port (§2.3).
> - [ ] **Buy the Legion desktop** — verify 3× DP/HDMI 2.1 outputs and PSU upgrade headroom (§1.5).
> - [ ] **Buy the KVM/dock** — iDock B23 (triple) / B10 / TESmart M24; confirm **VRR + EDID** passthrough (§4.3).
> - [ ] **Add a Thunderbolt 4 dock** for the Mac's single-cable connection (§2.3).
> - [ ] **Install software glide** — Deskflow or Logi Flow; test clipboard Mac↔Win (§4.2).
> - [ ] **Buy the mouse** — Basilisk V3 Pro (or Keychron M6 8K / G502 X PLUS) (§3).
> - [ ] **Mount + cable-manage** the triple array on an arm; add **Philips Hue** strip + Hue Sync.
> - [ ] **Reclaim the Surface Book** as your portable machine. ✅

---

## 📚 Sources

- Apple — [How many displays can be connected to MacBook Pro](https://support.apple.com/en-us/101571) · 9to5Mac — [M4 MacBook Pro external display support](https://9to5mac.com/2024/10/30/m4-macbook-pro-external-display-support/) · Plugable — [External display support on M4 chips](https://kb.plugable.com/docking-stations-and-video/understanding-external-display-support-on-apple-m1-m2-m3-and-m4-chips)
- Razer — [Basilisk V3 Pro](https://www.razer.com/gaming-mice/razer-basilisk-v3-pro) · Tom's Hardware — [Basilisk V3 Pro review](https://www.tomshardware.com/reviews/razer-basilisk-v3-pro)
- Logitech G — [G502 X PLUS](https://www.logitechg.com/en-us/products/gaming-mice/g502-x-plus-wireless-lightforce.html) · Tom's Hardware — [G502 X Plus review](https://www.tomshardware.com/reviews/logitech-g502-x-plus)
- Keychron — [M6 Wireless Mouse](https://www.keychron.com/products/keychron-m6-wireless-mouse) · MechanicalKeyboards — [M6 8K Steel Scroll](https://mechanicalkeyboards.com/products/keychron-m6-wireless-8k-mouse)
- AV-Access — [iDock B10](https://www.avaccess.com/products/idock-b10/) · [iDock B23 (triple)](https://www.avaccess.com/products/idock-b23/) · [iDock M10 (Mac+PC)](https://www.avaccess.com/products/idock-m10/) · [KVM dock category](https://www.avaccess.com/product-category/kvm-switch-dock/)
- TESmart — [HDK202-M24 (Dual 4K144 VRR)](https://www.tesmart.com/products/hdk202-m24) · [Dual-monitor KVM collection](https://www.tesmart.com/collections/dual-monitor)
- Deskflow — [GitHub project](https://github.com/deskflow/deskflow) · Symless — [Synergy](https://symless.com/synergy) · Logitech — [Flow setup](https://www.logitech.com/en-us/discover/a/flow-setup)
