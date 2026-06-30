

---

# 6/22/2026 4 PM - all the component searching

_Time spent: 5h_

went through JLCPCB part by part. EC21 variants on JLCPCB are useless for North America, wrong bands and basically no stock. I went to Mouser and found the EC25AFXGA-MINIPCIE which is certified for AT&T and T-Mobile. But its mini PCIe form factor meaning it plugs in instead than being soldered. 

caught a mistake. I had the SGM2036-2.8V LDO in the cart for the display VCI rail but the datasheet says VCI is 3.3V not 2.8V. also found the INMP441 mic on JLCPCB is overpriced and out of stock so decided on a 5-pack on Amazon for $11.99. they have through hole pins so the module just plugs into a header on the board instead of being SMD soldered.

---

# 6/22/2026 6 PM - display research rabbit hole

_Time spent: 4h_

needed to figure out the display. found the piBrick project, released June 1st, fully open source. it is a handheld CM5 computer using a DXQ AMOLED display connected over MIPI DSI. 

their display is 3.92 inches, which was too small. found the DXQ7D0023 in the catalog, 7 inch, 1080x1920, 165Hz, capacitave touch. listed at $96 publicly. emailed DXQ directly for sample pricing and the datasheet. the 7 inch size is similar to a iPhone 17 Pro Max but narrower than a Switch, fits in pockets, and the screen size makes the terminal actually usable and the demo visible.

during the research I asked gemini about the display driver IC and it confidently told me it was the SH8804B from Sino Wealth with no Linux support and that I would need an HDMI bridge chip. I was starting to plan a whole alternate path around that. DXQ then sent the actual datasheet and the driver is the ICNA3512,  and they gave me an init sequence that lets me write a device tree overlay without recompiling the kernel. Dont trust AI for everything LOL.

---

# 6/22/2026 11 PM - parts locked in, DXQ responded

_Time spent: 2h_

DXQ sent back the full DXQ7D0023 spec sheet and the ICNA3512 driver datasheet. timing parameters are all in there. 60Hz: HFP=156, HBP=23, VFP=20, VBP=15. same level of detail for every other refresh rate. 

the FPC connector is still a problem. the display has a 0.3mm pitch 39 pin connector and JLCPCB does not stock 0.3mm ZIF connectors at all.

---

# 6/23/2026 - DXQ sent the full driver package, display is completely solved

_Time spent: 6h_

emailed DXQ asking for the init code and driver files. they sent back a full zip with a DSC folder, a non-DSC folder, and a FocalTech touch driver. the main file is a full Qualcomm MDSS panel driver with complete init sequences for all five refresh rates: 60, 90, 120, 144, and 165Hz. the touch driver is complete GPL v2 Linux kernel source for the FT3519T.

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

---


# 6/26/2026 - schematic marathon, all 6 sheets done

_Time spent: 14h_

Started on the CM5 sheet and had to verify every single pin from scratch. the pin numbers from the previous session were wrong almost across the board. 5V inputs were listed as pins 1-4, but those are Ethernet and GND. The real 5V inputs are pins 77, 79, 81, 83, 85, 87. USB DM and DP were on the wrong connector entirely. went through the full CM5 datasheet line by line.

caught two design errors while doing this. the LDO enable pins were tied to +3V3 which is a  problem since the LDO cannot turn itself on. changed both to +5V from the boost converter, which is available first. also found the CM5 has a dedicated PWR_Button pin (pin 92) that handles power on and off without needing a GPIO at all, just wires straight to a button and ground.

added a second USB-C port for data after realizing the 16 pin charging port physically cannot carry USB 3.0 because it does not have the SuperSpeed pairs. added a 24 pin connector with a two-transistor load switch for VBUS control. finished all six sheets including cellular, audio, and controls. the cellular sheet was fast since most of the PCIe pairs on the mini PCIe slot are NC because the EC25 uses USB 2.0 internally.

---

# 6/27/2026 - PCB layout, routing

_Time spent: 16h_

Started PCB layout. board is 88 by 155mm, 4-layer JLC04161H-3313 stackup. set up design rules and net classes with MIPI DSI differential pair settings at 0.1mm trace and 0.1mm gap for 90 ohm impedance on the outer layer.

placement took most of the morning. 

The MIPI DSI routing was the hardest part. the CM5 J2 connector and the FPC connector are not directly across from each other and getting all differential pairs routed cleanly without vias was not possible with this placement. Ended up routing some pairs through the back copper, which is fine because the BCM2712 supports lane polarity inversion in device tree. D2 pair ended up inverted; will fix in the DTS. All five DSI pairs ended up within 5mm of each other in total length, which is within tolerance. USB 3.0 RX pair was also inverted at the CM5 side and needs a matching DTS fix.

---

# 6/28/2026 - DXQ cable drama, aluminum plate, and wrapping up

_Time spent: 4h_

The FPC cable is the last unresolved problem. The display has a 0.3mm pitch 39 pin connector and the carrier board has a 0.5mm pitch 40 pin ZIF. those do not connect directly. DXQ quoted custom cables but also mentioned a $0.79 adapter from Taobao. the problem is that adapter is only 31 pins and the display needs all 39. pins 32 through 38 are the touch controller I2C, reset, and interrupt lines. a 31-pin cable leaves the touch completely disconnected. sent a follow up asking how that would work. display itself is $56 regardless of how the cable gets resolved.

figured out the physical stack. aluminum plate on the bottom, thermal pad on top of that, PCB, battery, display. the thermal pad covers the full back face of the board so the aluminum cannot short anything even if it contacts a pad (the aluminum is also anodized to prevent that). CM5 heat goes through thermal vias to the pad to the plate. anodized black finish adds another layer of insulation.


---

# 6/29/2026 - exact cost quotes locked in, BOM finalized

_Time spent: 5h_

Got exact pricing for everything instead of rough estimates. JLCPCB cart comes to $225.86, CNC plate $24, EC25 from Mouser $94.92, Amazon cart $288, display $56. cable is not finalized, but $10 is a safe bet. Grand total estimate is $700.28. 

built a full itemized BOM CSV

got the GitHub repo set up and pushed. 

next step is hearing back on X tier, then placing every order at once. 
