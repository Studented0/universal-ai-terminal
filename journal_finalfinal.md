

---

# 6/22/2026 4 PM - all the component searching

_Time spent: 5h_

went through JLCPCB part by part. EC21 variants on JLCPCB are useless for North America, wrong bands and basically no stock. I went to Mouser and found the EC25AFXGA-MINIPCIE which is certified for AT&T and T-Mobile. But its mini PCIe form factor meaning it plugs in instead than being soldered. 

caught a mistake. I had the SGM2036-2.8V LDO in the cart for the display VCI rail but the datasheet says VCI is 3.3V not 2.8V. that would have been a dead board. removed it. also found the INMP441 mic on JLCPCB is overpriced and out of stock so grabbed a 5-pack on Amazon for $11.99. they have through hole pins so the module just plugs into a header on the board instead of being SMD soldered.

BOM is around $575-580.

---

# 6/22/2026 6 PM - display research rabbit hole

_Time spent: 4h_

needed to figure out the display. found the piBrick project, released June 1st, fully open source. it is a handheld CM5 computer using a DXQ AMOLED display connected over MIPI DSI. the fact that it exists and works is the biggest risk reduction for the whole project. it proves DXQ plus CM5 plus MIPI DSI is a working combination.

their display is 3.92 inches which felt too small for a terminal. found the DXQ7D0023 in the catalog, 7 inch, 1080x1920, 165Hz, touch included. listed at $96 publicly. emailed DXQ directly for sample pricing and the datasheet. the 7 inch size is wider than a phone but narrower than a Switch, fits in most pockets, and the screen size makes the terminal actually usable and the demo visible from a distance at Open Sauce.

during the research I asked another AI about the display driver IC and it confidently told me it was the SH8804B from Sino Wealth with no Linux support and that I would need an HDMI bridge chip. I was starting to plan a whole alternate path around that. DXQ then sent the actual datasheet and the driver is the ICNA3512, completely different chip, with an init sequence that lets me write a device tree overlay without recompiling the kernel. lesson learned about trusting AI for datasheet lookups.

---

# 6/22/2026 11 PM - parts locked in, DXQ responded, submitted pitch

_Time spent: 2h_

DXQ sent back the full DXQ7D0023 spec sheet and the ICNA3512 driver datasheet. timing parameters are all in there. 60Hz: HFP=156, HBP=23, VFP=20, VBP=15. same level of detail for every other refresh rate. writing the device tree overlay is now a defined task instead of a question mark.

submitted the official project pitch through the proper form. covers the full device: custom carrier PCB, CM5, LTE, 7 inch AMOLED, Claude Code and Ollama, gaming while waiting on prompts. also mentioned I have other projects ready as booth backup so the demo always has something to show regardless.

the FPC connector is still a problem. the display has a 0.3mm pitch 39 pin connector and JLCPCB might not stock 0.3mm ZIF connectors at all. looking at Mouser as a backup. grant is also not approved yet so the CM5 and EC25 are on hold but the CM5 is overnight on Amazon so that is not a hard blocker. PCB has to go in by June 26 and the schematic has not been started yet.

---

# 6/23/2026 - DXQ sent the full driver package, display is completely solved

_Time spent: 6h_

emailed DXQ asking for the init code and driver files. they sent back a full zip with a DSC folder, a non-DSC folder, and a FocalTech touch driver. the main file is a full Qualcomm MDSS panel driver with complete init sequences for all five refresh rates: 60, 90, 120, 144, and 165Hz. was told earlier that 144Hz was not supported. it is. the touch driver is complete GPL v2 Linux kernel source for the FT3519T, ready to compile. I2C address 0x38, compatible string focaltech,fts.

also found an error I had made earlier. I had decoded the OSC config register as CE 22 from a screenshot. the production driver file says CE 52. the driver files are the ground truth, not screenshots.

display sample price came back at $59, not the $96 listed publicly. BOM drops to around $538. sent DXQ the board side connector info (C2797220, 40 pin 0.5mm ZIF from Kinghelm) and asked if they can make a matching pitch adapter cable. waiting on confirmation before deciding how to handle the 0.3mm to 0.5mm mismatch.

---

# 6/23/2026 - first time opening KiCad for real, power sheet done

_Time spent: 8h_

started the schematic from scratch in KiCad 9.0.7. set up a hierarchical structure with six sheets: Power, CM5, Display, Cellular, Audio, Controls.

the power sheet took most of the day. placed the BQ25895 first and wired every pin. the label system in KiCad took a while to fully understand: local labels stay on one sheet, hierarchical labels cross between sheets, power symbols are global. once that clicked the workflow got a lot faster. TPS61235P boost converter followed, then the FUSB302, both LDOs, USB-C connector, JST battery connector, and PWR_FLAG symbols.

had to search for a while to find the right inductor for the BQ25895. the first JLCPCB results were 0806 package parts rated 1.1 to 2.7A which is not enough headroom for a 3A charger. had to search 1210 package specifically to find anything above 4A saturation current.

heard back about the pitch. the reviewer said it sounds cool and wants to see the electronics before committing to X tier. at minimum it is S. X tier is still in play and finishing the schematic is literally what unlocks the funding level.

---

# 6/25/2026 - tried AI schematic generation, learned its limits

_Time spent: 10h_

tried using AI code generation to build the remaining KiCad sheets automatically. it read the power sheet for format context, fetched the official Raspberry Pi CM5IO files from GitHub, extracted all 200 DF40 pin assignments, and generated all five sheets in about 45 minutes. the pin data it pulled was actually accurate: DSI1 lanes, I2C buses, USB pins all checked out against the official RPi files.

loaded everything in KiCad and it was completely broken. components were placed at the right positions but wire endpoints did not connect to pin stubs. in KiCad a net label that is even 1 mil off a pin is fully disconnected. ran two rounds of automated coordinate fixes. still broken after both.

decided to scrap the generated sheets and redo all five manually. kept the power sheet which works fine. estimated three and a half hours for the remaining sheets with proper pin tables in front of me. updated the briefing with complete pin tables and net label details for every component so the next session starts immediately.

---

# 6/26/2026 - schematic marathon, all 6 sheets done

_Time spent: 14h_

started on the CM5 sheet and had to verify every single pin from scratch. the pin numbers from the previous session were wrong almost across the board. 5V inputs were listed as pins 1-4 but those are ethernet and GND. the real 5V inputs are pins 77, 79, 81, 83, 85, 87. USB DM and DP were on the wrong connector entirely. went through the full CM5 datasheet line by line.

caught two design errors while doing this. the LDO enable pins were tied to +3V3 which is a chicken and egg problem since the LDO cannot turn itself on. changed both to +5V from the boost converter which is available first. also found the CM5 has a dedicated PWR_Button pin (pin 92) that handles power on and off without needing a GPIO at all, just wires straight to a button and ground.

added a second USB-C port for data after realizing the 16 pin charging port physically cannot carry USB 3.0 because it does not have the SuperSpeed pairs. added a 24 pin connector with a two transistor load switch for VBUS control. finished all six sheets including cellular, audio, and controls. the cellular sheet was fast since most of the PCIe pairs on the mini PCIe slot are NC because the EC25 uses USB 2.0 internally.

ran ERC after all six sheets and got around 200 errors. almost all were hierarchical label mismatches. fixed by converting everything to global labels which connect automatically by name across all sheets. wrote a Python script to do the rename in the .kicad_sch files directly since doing 40 labels by hand would have taken hours. ERC went from 200 errors to clean.

---

# 6/27/2026 - PCB layout, routing, and the ordering nightmare

_Time spent: 16h_

started PCB layout. board is 88 by 155mm, 4 layer JLC04161H-3313 stackup. set up design rules and net classes with MIPI DSI differential pair settings at 0.1mm trace and 0.1mm gap for 90 ohm impedance on the outer layer.

placement took most of the morning. fixed connectors went first: display FPC at top, USB-C ports at bottom, mini PCIe and SIM on the right, buttons on the right edge. CM5 connectors in the upper center, power ICs near the charging port, LDOs between the CM5 and FPC connector since they power the display directly.

the MIPI DSI routing was the hardest part. the CM5 J2 connector and the FPC connector are not directly across from each other and getting all differential pairs routed cleanly without vias was not possible with this placement. ended up routing some pairs through the back copper which is fine because the BCM2712 supports lane polarity inversion in device tree. D2 pair ended up inverted, will fix in the DTS with lane-polarities = <0 0 0 1 0>. all five DSI pairs ended up within 5mm of each other in total length which is within tolerance. USB 3.0 RX pair also inverted at the CM5 side, needs a matching DTS fix.

the JLCPCB BOM tool had some issues. it matched a resistor to a through hole package that would not have been assembled and could not match the inductors at all. also the CM5 combined footprint shows as one component but needs two physical DF40 connectors at specific coordinates. left a note ready for the engineer for when the order goes in. cart is finalized and ready to submit.

---

# 6/28/2026 - DXQ cable drama, aluminum plate, and wrapping up

_Time spent: 4h_

the FPC cable is the last unresolved problem. the display has a 0.3mm pitch 39 pin connector and the carrier board has a 0.5mm pitch 40 pin ZIF. those do not connect directly. DXQ quoted custom cables but also mentioned a $0.79 adapter from Taobao. the problem is that adapter is only 31 pins and the display needs all 39. pins 32 through 38 are the touch controller I2C, reset, and interrupt lines. a 31 pin cable leaves the touch completely disconnected. sent a follow up asking how that would work. display itself is $56 regardless of how the cable gets resolved.

figured out the physical stack. aluminum plate on the bottom, thermal pad on top of that, PCB, battery, display. the thermal pad covers the full back face of the board so the aluminum cannot short anything even if it contacts a pad. CM5 heat goes through thermal vias to the pad to the plate. anodized black finish adds another layer of insulation.

still waiting to hear back on X tier confirmation, which would mean the full $1000 budget plus a travel stipend covering the Houston to SF flight. holding off on ordering anything until that comes through. Open Sauce starts July 18, so the runway is shrinking either way.

---

# 6/29/2026 - exact cost quotes locked in, BOM finalized, repo on GitHub

_Time spent: 5h_

got exact pricing for everything instead of rough estimates. JLCPCB cart comes to $225.86, CNC plate $24, EC25 from Mouser $94.92, Amazon cart $288, display $56. cable is not finalized but $10 is the max. grand total estimate is $700.28. still have not ordered anything, holding off until X tier comes through so I am not stuck covering it myself if it does not.

built a full itemized BOM CSV and caught two missing parts in the process, a 3 pin header for the UART debug port and two female sockets for the mic modules. both under $2 combined, flagged so they do not get missed once the order actually goes in.

got the GitHub repo set up and pushed. ran into some issues with PowerShell vs Bash syntax but got it sorted. repo is live now.

next step is hearing back on X tier, then placing every order at once. boards take about a week to arrive once ordered, which still leaves time before Open Sauce if confirmation comes soon.
