# Universal AI Terminal

A pocketable AI terminal that runs Claude Code and Ollama over LTE. Custom carrier board for a Raspberry Pi Compute Module 5, 7" AMOLED touchscreen, and its own cellular modem so it doesn't need WiFi. While a long prompt is running, you can play a game on it instead of staring at the terminal.


---

## Screenshots

<img width="485" height="793" alt="Screenshot 2026-06-30 094633" src="https://github.com/user-attachments/assets/483ea5d5-be49-4eee-a808-c80d7e40a9d3" />
<img width="1234" height="862" alt="Screenshot 2026-06-30 094547" src="https://github.com/user-attachments/assets/769ba77c-d8a8-4b2c-b674-d24f488ab921" />
<img width="1253" height="876" alt="Screenshot 2026-06-30 094539" src="https://github.com/user-attachments/assets/5cda75c7-c588-4561-a9cb-6e4d0a3244b9" />
<img width="1239" height="880" alt="Screenshot 2026-06-30 094531" src="https://github.com/user-attachments/assets/baaa9f2a-fa27-41dd-b135-a97c05b5a0f5" />
<img width="1286" height="930" alt="Screenshot 2026-06-30 094522" src="https://github.com/user-attachments/assets/b1f6addc-8972-4dab-820d-04bf2caefd0d" />
<img width="1298" height="896" alt="Screenshot 2026-06-30 094512" src="https://github.com/user-attachments/assets/acd8a52b-8dde-48e2-b267-9d8159dbd41d" />
<img width="1240" height="860" alt="Screenshot 2026-06-30 094501" src="https://github.com/user-attachments/assets/461ff3dc-e01f-44fe-8a17-15d3a07eaa72" />
<img width="485" height="793" alt="Screenshot 2026-06-30 094633" src="https://github.com/user-attachments/assets/6a513c7f-e12c-4edd-861b-ea33ac16b90e" />
<img width="477" height="791" alt="Screenshot 2026-06-30 094626" src="https://github.com/user-attachments/assets/15d45b7e-aea7-45d7-91d7-e1825783d8cf" />
<img width="482" height="803" alt="Screenshot 2026-06-30 094620" src="https://github.com/user-attachments/assets/28eb3442-ae35-478f-9bb1-547e95efbe8d" />
<img width="469" height="796" alt="Screenshot 2026-06-30 094611" src="https://github.com/user-attachments/assets/7ac7b0bd-54ad-4977-858d-b0a53479d7a9" />


---

## Why I built this

I kept wanting Claude Code running when I was away from my desk, and there was no good way to do that besides carrying a laptop everywhere. There are videos all over the internet of people sleeping next to a laptop with Claude Code running waking up to accept permissions, or walking around a grocery store with their laptop open, looking crazy. I wanted something pocketable that solves that.

## Hardware

88×155mm, 4-layer board (JLC04161H-3313 stackup), designed in KiCad 9. Six hierarchical schematic sheets: Power, CM5, Display, Cellular, Audio, Controls.

**Compute** — Raspberry Pi Compute Module 5 (8GB RAM, 64GB eMMC, WiFi). Quad-core Cortex-A76 @ 2.4GHz. 

**Display** — DXQ7D0023, 7" AMOLED, 1080×1920, up to 165Hz variable refresh. ICNA3512 driver IC. FT3519T capacitive touch (FocalTech, I2C address 0x38).  Panel connector is a Hirose FH26-39S-0.3SHW (39-pin, 0.3mm pitch); board side is a 40-pin 0.5mm ZIF (Kinghelm KH-FG0.5-H2.0-40PIN), pins 1-39 mapped straight through, pin 40 unused.

**Cellular** — Quectel EC25AFXGA-MINIPCIE, Cat 4 LTE, AT&T/T-Mobile certified for North America. Mini PCIe form factor so it plugs in rather than getting hand-soldered. Uses USB 2.0 internally, not PCIe.

**Power** — BQ25895 handles battery charging and power path from USB-C input. TPS61235P boosts battery voltage up to the 5V the CM5 needs. FUSB302 negotiates USB-PD for faster charging. Two SGM2036 LDOs step down to 3.3V and 1.8V for the display and peripherals.

**I/O** — Two USB-C ports: one power and USB 2.0 (charging), one full data port with USB 3.0 SuperSpeed and a two-transistor load switch for VBUS control. Three tactile buttons (volume up/down, power; though power itself uses the CM5's dedicated PWR_Button pin and needs no GPIO at all). UART debug header, Test Points for power.

**Battery** — 10,000mAh Li-Po.

---

## Enclosure

3mm black-anodized aluminum plate on the back (CNC machined, doubles as a heatsink and structural backing), a thermal pad between the board and plate, then a bottom shell. 

---

## Software

Raspberry Pi OS Lite (64-bit, Bookworm), headless. 
---

## Bill of Materials


Full itemized BOM across all vendors: [`BOM_Universal_AI_Terminal.csv`](BOM_Universal_AI_Terminal.csv)

---

## Repository Structure

```
universal-ai-terminal/
├── HACK CLUB RELATED.kicad_pro    # KiCad project file 
├── HACK CLUB RELATED.kicad_sch    # schematic
├── HACK CLUB RELATED.kicad_pcb    # PCB layout
├── HACK CLUB RELATED.kicad_prl
├── HACK CLUB RELATED.step         # 3D STEP export of the board
├── power.kicad_sch                # Power sheet
├── CM5.kicad_sch                  # CM5 sheet
├── display.kicad_sch              # Display sheet
├── Cellular.kicad_sch             # Cellular sheet
├── audio.kicad_sch                # Audio sheet
├── controls.kicad_sch             # Controls sheet
├── convert_hlabels.py             # script used to convert hierarchical labels to global 
├── libs/easyeda/                  # imported EasyEDA symbols and footprints
├── production/                    # gerbers, BOM, CPL; JLCPCB Fabrication Toolkit output
├── HACK CLUB RELATED.SLDASM       # SolidWorks enclosure assembly
├── Part8.SLDPRT                   # SolidWorks enclosure part
├── BOM_Universal_AI_Terminal.csv  # full itemized BOM
├── journal.md                     # build log
├── LICENSE
└── README.md
```

`.kicad_sch.bak` files and KiCad's auto-generated `-backups/` folders are local working files, not meant to be tracked — they'll stay out of future commits once `.gitignore` is fixed.

---

## License

[MIT](LICENSE)
