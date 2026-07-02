

# 6/22/2026 4 PM - all the component searching

_Time spent: 5h_

went through JLCPCB part by part. EC21 variants on JLCPCB are useless for North America, wrong bands and basically no stock. I went to Mouser and found the EC25AFXGA-MINIPCIE which is certified for AT&T and T-Mobile. But its mini PCIe form factor meaning it plugs in instead than being soldered. 

Also Caught a mistake. I had the SGM2036-2.8V LDO in the cart for the display VCI rail, but the datasheet says VCI is 3.3V, not 2.8V. also found the INMP441 mic on JLCPCB is overpriced and out of stock so decided on a 5-pack on Amazon for $11.99. they have through-hole pins, so the module just plugs into a header on the board instead of being SMD soldered.

---

# 6/22/2026 6 PM - display research rabbit hole

_Time spent: 4h_

needed to figure out the display. found the piBrick project, released June 1st, fully open source. it is a handheld CM5 computer using a DXQ AMOLED display connected over MIPI DSI. 

their display is 3.92 inches, which was too small. found the DXQ7D0023 in the catalog, 7 inch, 1080x1920, 165Hz, capacitave touch. listed at $96 publicly. emailed DXQ directly for sample pricing and the datasheet. the 7 inch size is similar to a iPhone 17 Pro Max but narrower than a Switch, fits in pockets, and the screen size makes the terminal actually usable and the demo visible.

During the research I asked gemini about the display driver IC and it confidently told me it was the SH8804B from Sino Wealth with no Linux support and that I would need an HDMI bridge chip. I was starting to plan a whole alternate path around that. DXQ then sent the actual datasheet, and the driver is the ICNA3512, and they gave me an init sequence that lets me write a device tree overlay without recompiling the kernel. Don't trust AI for everything LOL.

---

# 6/22/2026 11 PM - parts locked in, DXQ responded

_Time spent: 2h_

DXQ sent back the full DXQ7D0023 spec sheet and the ICNA3512 driver datasheet. Timing parameters are all in there. 60Hz: HFP=156, HBP=23, VFP=20, VBP=15. Same level of detail for every other refresh rate. 

the FPC connector is still a problem. the display has a 0.3mm pitch 39-pin connector, and JLCPCB does not stock 0.3mm ZIF connectors at all.

---

# 6/23/2026 - DXQ sent the full driver package, display is completely solved

_Time spent: 6h_

Emailed DXQ asking for the init code and driver files. they sent back a full zip with a DSC folder, a non-DSC folder, and a FocalTech touch driver. The main file is a full Qualcomm MDSS panel driver with complete init sequences for all five refresh rates: 60, 90, 120, 144, and 165Hz. the touch driver is complete GPL v2 Linux kernel source for the FT3519T.

Display sample price came back at $59, not the $96 listed publicly. sent DXQ the board side connector info (C2797220, 40 pin 0.5mm ZIF from Kinghelm) and asked if they can make a matching pitch adapter cable. waiting on confirmation before deciding how to handle the 0.3mm to 0.5mm mismatch.
[ICNA3512_Preliminary Datasheet_V0.00.pdf](https://github.com/user-attachments/files/29510919/ICNA3512_Preliminary.Datasheet_V0.00.pdf)
[DXQ7D0023_AMOLED规格书_HDR_10bit.pdf](https://github.com/user-attachments/files/29510915/DXQ7D0023_AMOLED._HDR_10bit.pdf)
[7D0023调试资料.zip](https://github.com/user-attachments/files/29510878/7D0023.zip)

---

# 6/23/2026 - first time opening KiCad for real, power sheet done

_Time spent: 8h_

Started the schematic from scratch in KiCad 9.0.7. Set up a hierarchical structure with six sheets: Power, CM5, Display, Cellular, Audio, Controls.

The power sheet took most of the day. 

Had to search for a while to find the right inductor for the BQ25895. The first JLCPCB results were 0806 package parts rated 1.1 to 2.7A which is not enough headroom for a 3A charger. had to search 1210 package specifically to find anything above 4A saturation current.
I was using hierarchical labels, but little did I know that would come back to stab me. Using a USB 2.0 with PD as the main charging port, with USB 2 data support if needed. Later on added some test points so I can check if any major power problems are happening
<img width="1203" height="877" alt="image" src="https://github.com/user-attachments/assets/289c9d71-714d-405a-b627-f30b13227d44" />

---


# 6/26/2026 10 AM - CM5 sheet, pin verification, catching design errors

_Time spent: 5h_

Started on the CM5 sheet and immediately ran into a problem. The pin table from the previous attempt had almost every pin number wrong. I had to pull up the official CM5 datasheet and go through all 200 pins line by line to build a correct table again but correctly this time before touching anything in KiCad.

biggest corrections: the 5V supply inputs are at pins 77, 79, 81, 83, 85, 87 -- not pins 1-4 like the generated data said. pins 1-4 are Ethernet and GND. USB DM and DP were assigned to the wrong connector entirely.

while wiring caught two design errors that would have killed the board. the enable pins on both LDOs were tied to +3V3, which is the LDO output; the LDO can't turn itself on from its own output rail. fixed both enable pins to tie to +5V from the boost converter instead, which comes up first. also found that the CM5 has a dedicated PWR_Button pin (pin 92) that handles power on and off natively with no GPIO needed at all. removed the GPIO power button wiring and just connected pin 92 directly to a button and GND.

<img width="1298" height="896" alt="image" src="https://github.com/user-attachments/assets/94dcb9c0-1a49-4171-a477-cabbdda7c306" />
<img width="1295" height="803" alt="Screenshot 2026-06-26 103300" src="https://github.com/user-attachments/assets/a6345636-8254-4f89-80e1-a19a7592af0e" />


---

# 6/26/2026 3 PM - remaining 5 sheets, ERC, 200 errors to clean

_Time spent: 9h_

knocked out Display, Cellular, Audio, and Controls sheets after the CM5 sheet was solid. cellular was the fastest since the EC25 uses USB 2.0 internally and almost all the PCIe pairs on the mini PCIe slot are no-connects.

realized partway through the display sheet that the 16-pin USB-C charging port can't carry USB 3.0 SuperSpeed pairs since those pins don't exist on a 16-pin connector. added a second USB-C port, a 24-pin connector, for mainly data and powered hubs. wired a two-transistor load switch for VBUS control on that port.

ran ERC after all six sheets and got around 200 errors. almost all of them were hierarchical label mismatches between sheets (came back to bite me) I had used hierarchical labels in most places, but they need matching port symbols on the parent sheet to connect properly. The fix I did converting everything to global labels, which just connect by name across all sheets automatically. wrote a simple Python script to do the find-and-replace directly in the .kicad_sch files since doing 40+ labels by hand would have taken wayyy too much time. ERC went from 200 errors to clean after running it again.
<img width="1239" height="880" alt="image" src="https://github.com/user-attachments/assets/cbb14fb8-b590-44c8-9609-fe44fae40751" />
<img width="1253" height="876" alt="image" src="https://github.com/user-attachments/assets/c2be8890-ddc8-457f-adad-514913a78c86" />
<img width="1234" height="862" alt="image" src="https://github.com/user-attachments/assets/03f7b9ce-034e-4c44-b377-df8a499b0db5" />
<img width="1227" height="855" alt="image" src="https://github.com/user-attachments/assets/721f915e-9140-4bc3-b59d-61a6c49ce568" />



---

# 6/27/2026 9 AM - PCB setup and component placement

_Time spent: 5h_

Started PCB layout. board outline is going to be 88 by 155mm. stackup is JLC04161H-3313 (F.Cu for Signal, In1.Cu for power, In2.Cu also for power, and B.cu for backup signal) , 4-layer: F.Cu for signals, In1.Cu solid GND plane, In2.Cu power planes, B.Cu for overflow signals with a GND pour. set up design rules and net classes -- MIPI DSI differential pairs get 0.1mm trace and 0.1mm gap for 90 ohm impedance on the outer layer.

Placement strategy was fixed connectors first since those can't move. Display FPC ZIF at the top center (changed later), two USB-C ports at the bottom(also changed to match a Nintendo Switch more), mini PCIe slot and SIM socket on the right edge, tactile buttons also on the right edge so they'll be accessible when the board is inside the enclosure. CM5 connectors go upper center(changed to bottom center) since the module covers most of the top half of the board. Power ICs clustered near the charging port. LDOs placed between the CM5 connectors and the FPC connector since they power the display directly, and to keep those traces short .

Took a few placement iterations to get everything to fit without components overlapping keepout areas around the connectors.
<img width="819" height="106" alt="image" src="https://github.com/user-attachments/assets/b591d0c6-bdae-47b6-a0b0-3a8bc6b70827" />

---

# 6/27/2026 2 PM - MIPI DSI routing, lane polarity inversion

_Time spent: 7h_

MIPI DSI routing was the hardest part of the whole layout. The CM5 J2 connector and the display FPC connector are on opposite sides of the board but not directly across from each other the FPC is top center, and J2 is offset. Getting all five differential pairs (CLK + 4 data lanes) routed cleanly on F.Cu without crossing vias into the GND plane was not possible with this placement (it will be fine for a first version though and I was on a time crunch).

Ended up routing some pairs through B.Cu. Normally you avoid vias on high-speed differential pairs, but the BCM2712 datasheet says it supports lane polarity inversion in device tree, which means if a pair ends up physically swapped at the CM5 connector you can just flip the bit in software and it works fine. the D2 pair ended up inverted at the CM5 side. will add `lane-polarities = <0 0 0 1 0>` to the device tree overlay to correct it. USB 3.0 RX pair also ended up inverted at the CM5 side from the same routing constraint, needs a matching DTS fix.

Measured all five DSI pairs after routing -- all within 5mm of each other in total length. MIPI DSI spec allows up to about 10mm skew at this data rate so no length tuning needed, just verify with a ruler in KiCad. (can definitely work on my PCB tracing LOL)
<img width="1591" height="605" alt="image" src="https://github.com/user-attachments/assets/82a5726e-a1f5-4ced-affb-ee80809bfe32" />
<img width="1271" height="912" alt="image" src="https://github.com/user-attachments/assets/60721aec-5e0a-4804-bf88-ed212f8ea2de" />


---

# 6/27/2026 9 PM - finishing routing, BOM tool issues, order prep

_Time spent: 4h_

finished routing all non-critical traces and poured GND. ran DRC and it came back clean other than a few silkscreen overlap warnings that don't affect assembly.

went through the JLCPCB BOM tool to match components. found a couple of issues: it matched a pull-up resistor to a through-hole 1/4W package instead of 0402, which would have been left unassembled without catching it. the inductors L1 and L2 had no automatic match and needed manual LCSC number entry. (I realized I could just use the production files instead of going over it like this)

the CM5 combined footprint also shows as a single component in the BOM tool, but it physically represents two DF40 connectors that have to land at a very specific 5mm center-to-center spacing to match the CM5 module. left a note in the JLCPCB order comments for the engineer explaining this so they don't try to substitute with separately placed connectors. 



---

# 6/28/2026 - DXQ cable drama, aluminum plate, and wrapping up

_Time spent: 4h_

The FPC cable is the last unresolved problem. The display has a 0.3mm pitch 39 pin connector, and the carrier board has a 0.5mm pitch 40 pin ZIF. Those do not connect directly. DXQ quoted custom cables but also mentioned a $0.79 adapter from Taobao. The problem is that the adapter is only 31 pins, and the display needs all 39. pins 32 through 38 are the touch controller I2C, reset, and interrupt lines. a 31-pin cable leaves the touch completely disconnected. Sent a follow-up asking how that would work. display itself is $56 regardless of how the cable gets resolved.

figured out the physical stack. aluminum plate on the bottom, thermal pad on top of that, PCB, battery, display. the thermal pad covers the full back face of the board so the aluminum cannot short anything even if it contacts a pad (the aluminum is also anodized to prevent that). CM5 heat goes through thermal vias to the pad to the plate. anodized black finish adds another layer of insulation.
<img width="1148" height="553" alt="image" src="https://github.com/user-attachments/assets/28b8355a-620a-4aec-a0e3-8c2553f38567" />
<img width="1471" height="381" alt="image" src="https://github.com/user-attachments/assets/8dbcfb93-6fb9-47c4-bb9f-ee549524e314" />
<img width="1550" height="629" alt="Screenshot 2026-06-29 010633" src="https://github.com/user-attachments/assets/7d219cc4-d358-4623-8091-1e060716909e" />


---

# 6/29/2026 - exact cost quotes locked in, BOM finalized

_Time spent: 5h_

Got exact pricing for everything instead of rough estimates. JLCPCB cart comes to $225.86, CNC plate $24, EC25 from Mouser $94.92, Amazon cart $288, display $56. cable is not finalized, but $10 is a safe bet. Grand total estimate is $700.28. 

built a full itemized BOM CSV

got the GitHub repo set up and pushed. 

# 6/30/2026 - Figured out display connector

_Time spent: 2h_

Did some more research on the display connector and found a 39-pin 0.3 mm to 0.5mm pitch connector! Literally perfect and exactly what I needed. I don't need to use any weird adapters or pay for DXQ to make custom cables! I reached out to the manufacturer to ask for a longer cable and if they could review the datasheets and make sure that it would be compatible too. Everything is now figured out and I am ready to assemble as soon as the parts arrive! 
<img width="1512" height="938" alt="Screenshot 2026-06-30 095629" src="https://github.com/user-attachments/assets/6f8594e0-4b09-48bd-a0c9-618b58a00f3f" />


Some BOM stuff:
<img width="1397" height="882" alt="Screenshot 2026-06-29 102104" src="https://github.com/user-attachments/assets/834d9945-3170-4864-8003-e250d4bab683" />
<img width="386" height="413" alt="Screenshot 2026-06-29 122206" src="https://github.com/user-attachments/assets/71ec69b3-4cef-4b7f-9ff6-a03fe9bb6fd0" />
<img width="398" height="815" alt="image" src="https://github.com/user-attachments/assets/186161cc-05f4-48b8-993f-11b9b6d7eb2e" />
