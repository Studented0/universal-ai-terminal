# Portable AI Terminal — Complete Project Briefing
> **Last updated:** June 25, 2026  
> **Author:** Yahya (Spring, TX)  
> **For:** Hack Club Outpost X Tier — Open Sauce, San Francisco, July 18-20, 2026

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Timeline and Deadlines](#2-timeline-and-deadlines)
3. [Hack Club Outpost Context](#3-hack-club-outpost-context)
4. [Funding Justification](#4-funding-justification)
5. [Complete Component List](#5-complete-component-list)
6. [Display — DXQ7D0023 Technical Details](#6-display--dxq7d0023-technical-details)
7. [Schematic Architecture](#7-schematic-architecture)
8. [Power System Design](#8-power-system-design)
9. [Outstanding Blockers](#9-outstanding-blockers)
10. [Decisions Already Locked In](#10-decisions-already-locked-in)
11. [Software Stack](#11-software-stack)
12. [Linux Display Driver Plan](#12-linux-display-driver-plan)
13. [Assembly Plan](#13-assembly-plan)
14. [Open Sauce Demo Plan](#14-open-sauce-demo-plan)
15. [Key Reference Links](#15-key-reference-links)
16. [Immediate Next Actions](#16-immediate-next-actions)

---

## 1. Project Overview

### What it is
A custom portable universal AI terminal. A single purpose-built device — not a phone, not a laptop — that gives you access to Claude Code, Codex, Gemini, and Ollama from anywhere via 4G LTE cellular. No laptop needed, no phone needed. Just a device you built yourself that does one thing extremely well: connect you to AI.

### The core problem it solves
People running Claude Code on their laptop have to carry their laptop open or stay near it. There are viral videos of developers sleeping with their laptop next to them waiting on Claude Code to finish, or walking around a grocery store with their laptop open. This device solves that. Pocket it, walk away, come back to results.

### Why gaming is part of it
AI prompts — especially multi-agent Claude Code sessions — can take 5-20 minutes to complete. Instead of watching a loading bar, the device runs game emulators in a split view or full screen. N64, PSP, PS1 all run natively on the hardware. Play while you wait, get notified when the prompt finishes.

### Form factor
Phone/Nintendo Switch sized. 7" OLED touchscreen. Approximately 93mm wide × 165mm tall × 22-24mm thick. Pocketable in normal pants/jacket pockets. Lighter than a Switch with JoyCons.

### The hardware
- Custom 4-layer carrier PCB designed entirely from scratch
- Raspberry Pi CM5 compute module (same chip as Raspberry Pi 5)
- 4G LTE cellular modem (Quectel EC25-AF North America variant)
- 7" AMOLED 1080×1920 FHD touchscreen (60/90/120/144/165Hz, $59 confirmed)
- 10,000mAh battery (~8-9 hours of real use)
- Microphone for voice dictation
- Speaker for audio/game output
- WiFi + Bluetooth (from CM5 module)
- 64GB eMMC internal storage

### The software
- Raspberry Pi OS running full Linux
- Session manager app — custom-built UI that lets you switch between Claude Code, Codex, Gemini, and Ollama sessions with a tap
- mosh + tmux for resilient SSH connections that survive cellular handoffs
- Ollama for local LLM use when signal is weak
- RetroArch for game emulation

---

## 2. Timeline and Deadlines

| Date | Event |
|------|-------|
| **June 23** | Display + touch drivers fully resolved. Power sheet schematic started. |
| **June 25** | Today. Power sheet ~90% complete. FPC connector path resolved. PCB order deadline extended to June 27 (Friday) with expedited build to maintain July arrival. |
| **June 27** | Revised PCB order deadline — expedited 4-layer build at JLCPCB |
| **July 1-3** | Boards ship from JLCPCB with expedited service |
| **July 3-5** | Boards arrive |
| **June 26** | Hard PCB order deadline — must place JLCPCB order by this date |
| **June 26-28** | PCB in fabrication at JLCPCB |
| **July 1-3** | Order all non-JLCPCB parts (CM5, EC25, display, battery, etc.) |
| **July 7-10** | PCBs arrive via DHL to Spring, TX |
| **July 10-12** | Assembly (hot plate session + plug-ins) |
| **July 12-14** | Firmware bring-up, software configuration, initial testing |
| **July 14** | Leave for San Francisco |
| **July 14-17** | Outpost 4-day on-site hackathon (build keyboard attachment on-site) |
| **July 18-20** | Open Sauce expo — demo device to 35,000 attendees |

**Zero margin for error.** If PCB order slips past June 26, boards arrive after July 14 and the project misses the demo entirely. Schematic must start tonight.

---

## 3. Hack Club Outpost Context

### What Outpost is
A 6-day hardware hackathon + expo co-hosted with Open Sauce in San Francisco. July 14-20, 2026. Part hackathon (July 14-17 building), part expo (July 18-20 at Open Sauce with 35,000 people). Organized by Hack Club.

### Tiers
- **B tier**: $25 funding, 30% Stardust off ticket
- **A tier**: $120 funding, 50% Stardust off ticket
- **S tier**: $180 funding, 100% Stardust off (free ticket)
- **X tier**: $350+ funding (case-by-case), free ticket + extra travel stipend

### Why X tier is needed
Flight from Houston to San Francisco costs $300-400. Without X tier the base travel stipend is only $75, which doesn't cover the flight. X tier specifically includes an extra travel stipend that can cover the full flight cost.

### Approval status
- Pitch sent to **@alexren** in #outpost-idea-pool (primary X tier approver)
- Pitch sent to **Clay** (Outpost organizer, can approve funding and has authority up to ~$1,000)
- Both pitches describe: portable universal AI terminal, custom PCB, LTE cellular, 7" OLED, Claude/Codex/Gemini/Ollama, gaming while waiting on prompts
- Awaiting responses from both

### The funding concern
X tier budget is up to ~$1,000 but Hack Club reviewers may flag costs as "excessive." Total project BOM is approximately $580. This is **not** excessive for a custom handheld Linux computer with cellular — a GPD Pocket 3 (commercial equivalent) costs $700+ and can't be modified. The justification is in Section 4 below.

---

## 4. Funding Justification

### Why the budget is what it is
Every dollar in this BOM reflects actual hardware engineering, not off-the-shelf assembly:

| Cost driver | Amount | Why necessary |
|-------------|--------|---------------|
| CM5108064 compute module | $185 | The brain. Same chip as RPi 5. 8GB RAM needed to run local Ollama 7B alongside SSH sessions without paging. No cheaper option with same capability. |
| EC25AFXGA-MINIPCIE cellular modem | $75 | North America LTE Cat-4 certification on AT&T + T-Mobile. Without this the device is just a Pi in a box — LTE is what makes it a "terminal anywhere." No US-certified cheaper option exists. |
| DXQ7D0023 7" OLED display | $59 | The 7" size is what makes this demoable to 35,000 people at Open Sauce. A 4" screen loses the crowd. OLED specifically needed for terminal use — pure black background means black pixels are off, massively saving battery. (Sample pricing confirmed via email from Emily at DXQ.) |
| Custom 4-layer PCB + JLCPCB assembly | $125 | The actual engineering work. A 4-layer carrier PCB with impedance-controlled MIPI DSI traces, USB 2.0 differential pairs, power sequencing for an OLED display — this is not a breakout board, this is a hardware product. |
| All other components combined | $100 | Battery, LDOs, boost converter, USB-C PD IC, SIM slot, FPC connector, buttons, mic module, speaker, passives, enclosure resin |

**Total: ~$538**

### What makes this X tier, not S tier
- **Custom 4-layer PCB design** — not a kit, not a Pi in an enclosure. Every trace is designed.
- **MIPI DSI display integration** — routing 4 differential MIPI lanes with impedance control is advanced PCB work.
- **LTE cellular integration** — USB 2.0 differential pair routing to modem, SIM card circuit, antenna layout.
- **Multi-IC power system** — BQ25895 battery management + FUSB302 USB-PD + TPS61235P boost converter + two LDOs, all with proper sequencing.
- **Custom Linux DRM driver** — ICNA3512 has no mainline kernel driver. Writing a Device Tree overlay or custom DRM panel driver is genuine embedded Linux work.
- **Novel concept** — nothing like this exists commercially or as an open-source project. The closest thing (piBrick Pocket-CM5) doesn't have cellular, doesn't have the AI session manager, and doesn't have gaming integration.

### The $1,000 ceiling — why we're well under it
At $538, the BOM is 53.8% of the theoretical ceiling. There is no padding, no overpricing, no vanity components. Every item is load-bearing.

---

## 5. Complete Component List

### 5.1 JLCPCB Assembly Cart (confirmed in stock)

These components are already confirmed available in the JLCPCB assembly parts library. All are Extended parts (small setup fee) unless noted.

| Part | LCSC# | Package | Qty | Unit Cost | Purpose |
|------|-------|---------|-----|-----------|---------|
| DF40C-100DS-0.4V(51) | C597931 | Hirose DF40 100-pin | 2 | $1.06 | CM5 board-to-board connectors |
| BQ25895RTWR | C80200 | QFN-24-EP | 1 | $2.15 | Battery management + power path |
| TPS61235PRWLR | C544673 | VQFN-9 | 1 | $0.88 | 5V boost converter for CM5 |
| FUSB302BMPX | C132291 | WFQFN-14 | 1 | $0.41 | USB-PD negotiation IC |
| SGM2036-1.8YN5G/TR | C700371 | SOT-23-5 | 1 | $0.13 | 1.8V LDO (display VDDIO) |
| SGM2036-3.3YN5G/TR | **TBD** | SOT-23-5 | 1 | ~$0.13 | 3.3V LDO (display VCI) — **NOT YET FOUND** |
| TYPE-C 16PIN 3MD(385) | C2858270 | SMD | 1 | $0.08 | USB-C receptacle (charging) |
| PCIE-52P40H | C266898 | SMD right-angle | 1 | $0.49 | Mini PCIe slot (EC25 cellular) |
| NANO SIM 7P H1.37 | C7529384 | SMD push-push | 1 | $0.16 | Nano SIM card slot |
| HanElec IPEX U.FL | C47986640 | SMD | 2 | $0.04 | Antenna U.FL connectors |
| K2-6639SP-C4SC-04 | C83206 | SMD vertical | 3 | $0.03 | Power button + vol+/vol- |
| B2B-PH-SM4-TBT(LF)(SN) | C265003 | SMD JST-PH | 1 | $0.31 | 2-pin battery connector |
| MAX98357A | **TBD** | SMD | 1 | ~$1.50 | I2S audio amplifier (speaker) |
| 0603 LED red | **TBD** | 0603 SMD | 1 | ~$0.05 | Status LED |
| 39-pin 0.3mm FPC ZIF | **TBD** | SMD ZIF | 1 | ~$1.00 | **BLOCKING — display ribbon connector** |

> ⚠️ **IMPORTANT:** C154990 (SGM2036-2.8V) was accidentally added to the JLCPCB cart. **Remove it.** VCI rail is 3.3V, not 2.8V. The 2.8V LDO is wrong for this design.

### 5.2 Mouser Order (ship to yourself, forward module to JLCPCB for assembly or install yourself)

| Part | Mouser# | Qty | Unit Cost | Notes |
|------|---------|-----|-----------|-------|
| Quectel EC25AFXGA-MINIPCIE | 277-EC25AFXGA-MINIPCIE | 1 | $75 | North America LTE, AT&T + T-Mobile certified, mini PCIe, plugs into carrier PCB |
| JAE SM3ZS067U410AMR1000 | 656-SM3ZS067U410AM10 | 1 | $1.57 | M.2 M-key connector (optional NVMe expansion) |

### 5.3 Amazon Orders

| Item | Approx Cost | Notes |
|------|-------------|-------|
| CM5108064 — Raspberry Pi CM5 8GB/64GB/WiFi (used, Very Good) | $185 | Main compute. Confirmed available overnight. Buy first — longest lead time. |
| AITRIP INMP441 I2S Microphone Modules ×5 | $11.99 | Plugs into 6-pin female header on PCB. No soldering. |
| 10000mAh Li-Po battery (model 1160100, 100×60×11mm, PH2.0) | $16.99 | Confirmed fitting in device body. 8-9 hour battery life. |
| Small 8Ω 1W speaker (round, ~20mm diameter) | ~$5 | For game audio + voice output |
| Through-hole red LED 3mm or 5mm | ~$2 | Status indicator, hand-solder |
| Flexible LTE antenna U.FL IPEX ~15cm | ~$5 | For EC25 cellular modem main antenna |
| Flexible WiFi/BT antenna U.FL 2.4/5GHz | ~$4 | For CM5 WiFi |
| Solder paste syringe (63/37 or SAC305) | ~$8 | For hot plate assembly of M.2 connector |
| Hot plate / mini reflow plate (~$25 if you don't have one) | ~$25 | For hot plate assembly |

### 5.4 DXQ Display Order

| Part | Contact | Cost | Status |
|------|---------|------|--------|
| DXQ7D0023 7" OLED with touch | dxqlcd@dxq-lcd.com (Emily) | **$59** | Sample unit price confirmed via email June 23, 2026. Ready to order once grant approved. |

### 5.5 Enclosure

- **Material**: SLA resin (friend prints for cost of resin only, ~$10-15)
- **Dimensions to design around**: ~95mm × 168mm × 24mm
- **File format**: STL for printing
- **Design tool**: FreeCAD or Fusion 360
- **Note**: Design enclosure AFTER PCB layout is complete (enclosure wraps the PCB, not the other way around)

---

## 6. Display — DXQ7D0023 Technical Details

### General Specifications

| Parameter | Value |
|-----------|-------|
| Model | DXQ7D0023 |
| Type | AMOLED (Active Matrix OLED) |
| Size | 7.0 inch diagonal |
| Resolution | 1080 × 1920 (FHD) |
| PPI | 315 |
| Panel technology | LTPS (Low Temperature Poly-Silicon) |
| Driver IC | **ICNA3512** (not SH8804B — Gemini hallucinated that) |
| Interface | MIPI DSI, 4-lane |
| Refresh rates | 60 / 90 / 120 / 144 / 165 Hz | All confirmed — complete init sequences in hand |
| Connector | FH26-39S-0.3SHW (Hirose, 39 pins, 0.3mm pitch) |
| Module dimensions (W×H×T) | 89.13 × 160.91 × 1.095 mm |
| Active area (W×H) | 87.13 × 154.91 mm |
| Normal brightness | 800 nits (typical) |
| HBM brightness | 1000 nits (typical) |
| Contrast ratio | 100,000:1 |
| Color gamut | 100% NTSC |
| Colors | 1.07 billion (10-bit DSC) |
| Touch | On-cell capacitive, 5-point |
| Touch sensor | 20 Tx × 36 Rx channels, diamond pattern |
| Operating temperature | -20°C to 70°C |

### Power Rails

| Pin name | Voltage | Source on carrier PCB | Notes |
|----------|---------|----------------------|-------|
| VBAT (pins 4-8) | 3.8 – 4.5V | BQ25895 SYS output directly | Li-Po 3.8-4.35V range fits perfectly. Set VSYSMIN=3.8V in BQ25895 register. No regulator needed. |
| VCI (pin 30) | 3.3V | SGM2036-3.3V LDO | Powers driver IC analog supply |
| VDDIO (pin 29) | 1.8V | SGM2036-1.8V LDO (C700371) | Powers driver IC digital I/O |
| TP-VDD (pin 33) | 3.3V | Share VCI rail | Touch IC power |
| TP-1V8 (pin 34) | 1.8V–3.3V | Share VDDIO rail at 1.8V | Touch IC I/O — spec says 1V8–3V3 range; using 1.8V is correct |
| RESX (pin 28) | 1.8V logic | CM5 GPIO (pulled high via 10kΩ to 1.8V) | Active LOW reset. ICNA3512 datasheet: hold low ≥10μs after both VCI and VDDIO stable, then release. |

> **Confirmed from ICNA3512 datasheet:** nRESET must be held LOW for minimum 10μs after both VCI (3.3V) and VDDIO (1.8V) have reached their target voltages before being released HIGH. Violation of this sequence means the IC may not initialize correctly.

### Module Dimensions — Thickness Clarification

The DXQ spec contains two thickness numbers which initially appear to conflict:
- **89.13 × 160.91 × 1.095mm "With R.T"** — This is the assembled module as-shipped, including the AMOLED glass, bonded FPC ribbon cable, and reinforcement tape (R.T). **Use 1.095mm for enclosure design.**
- **89.1344 × 160.9056 × 0.8mm** — This is the bare AMOLED glass panel only, from the Visionox panel spec embedded in the DXQ document. The remaining 0.295mm comes from the FPC and tape assembly.

**Design to 1.095mm.** That's what arrives in the box.

### Complete 39-Pin Connector Pinout

| Pin | Name | Function | Notes |
|-----|------|----------|-------|
| 1 | GND | Ground | |
| 2 | GND | Ground | |
| 3 | GND | Ground | |
| 4 | VBAT | 3.8-4.5V power in | |
| 5 | VBAT | 3.8-4.5V power in | |
| 6 | VBAT | 3.8-4.5V power in | |
| 7 | VBAT | 3.8-4.5V power in | |
| 8 | VBAT | 3.8-4.5V power in | |
| 9 | GND | Ground | |
| 10 | OTPV | OTP programming voltage | Leave open / NC in normal use |
| 11 | NC | No connection | Leave open |
| 12 | GND | Ground | |
| 13 | D3P | MIPI DSI data lane 3 + | Differential pair — route as 90Ω impedance-controlled |
| 14 | D3N | MIPI DSI data lane 3 – | Differential pair |
| 15 | GND | Ground | |
| 16 | D0P | MIPI DSI data lane 0 + | Differential pair |
| 17 | D0N | MIPI DSI data lane 0 – | Differential pair |
| 18 | GND | Ground | |
| 19 | CLKP | MIPI DSI clock lane + | Differential pair |
| 20 | CLKN | MIPI DSI clock lane – | Differential pair |
| 21 | GND | Ground | |
| 22 | D1P | MIPI DSI data lane 1 + | Differential pair |
| 23 | D1N | MIPI DSI data lane 1 – | Differential pair |
| 24 | GND | Ground | |
| 25 | D2P | MIPI DSI data lane 2 + | Differential pair |
| 26 | D2N | MIPI DSI data lane 2 – | Differential pair |
| 27 | GND | Ground | |
| 28 | RESX | Reset (active low, 1.8V) | Pull high to 1.8V via 10kΩ. Drive low via CM5 GPIO to reset. |
| 29 | VDDIO | 1.8V digital I/O supply | |
| 30 | VCI | 3.3V analog supply | |
| 31 | TE | Tear effect output | Connect to CM5 GPIO for frame sync (optional but recommended) |
| 32 | GND | Ground | |
| 33 | TP-VDD | Touch IC 3.3V power | |
| 34 | TP-1V8 | Touch IC 1.8V I/O power | |
| 35 | TP-SDA | I2C data (1.8V–3.3V) | Pull up to 1.8V via 4.7kΩ |
| 36 | TP-SCL | I2C clock (1.8V–3.3V) | Pull up to 1.8V via 4.7kΩ |
| 37 | TP-RESET | Touch reset (active low) | Pull high to 1.8V via 10kΩ, drive via CM5 GPIO |
| 38 | TP-INT | Touch interrupt output | Pull up to 1.8V via 10kΩ, read via CM5 GPIO |
| 39 | GND | Ground | |

### Display Timing Parameters

From DXQ7D0023 spec (page 4). All values confirmed from vendor datasheet.

**Constraints (hardware-enforced by ICNA3512):**
- HS + HBP must be a multiple of 4
- VS + VBP must be a multiple of 4

**60Hz mode:**
| Parameter | Value |
|-----------|-------|
| HS (HSync width) | 1 |
| HBP | 23 |
| HAdr (horizontal active) | 1080 |
| HFP | 156 |
| HTOTAL | 1 + 23 + 1080 + 156 = **1260** |
| VS (VSync width) | 1 |
| VBP | 15 |
| VAdr (vertical active) | 1920 |
| VFP | 20 |
| VTOTAL | 1 + 15 + 1920 + 20 = **1956** |
| **Pixel clock** | 60 × 1260 × 1956 = **147,657,600 Hz (~147.66 MHz)** |

```dts
clock-frequency = <147657600>;
```

Check: HS+HBP = 1+23 = 24 ✓ (multiple of 4). VS+VBP = 1+15 = 16 ✓ (multiple of 4).

**120Hz mode (DSC compressed):**

From the init code screenshot in the DXQ spec, format is `VA HA HZ VBP VFP HBP HFP VS HS`:
```
mipi.video 1920 1080 120 15 412 23 156 1 1
```

| Parameter | 60Hz | 120Hz DSC |
|-----------|------|-----------|
| VFP | 20 | **412** |
| VTOTAL | 1956 | 1 + 15 + 1920 + 412 = 2348 |

The VFP of 412 at 120Hz is not a mistake — DSC (Display Stream Compression) needs a large vertical front porch to give the panel's decode pipeline time to process compressed frames. This is normal for DSC-enabled panels.

**90Hz and 165Hz modes:** Supported by the panel spec but timing parameters not yet obtained. If needed, ask Emily for the corresponding init code files.

**MIPI DSI lane rate (60Hz):**
- Pixel clock × 24 bpp / 4 lanes ≈ 147.66 MHz × 24 / 4 = **885 Mbps per lane**
- CM5 DSI PHY limit: ~2.5 Gbps per lane — 60Hz is well within spec
- 120Hz DSC: compressed ~3:1, effective ~885 Mbps per lane — also within spec

### Production Driver Package — DXQ Debug Files (Received June 23, 2026)

DXQ sent a complete production-grade driver package. All display and touch driver questions are now fully resolved. Files received:

| File | Contents |
|------|----------|
| `dsi-panel-7inch-vrr-cmd.TXT` | Complete Qualcomm MDSS panel driver — init sequences for ALL 5 refresh rate modes in one file, including timing-switch commands for live mode changes |
| `Display_init_code_60Hz_NO_DSC.txt` | Simpler legacy 60Hz init. Superseded by VRR file but useful for reference. |
| `PPS_code_VESA1_2_10_10_slice1_20_1080x1920_block_pred_disable.txt` | DSC Picture Parameter Set in human-readable form — the 88 bytes needed by the CM5 DSC engine. Also embedded in C7/C8/C9 commands in VRR file. |
| `DSC_set_VESA1_2_10_10_slice1_20_1080x1920_block_pred_disable.txt` | Human-readable DSC configuration: VESA 1.2, 10-bit source, 10-bit output, 1080×20 slice, no block prediction. Maps directly to CM5 DRM DSC config struct. |
| `Porch.png` | Timing diagram for SSD2828 RGB-to-DSI bridge — **not relevant** to CM5 direct DSI. Ignore. |
| `focaltech_config.h` | Confirms touch IC: `FTS_CHIP_TYPE = _FT3519T` (line 223) |
| `focaltech-ts.txt` | Device tree example for FT3519T — I2C address 0x38, compatible = "focaltech,fts" |
| All other focaltech_*.c/.h files | **Complete GPL v2 Linux kernel driver source for FT3519T.** Ready to compile. No touch driver work needed. |

### ICNA3512 Key Register Reference

| Command | Hex | Name | What it does |
|---------|-----|------|--------------|
| CMDLOCKUCS | 9Ch | UCS Lock | Unlock (A5 A5) or lock (5A 5A) user command set |
| CMDLOCKMCS | FDh | MCS Lock | Unlock (5A 5A) or lock (A5 A5) manufacturer command set |
| WRDSIM | 48h | DSI Mode | Set DSI mode and refresh rate tier (see WRDSIM table below) |
| WRCTRL | 53h | Control Display | Enable brightness control, set HBM mode |
| WRDISBV | 51h | Display Brightness | 13-bit brightness value |
| TEON | 35h | Tear Effect On | Enable TE signal for frame sync |
| SLPOUT | 11h | Sleep Out | Wake panel — mandatory 120ms wait before DISPON |
| DISPON | 29h | Display On | Begin showing image |
| DISPOFF | 28h | Display Off | Used before entering sleep |
| SLPIN | 10h | Sleep In | Low power sleep |
| MADCTL | 36h | Memory Access Control | Flip/mirror display if mounted inverted |
| REG SEL | 9Fh | MCS Group Select | Select manufacturer register group before writing |

### WRDSIM (48h) Refresh Rate Register

| Mode | Byte | Binary | HFR_MODE | DSI_MODE | Notes |
|------|------|--------|----------|----------|-------|
| 60Hz | `48 00` | 0b00000000 | 00 | 00 (cmd) | Command mode |
| 90Hz | `48 00` | 0b00000000 | 00 | 00 (cmd) | Same WRDSIM, different timing registers |
| 120Hz | `48 30` | 0b00110000 | 11 (HF3) | 00 (cmd) | HF3 mode |
| 144Hz | `48 30` | 0b00110000 | 11 (HF3) | 00 (cmd) | Same HFR as 120Hz, tighter timing config |
| 165Hz | `48 20` | 0b00100000 | 10 (HF2) | 00 (cmd) | HF2 mode, different HFP |

> The VRR file uses DSI command mode (DSI_MODE=00). For the CM5, video mode (DSI_MODE=11, byte ORed with 0x03) is simpler to implement. Either works — command mode is more power efficient, video mode is easier to bring up first.

### All Five Refresh Rate Timings

| Mode | HFP | HBP | HS | VFP | VBP | VS | WRDSIM |
|------|-----|-----|----|-----|-----|----|--------|
| 60Hz | 156 | 23 | 1 | 2760 | 15 | 1 | `48 00` |
| 90Hz | 156 | 23 | 1 | 1192 | 15 | 1 | `48 00` |
| 120Hz | 156 | 23 | 1 | 412 | 15 | 1 | `48 30` |
| 144Hz | 156 | 23 | 1 | 20 | 15 | 1 | `48 30` |
| 165Hz | 98 | 23 | 1 | 20 | 15 | 1 | `48 20` |

> **Note on large VFPs:** In command mode, the vertical front porch is the window the host uses to push frame data into the display's internal GRAM. 60Hz has 2760 blank lines — a large buffer. This shrinks at higher rates as timing gets tighter. 144Hz and 165Hz use the minimum VFP (20 lines) meaning the host must be fast. For initial bring-up, start at 60Hz.

> **165Hz timing note:** HFP changes from 156 to 98 — the horizontal blanking is tighter. All other modes share the same horizontal structure. 165Hz has the simplest init sequence of all five modes despite being the highest rate.

### Production Init Sequence Structure (All Modes)

Every mode follows this structure (extracted from `dsi-panel-7inch-vrr-cmd.TXT`):

```
1. Unlock registers
   9C A5 A5   → Unlock user command set
   FD 5A 5A   → Unlock manufacturer command set

2. Set brightness to zero
   51 00 00   → Prevents flash during init

3. Sleep Out + mandatory 120ms wait
   11         → (delay 0x78 = 120ms)

4. Configure analog gain (same across all modes)
   9F 01
   C6 11 88

5. Send DSC Picture Parameter Set (same across all modes)
   C7 [33 bytes of PPS data — rows 1-2 of PPS]
   C8 [33 bytes of PPS data — rows 3-4 of PPS]
   C9 [31 bytes of PPS data — row 5 of PPS]

6. Configure display timing for THIS specific refresh rate
   9F 07 (or 07)
   B3 / B5 [mode-specific timing config]
   D3 / D9 [mode-specific pixel clock divider]
   CB / CE [mode-specific divider config]
   48 [WRDSIM — sets HFR mode]

7. Configure display geometry (same across all modes)
   9F 0E
   B2 70 76 04
   B3 41 A4 0A 17 14
   B4 31
   B5 61
   B6 01
   B7 [16 bytes]
   D6 14 24 08

8. OSC configuration group 5 (same across all modes)
   9F 05
   B3 82 00 00 99 99 09 99 00 3E FE

9. OSC configuration group F (same across all modes)
   9F 0F
   CE 52   ← NOTE: This is CE 52, NOT CE 22
              (CE 22 was from an incomplete/earlier FAE screenshot — CE 52 is the production value)

10. Brightness control and display on
    53 E0   → WRCTRL: brightness ctrl on, HBM off
    35      → TEON: tearing effect on
    29      → DISPON: display on (20ms delay)
```

### DTS Init Sequence (60Hz Command Mode — Ready to Use)

Translated from Qualcomm MDSS format to Linux DRM panel format. Format per byte: `type delay len [data...]`

```dts
panel-init-sequence = [
    /* Unlock user + manufacturer command sets */
    39 00 03 9C A5 A5
    39 00 03 FD 5A 5A
    /* Set brightness to 0 */
    39 00 03 51 00 00
    /* Sleep Out — 120ms mandatory delay */
    05 78 01 11
    /* Analog gain config */
    39 00 02 9F 01
    39 00 03 C6 11 88
    /* DSC PPS — Picture Parameter Set (88 bytes across C7/C8/C9) */
    39 00 21 C7 12 00 00 AB 10 A0 07 80 04 38 00 14 04 38 05 46 01 9A 02 D4 00 19 02 40 00 15 00 0D 05 7A 03 1D
    39 00 21 C8 16 00 10 EC 07 10 20 00 06 0F 0F 33 0E 1C 2A 38 46 54 62 69 70 77 79 7B 7D 7E 01 C2 22 00 2A 40
    39 00 1F C9 32 BE 3A FC 3A FA 3A F8 3B 38 3B 78 3B 76 4B B6 4B B6 4B F4 5B F4 7C 34 00 00 00 00 00 00
    /* 60Hz timing config — Group 1 */
    39 00 02 9F 01
    39 00 07 B3 00 E0 A0 10 C8 00
    /* 60Hz timing config — Group 7 */
    39 00 02 9F 07
    39 00 08 B2 04 18 08 0C 02 00 C4
    39 00 10 D3 88 4A 4A 88 4A 4A 00 EB 00 00 00 00 00 00 00
    39 00 08 CB 01 01 01 01 04 09 2C
    /* WRDSIM: 60Hz command mode */
    39 00 02 48 00
    /* Display geometry — Group E */
    39 00 02 9F 0E
    39 00 04 B2 70 76 04
    39 00 06 B3 41 A4 0A 17 14
    39 00 02 B4 31
    39 00 02 B5 61
    39 00 02 B6 01
    39 00 11 B7 61 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
    39 00 04 D6 14 24 08
    /* OSC config — Group 5 */
    39 00 02 9F 05
    39 00 0B B3 82 00 00 99 99 09 99 00 3E FE
    /* OSC config — Group F */
    39 00 02 9F 0F
    39 00 02 CE 52
    /* Brightness control on */
    39 00 02 53 E0
    /* Tearing effect on */
    05 00 01 35
    /* Display On — 20ms delay */
    05 14 01 29
];

panel-exit-sequence = [
    /* Display off */
    05 00 01 28
    /* Sleep In — 120ms delay */
    05 78 01 10
];
```

**For 165Hz:** Change the timing config group 1/7 commands and `48 00` → `48 20`, and change HFP from 156 to 98 in the DTS timing node. Everything else stays identical.

**For 120Hz/144Hz:** Change `48 00` → `48 30` and swap the B3/B5/D9/CE timing group bytes per the VRR file. Requires DSC host configuration on CM5 side.

### Touch Controller — FT3519T (FULLY RESOLVED ✅)

| Parameter | Value | Source |
|-----------|-------|--------|
| IC model | FT3519T | `focaltech_config.h` line 223 |
| I2C address | 0x38 | `focaltech-ts.txt` confirmed |
| Compatible string | `focaltech,fts` | `focaltech-ts.txt` |
| Max simultaneous touches | 10 | `focaltech-ts.txt` |
| Display coords | 0 0 1079 1919 | `focaltech-ts.txt` |
| Linux driver | **Complete kernel source provided** | All focaltech_*.c files |
| Driver license | GPL v2 | `focaltech_core.c` header |
| Interface | I2C (primary) or SPI | Both supported |

**Ready-to-use DTS node for FT3519T:**
```dts
&i2c1 {
    focaltech@38 {
        compatible = "focaltech,fts";
        reg = <0x38>;
        interrupt-parent = <&gpio>;
        interrupts = <XX IRQ_TYPE_EDGE_FALLING>;
        focaltech,reset-gpio = <&gpio YY 0>;
        focaltech,irq-gpio = <&gpio XX 0x02>;
        focaltech,max-touch-number = <10>;
        focaltech,display-coords = <0 0 1079 1919>;
        status = "okay";
    };
};
```
Replace XX and YY with actual CM5 GPIO numbers once pin assignment is finalized.

**To integrate the driver:** Copy all focaltech_*.c and *.h files into `drivers/input/touchscreen/` in the CM5 kernel tree. Add `obj-$(CONFIG_TOUCHSCREEN_FT3519T) += focaltech_ts.o` to the Makefile. Enable in Kconfig. The driver handles firmware, ESD recovery, gesture detection — everything.

### DSC Configuration (for CM5 DRM Driver)

```c
/* Values from DSC_set_VESA1_2_10_10_slice1_20_1080x1920 */
struct drm_dsc_config dxq7d0023_dsc = {
    .dsc_version_major = 1,
    .dsc_version_minor = 2,       /* VESA DSC 1.2 */
    .bits_per_component = 10,
    .bits_per_pixel = 10 << 4,    /* 10.0 bpp (160 in 4-bit fractional) */
    .slice_height = 20,
    .slice_width = 1080,
    .pic_height = 1920,
    .pic_width = 1080,
    .initial_xmit_delay = 410,
    .initial_dec_delay = 724,
    .initial_scale_value = 25,
    .scale_increment_interval = 576,
    .scale_decrement_interval = 21,
    .first_line_bpg_offset = 13,
    .nfl_bpg_offset = 1402,
    .slice_bpg_offset = 797,
    .initial_offset = 5632,
    .final_offset = 4332,
    .flatness_min_qp = 7,
    .flatness_max_qp = 16,
    .block_pred_enable = 0,
    .convert_rgb = 1,
    .rc_model_size = 8192,
};
```

The display uses the **Hirose FH26-39S-0.3SHW** connector on the display side.

**Current status (June 25):** DXQ confirmed no standard 0.5→0.3mm adapter FPC exists. Two paths:

**Path A (preferred):** Ask DXQ to make a custom FPC adapter (0.3mm panel side → 0.5mm PCB side). Emily said they need the PCB-side connector spec first. Find a 0.5mm 39-pin ZIF on JLCPCB, send part number to Emily.

**Path B (backup):** Source Hirose FH26-39S-0.3SHW from Mouser, send to JLCPCB as customer-provided component before assembly.

**Does not block PCB order.** Use whichever connector is confirmed before assembly date (July 3-5).

---

## 7. Schematic Architecture

### Block Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CARRIER PCB                              │
│                                                                   │
│  USB-C ──► FUSB302 ──► BQ25895 ──► SYS ──► TPS61235 ──► 5V    │
│  (charging)  (PD)    (charger)     │           (boost)    │      │
│                           │        └──► VBAT ──► Display  │      │
│                           └──► BAT ──► Li-Po 10000mAh     │      │
│                                                            │      │
│                                        5V ──► SGM2036-3.3V──►3.3V│
│                                        3.3V──► SGM2036-1.8V──►1.8V│
│                                                            │      │
│  ┌─────────────────────────────────────────────────┐      │      │
│  │              CM5 (via 2× DF40 connectors)        │◄─────┘      │
│  │                                                   │             │
│  │  MIPI DSI ──────────────────────────────────────►│ Display FPC │
│  │  I2C ──────────────────────────────────────────►│ Touch + BQ  │
│  │  I2S ──────────────────────────────────────────►│ Mic + Amp   │
│  │  USB 2.0 D+/D- ──────────────────────────────►│ Mini PCIe   │
│  │  GPIO ────────────────────────────────────────►│ Buttons     │
│  │  GPIO ────────────────────────────────────────►│ RESX/TE/INT │
│  └─────────────────────────────────────────────────┘             │
│                                                                   │
│  Mini PCIe ──► EC25AFXGA ──► U.FL ──► LTE antenna               │
│  Nano SIM ──► EC25AFXGA                                          │
│  6-pin header ──► INMP441 mic module                             │
│  MAX98357A ──► 8Ω speaker                                        │
│  JST-PH ──► Li-Po battery                                        │
│  USB-C ──► (also available for data/programming)                 │
└─────────────────────────────────────────────────────────────────┘
```

### CM5 Pin Allocations (high-level)

| CM5 function | Used for |
|--------------|---------|
| MIPI DSI lanes 0-3 + clock | Display (5 differential pairs) |
| I2C bus 0 | BQ25895 battery management |
| I2C bus 1 | Display touch controller (FocalTech, confirm address 0x38 or 0x70 from piBrick DTS) |
| I2S (BCLK, LRCLK, SDI, SDO) | INMP441 mic + MAX98357A amp |
| USB 2.0 D+/D- | EC25 cellular modem (via mini PCIe) |
| GPIO (×8 minimum) | RESX, TE, TP-RESET, TP-INT, power btn, vol+, vol-, LED |
| GPIO (×2) | EC25 power enable, EC25 reset |
| SD card (CM5 Lite) | Note: CM5108064 has eMMC — no SD needed |
| PCIe | Not used (saved for future NVMe expansion if M.2 connector added) |
| 5V input | From TPS61235P boost converter output |

---

## 8. Power System Design

### Power Chain Detail

```
AC wall adapter
      │
      ▼
USB-C connector (C2858270, 16-pin, 3A rated)
      │
      ▼
FUSB302BMPX (USB-PD negotiation IC)
  - Communicates with charger via CC1/CC2 pins
  - Requests 9V/3A = 27W from compatible chargers
  - Falls back to 5V/3A = 15W if charger doesn't support PD
  - Connected to CM5 via I2C for status monitoring
      │
      ▼ (VBUS, up to 9V 3A)
BQ25895RTWR (battery management IC)
  - QFN-24-EP package, JLCPCB assembled
  - Charges Li-Po at up to 3.25A (configurable via I2C)
  - VSYSMIN register set to 3.8V (display VBAT minimum)
  - SYS output = max(VBAT, 3.8V) — always above 3.8V
  - I2C to CM5 for charge status, battery %, temperature
  ├──► SYS output (3.8-4.35V) ──► Display VBAT (pins 4-8 direct)
  ├──► SYS output ──► TPS61235PRWLR input
  └──► BAT ──► JST-PH connector ──► 10000mAh Li-Po

TPS61235PRWLR (boost converter)
  - Input: 3.5-4.35V from BQ25895 SYS
  - Output: 5.1V regulated, up to 3.5A
  - Efficiency ~90-92% at typical load
  - Powers CM5 + anything on 5V rail
      │
      ▼ (5V rail)
      ├──► CM5 5V input pins (via DF40 connectors)
      ├──► SGM2036-1.8YN5G/TR (1.8V LDO, C700371)
      │         └──► 1.8V rail: Display VDDIO, Display TP-1V8, RESX signal
      └──► SGM2036-3.3YN5G/TR (3.3V LDO, TBD LCSC#)
                └──► 3.3V rail: Display VCI, Display TP-VDD, mini PCIe 3.3V, audio amp, pull-ups
```

### Power Sequencing
OLED displays require power rails to come up in a specific order:
1. VDDIO (1.8V) must stabilize first
2. VCI (3.3V) comes up second
3. VBAT (3.8-4.5V) comes up last
4. Then RESX is de-asserted (pulled high) to release display from reset

Use enable pins on the LDOs to control sequencing. CM5 GPIO drives enable pins in order.

### Battery Life Estimates

| Usage mode | Power draw | Battery life (10000mAh) |
|------------|------------|------------------------|
| Light SSH + display at 50% | ~3.9W | ~9.5 hours |
| Active Claude Code session + display bright | ~5.8W | ~6.4 hours |
| Gaming (emulator) at full brightness | ~7.5W | ~4.9 hours |
| Standby (screen off, SSH idle) | ~1.2W | ~30 hours |

---

## 9. Outstanding Blockers

### BLOCKER 1: 39-pin 0.3mm FPC connector (CRITICAL)

**Status**: Not found on JLCPCB  
**Impact**: Cannot complete display section of PCB layout without this footprint  
**Actions**:
1. Search JLCPCB with these terms: `FPC 0.3mm 39`, `AFC07-S39`, `FH26-39 mating`, `ZIF 0.3mm 39pin`
2. If not on JLCPCB: search Mouser for Hirose FH52 series or Amphenol AFC07-S39-00 — source and send to JLCPCB as customer-provided component
3. Ask DXQ Emily if the panel ships with cable terminated to different pitch on board side

### Schematic Progress (June 25)

Power sheet ~90% complete in KiCad 9.0.7. Components placed and wired:
- BQ25895 with all passives ✅
- TPS61235P with all passives ✅
- FUSB302 with passives ✅
- SGM2036-3.3V LDO ✅
- SGM2036-1.8V LDO ✅
- USB-C connector J1 ✅
- Battery connector J2 ✅
- PWR_FLAGS ✅

Remaining sheets: CM5, Display, Cellular, Audio, Controls — to be generated via Claude Code.

### Hack Club Status

Submitted to #outpost-experts. Response from reviewer (1mon): "this sounds pretty cool. i'd like to see how the electronics work before being confident on X tier but at least S tier." 

**X tier is still achievable** — reviewer wants to see hardware progress. Completed schematic + PCB order is the unlock.

### Layer Count — Locked at 4 ✅

JLC04161H-3313 stackup:
- L1 (top): Signal — MIPI DSI, USB, sensitive signals
- L2: GND plane — solid copper
- L3: Power plane — 5V, 3.3V, 1.8V pours
- L4 (bottom): Signal — I2C, GPIO, audio, misc

piBrick uses 4 layers. CM5 reference designs use 4 layers. Correct choice for this design.

### Thermal Solution — Locked ✅

No fan. Passive solution:
- 2mm silicone or graphite thermal pad between CM5 metal lid and aluminum back plate
- 1mm aluminum back plate (laser-cut) on device back — acts as heatsink
- BQ25895 and TPS61235P: copper thermal pad + thermal via array to GND plane (required by datasheets)
- Sufficient for ~4W sustained operation without throttling

**Status**: Complete production init sequences for ALL FIVE refresh rate modes (60/90/120/144/165Hz) received from DXQ in debug package. DTS-ready 60Hz init sequence is in Section 6. All modes fully documented.

### ~~BLOCKER: Touch driver unknown~~ — FULLY RESOLVED ✅

**Status**: FT3519T confirmed. I2C address 0x38 confirmed. Compatible string "focaltech,fts" confirmed. Complete GPL v2 Linux kernel driver source received (all focaltech_*.c files). DTS node template in Section 6. Zero driver work needed — just compile in and configure.

### BLOCKER 3: SGM2036-3.3V not yet in JLCPCB cart (LOW)

**Status**: The 2.8V version was mistakenly added. Need 3.3V version.  
**Action**: Remove C154990 (2.8V). Search `SGM2036-3.3YN5G/TR` on JLCPCB. Should be straightforward.

### BLOCKER 4: Grant not yet approved (MEDIUM)

**Status**: Pitch submitted to Clay (Outpost organizer). X tier pitch submitted to alexren.  
**Impact**: CM5 and EC25 cannot be ordered yet (total ~$260)  
**Mitigation**: PCB design can proceed without parts in hand. If grant approval takes >48 hours, the CM5 should be ordered out-of-pocket and reimbursed — it ships overnight from Amazon.

### BLOCKER 5: MAX98357A and 0603 LED not yet confirmed on JLCPCB

**Action**: Search JLCPCB for `MAX98357A` and `0603 LED red`. Report stock levels.

---

## 10. Decisions Already Locked In

**Do not revisit these in the next chat session. Every one of these was debated and closed.**

| Decision | What was decided | Why it's locked |
|----------|-----------------|-----------------|
| Compute module | Raspberry Pi CM5108064 (8GB, 64GB eMMC, WiFi) | piBrick reference design, BCM2712 MIPI DSI validated with DXQ display, Pi OS ecosystem, available overnight on Amazon |
| NOT Orange Pi CM5 | Rejected despite better GPU | Driver unknowns + OS unknowns on 26-day timeline unacceptable. GPU only matters for gaming which is secondary feature. |
| NOT Radxa CM5 | Rejected | Out of stock everywhere in US |
| Cellular modem | EC25AFXGA-MINIPCIE (mini PCIe, North America) | LCC version requires hot plate reflow. Mini PCIe plugs in — zero soldering risk. AT&T + T-Mobile certified. |
| NOT EC25 LCC | Rejected | Too risky to hand-solder without good iron |
| Display | DXQ7D0023 7" OLED 1080×1920 | 7" is the right size for the form factor. Same manufacturer as piBrick's validated display. ICNA3512 driver work is tractable. |
| Storage | CM5 64GB eMMC (no NVMe) | eMMC is on the CM5 module itself. No extra connector needed. 64GB holds OS + Ollama models comfortably. M.2 M-key connector still added for optional expansion. |
| Battery | 10000mAh thin Li-Po (100×60×11mm, PH2.0) | ~8-9 hours, fits device body, PH2.0 matches PCB JST connector |
| Microphone | INMP441 module via 6-pin female header | Plugs in, zero soldering, hand assembled |
| Speaker | 8Ω speaker via MAX98357A I2S amp | Same I2S bus as mic |
| LED | Through-hole red LED, hand soldered | JLCPCB doesn't stock 0402 LEDs reliably |
| Boost converter | TPS61235PRWLR | Handles CM5 5V requirement from 3.7-4.35V battery voltage |
| Battery management | BQ25895RTWR | Industry standard, I2C controlled, handles USB-PD input |
| USB-PD | FUSB302BMPX | Standard PD negotiation IC, 9V/3A = 27W charging |
| PCB fabrication | JLCPCB 4-layer with SMT assembly | Extended parts, handle all SMD components. User only plugs in modules. |
| Enclosure | SLA resin, friend prints | Free (cost of resin ~$10-15) |

---

## 11. Software Stack

### Operating System
Raspberry Pi OS Lite (64-bit, Bookworm). Headless base, then add only what's needed. No desktop environment — the session manager IS the UI.

### Display / UI Framework
Two options being considered:
1. **Wayland + custom Python app (Textual or similar)** — Full Linux desktop, runs apps natively
2. **Framebuffer app** — Lighter, boots straight to the session manager without a compositor

Recommendation: Wayland with a minimal compositor (weston or sway in kiosk mode), custom session manager app written in Python using Kivy or a web app served via ttyd. Touch input via evdev through Wayland.

### Session Manager App
Custom-built application. Boots automatically on startup. Displays:
- Home screen: grid of AI sessions (Claude Code, Codex, Gemini, Ollama, custom)
- Each session shows: name, status (idle/running/completed), last output preview, latency
- Tap to connect via mosh SSH
- Swipe to switch between active sessions
- Status bar: signal strength (LTE/WiFi), battery %, time, active session count

### SSH/Remote Access
- **mosh** instead of plain SSH — survives cellular IP changes and brief dropouts
- **tmux** on the remote machine — sessions persist even if connection drops
- Supports connecting to: home server, Amazon Bedrock machine, Google Cloud machine, any SSH target

### AI Providers
- **Claude Code** — SSH to remote machine running `claude` CLI
- **Codex** — SSH to remote machine running `codex` CLI  
- **Gemini** — SSH to remote running `gemini` CLI, OR direct API call from device
- **Ollama** — SSH to remote machine, OR run locally on CM5 for offline use
- **Amazon Bedrock** — SSH to remote AWS machine
- **Google Cloud / Vertex AI** — SSH to remote GCS machine

### Gaming
- **RetroArch** with cores: mGBA (GBA), Mupen64Plus (N64), PPSSPP (PSP), DuckStation (PS1), PCSX2 (PS2, borderline)
- Controllers: keyboard attachment (built at hackathon) or USB OTG gamepad

### Local LLM (offline fallback)
- **Ollama** running on CM5 locally
- Models that fit in 8GB RAM: Llama 3.2 3B (~2GB), Phi-3 Mini (~2.3GB), Gemma 2 2B (~1.6GB)
- Performance: ~4-8 tokens/second on BCM2712 — usable for short queries, slow for long context

---

## 12. Linux Display Driver Plan

### Status: All driver materials in hand ✅

Complete production-grade driver package received from DXQ June 23. Every question about display bring-up is now answered. What remains is translation and integration work, not research.

### The Source Material

**`dsi-panel-7inch-vrr-cmd.TXT`** is a Qualcomm MDSS format panel driver. It was written for Android phones (Qualcomm Snapdragon) but the MIPI DCS command bytes inside are universal — they work identically on the CM5's BCM2712 DSI host. The only work is reformatting from Qualcomm wrapper syntax to Linux DRM panel format. The bytes themselves do not change.

**FocalTech FT3519T driver** is complete GPL v2 kernel source. Drop the files into `drivers/input/touchscreen/`, add to Makefile and Kconfig, done.

### Plan A: panel-simple-dsi Device Tree Overlay (Preferred)

Complete 60Hz DTS init sequence is in Section 6, ready to compile. Full overlay:

```dts
/ {
    fragment@0 {
        target = <&dsi1>;
        __overlay__ {
            status = "okay";
            #address-cells = <1>;
            #size-cells = <0>;

            panel@0 {
                compatible = "dxq,dxq7d0023";
                reg = <0>;
                reset-gpios = <&gpio XX GPIO_ACTIVE_LOW>;
                vddio-supply = <&vddio_1v8>;
                vci-supply = <&vci_3v3>;
                width-mm = <87>;
                height-mm = <155>;

                /* Full init sequence in Section 6 */

                display-timings {
                    timing0: 60hz {
                        clock-frequency = <147657600>;
                        hactive = <1080>;
                        vactive = <1920>;
                        hfront-porch = <156>;
                        hback-porch = <23>;
                        hsync-len = <1>;
                        vfront-porch = <2760>;
                        vback-porch = <15>;
                        vsync-len = <1>;
                    };
                };
            };
        };
    };
};
```

Compile with `dtc`, load in `/boot/overlays/`. No kernel recompilation.

### Plan B: Custom DRM Panel Driver

Write a minimal C kernel module. piBrick (github.com/amarullz/piBrick) has a working DXQ AMOLED driver — use as template. Init bytes from Section 6 drop straight in.

### Touch Driver Integration

```
1. Copy all focaltech_*.c and *.h files to drivers/input/touchscreen/focaltech_ts/
2. Add to drivers/input/touchscreen/Makefile:
   obj-$(CONFIG_TOUCHSCREEN_FT3519T) += focaltech_ts/
3. Add to Kconfig, enable in menuconfig
4. Add DTS node (template in Section 6) with correct GPIO numbers
5. Boot — driver auto-detects FT3519T at 0x38 and loads
```

### Refresh Rate Bring-Up Sequence

Start at 60Hz (simplest, no DSC complications on host side), then unlock higher rates:

1. **60Hz first** — DTS overlay, no DSC, confirm display lights up and touch works
2. **165Hz second** — Simplest init of all high-rate modes, no DSC configuration change needed compared to 60Hz (same DSC parameters, just different timing and `48 20`)
3. **120Hz/144Hz** — Requires CM5 DSI host DSC configuration using the PPS parameters in Section 6
4. **90Hz** — Same WRDSIM as 60Hz, just different B3/D3 timing group values

---

## 13. Assembly Plan

### What JLCPCB assembles (you do nothing)
All SMD components on the PCB:
- DF40 CM5 connectors
- BQ25895 (QFN-24)
- TPS61235P (VQFN-9)
- FUSB302 (WFQFN-14)
- Both LDOs (SOT-23-5)
- USB-C receptacle
- Mini PCIe slot
- SIM tray
- U.FL connectors ×2
- Tactile buttons ×3
- JST connector
- MAX98357A
- LED
- FPC ZIF connector
- All passives (resistors, capacitors, inductors)

JLCPCB machines place and reflow everything. You receive a fully populated PCB.

### What you hot plate (one session)
Using hot plate + solder paste syringe:
- **M.2 M-key connector** (if included): Large SMD pads, straightforward. Apply paste with syringe, place, reflow ~230°C.

### What you plug in (no soldering at all)
- **CM5 module** → presses into 2× DF40 connectors
- **EC25AFXGA cellular modem** → slides into mini PCIe slot, one screw
- **Display FPC ribbon** → inserts into ZIF connector (flip lock to secure)
- **INMP441 mic module** → plugs into 6-pin female header
- **SIM card** → slides into push-push SIM tray
- **Battery** → JST-PH 2-pin connector
- **LTE antenna** → snaps onto U.FL connector
- **WiFi antenna** → snaps onto U.FL connector
- **Speaker** → connects to MAX98357A output pads

### What you hand solder
- **Through-hole LED** — two legs, easy
- That's literally it

### Tools needed
- Hot plate (or toaster oven with reflow profile) — ~$25 Amazon if you don't have one
- Solder paste syringe (63/37 or SAC305)
- Tweezers
- Magnifying glass
- Soldering iron (only for the LED)
- Small Phillips screwdriver (for M.2 modem mounting screw)

---

## 14. Open Sauce Demo Plan

### The scenario
Open Sauce, San Francisco, July 18-20. 35,000 attendees. Your booth has the device, a printed PCB schematic poster, and the GitHub repo QR code.

### The 60-second demo script
1. Show the device — hold it like a phone. "This is a custom-built AI terminal. I designed the PCB from scratch."
2. Open the session manager — "This shows my active AI sessions. I have Claude Code running on a remote server right now."
3. Switch to Claude Code session — type a short command, show it responding over LTE.
4. Show the signal bar — "No WiFi. Pure cellular."
5. Switch to a game while Claude is running — "While the AI is working, I can play. Device built this."
6. Show the PCB schematic poster — "Every component. 4-layer board. Custom carrier for the Raspberry Pi CM5."

### What makes people stop
- A 7" OLED showing a terminal in a device this small
- Handing it to someone and saying "ask it anything"
- Showing that it works with cellular signal bar visible, no hotspot

### Keyboard attachment (built on-site)
The 4-day hackathon before Open Sauce is the build window for the Hall Effect keyboard attachment. Surface Pro-style pogo pins + magnets. If it's ready, snap it on for the demo — "and here's the keyboard." If it's not ready, the device demos fine without it.

---

## 15. Key Reference Links

| Resource | URL | Why it matters |
|----------|-----|----------------|
| piBrick Pocket-CM5 | github.com/amarullz/piBrick | GPL 3.0 open source CM5 handheld with DXQ AMOLED. Primary schematic reference. CM5 DF40 wiring, power section template. |
| DXQ display manufacturer | dxqlcd@dxq-lcd.com | Contact: Emily. Display $59 confirmed. Full driver package received. |
| JLCPCB assembly parts | jlcpcb.com/parts | Search all SMD parts here before adding to schematic |
| LCSC component search | lcsc.com | Full LCSC catalog — JLCPCB uses LCSC part numbers |
| CM5 datasheet | datasheets.raspberrypi.com/cm5 | Essential for carrier board design — DF40 pin functions, power requirements |
| BQ25895 datasheet | ti.com (search BQ25895) | Battery management IC register map and application circuit |
| TPS61235P datasheet | ti.com (search TPS61235) | Boost converter application circuit and component selection |
| FUSB302 datasheet | onsemi.com | USB-PD IC application circuit |
| EC25 hardware design guide | Quectel (search EC25 hardware design) | Mini PCIe footprint and USB routing requirements |
| Hack Club Outpost | stardance.hackclub.app | Project tiers, X tier submission |
| **DXQ Debug Files** | Project files | `dsi-panel-7inch-vrr-cmd.TXT` — complete VRR panel driver all 5 modes. FocalTech FT3519T complete kernel driver source. DSC PPS parameters. |

---

## 16. Immediate Next Actions

**1. RIGHT NOW — Claude Code schematic generation**
Run Claude Code in project directory with claude-opus-4-6 model:
```
cd "C:\Users\dryah\OneDrive\Desktop\HACK CLUB RELATED\Outpost\Universal AI Terminal\HACK CLUB RELATED"
claude --model claude-opus-4-6
```
Prompt: Read Power.kicad_sch and this briefing, then generate CM5.kicad_sch, Display.kicad_sch, Cellular.kicad_sch, Audio.kicad_sch, Controls.kicad_sch using identical library references and formatting.

**2. FPC connector — find 0.5mm ZIF on JLCPCB**
Search `0.5mm pitch 39pin ZIF FPC connector` — get part number, email Emily with the spec so she can confirm custom cable feasibility.

**3. JUNE 27 (Friday) — PCB order deadline**
Order with expedited 4-layer build. Boards arrive July 3-5. Two full weeks before Open Sauce.

**4. WHEN GRANT APPROVED**
- CM5108064 Amazon overnight: $185
- EC25AFXGA-MINIPCIE Mouser: $75
- DXQ7D0023 from Emily: $59
- Battery, mics, speaker, antennas Amazon: ~$50

---

## Appendix A: Full Budget Breakdown

| Item | Source | Cost |
|------|--------|------|
| CM5108064 (8GB, 64GB eMMC, WiFi) | Amazon | $185 |
| EC25AFXGA-MINIPCIE | Mouser | $75 |
| DXQ7D0023 7" OLED | DXQ direct | $59 |
| 10000mAh Li-Po battery | Amazon | $17 |
| INMP441 mic modules ×5 | Amazon | $12 |
| Speaker 8Ω | Amazon | $5 |
| LTE antenna (U.FL) | Amazon | $5 |
| WiFi antenna (U.FL) | Amazon | $4 |
| Through-hole LED | Amazon | $2 |
| JAE M.2 M-key connector | Mouser | $2 |
| All JLCPCB assembled SMD parts | JLCPCB | ~$15 |
| PCB fabrication 4-layer ×5 | JLCPCB | ~$60 |
| JLCPCB SMT assembly | JLCPCB | ~$65 |
| Enclosure resin | Friend's printer | ~$12 |
| Shipping (various) | Various | ~$20 |
| **Total** | | **~$538** |

**This is 53.8% of the $1,000 X tier ceiling.** Not excessive. Every line item is necessary.

---

## Appendix B: Why This Isn't Excessive Spending

A direct comparison to commercial alternatives:

| Device | Price | Custom hardware | LTE | AI native | Open source |
|--------|-------|----------------|-----|-----------|-------------|
| This project | $538 | ✅ Custom PCB | ✅ | ✅ | ✅ |
| GPD Pocket 3 | $699 | ❌ | ❌ | ❌ | ❌ |
| GPD Win Mini | $599 | ❌ | ❌ | ❌ | ❌ |
| Steamdeck OLED | $549 | ❌ | ❌ | ❌ | ❌ |
| Unihertz Titan | $459 | ❌ | ✅ | ❌ | ❌ |

The device doesn't just cost $575 — it demonstrates $575 worth of hardware engineering that doesn't exist in any commercial product.
