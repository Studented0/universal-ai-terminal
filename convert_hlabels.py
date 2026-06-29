#!/usr/bin/env python3
"""
Convert all hierarchical_label to global_label in KiCad .kicad_sch files.
Run from the directory containing your .kicad_sch files.

Usage: python3 convert_hlabels.py
"""

import os
import re
import shutil

def convert_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Count how many we're converting
    count = content.count('(hierarchical_label')

    # Replace hierarchical_label with global_label
    # Also need to remove the (shape ...) field that H labels have
    # and the (sheet_name ...) (sheet_file ...) that sheet pins have
    
    # Step 1: Replace the label type
    content = content.replace('(hierarchical_label', '(global_label')

    # Step 2: H labels have a specific shape like (shape input) (shape output) etc.
    # Global labels use (shape input_output) or similar — but KiCad accepts
    # (shape input), (shape output), (shape bidirectional) for global labels too
    # No shape change needed — KiCad handles it

    if content != original:
        # Backup original
        shutil.copy2(filepath, filepath + '.bak')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Converted {count} hierarchical labels in: {os.path.basename(filepath)}")
        return count
    else:
        print(f"  No hierarchical labels found in: {os.path.basename(filepath)}")
        return 0

def main():
    # Find all .kicad_sch files in current directory and subdirectories
    sch_files = []
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.kicad_sch'):
                sch_files.append(os.path.join(root, f))

    if not sch_files:
        print("No .kicad_sch files found. Run from your project directory.")
        return

    print(f"Found {len(sch_files)} schematic file(s):\n")
    
    total = 0
    for filepath in sch_files:
        total += convert_file(filepath)

    print(f"\nDone. Converted {total} hierarchical labels total.")
    print("Backups saved as .kicad_sch.bak files.")
    print("\nNEXT STEPS in KiCad:")
    print("1. Close and reopen your project")
    print("2. Go to each sheet rectangle in root schematic")
    print("3. Right-click each sheet rectangle -> Edit -> remove any remaining sheet pins")
    print("4. Run ERC again")

if __name__ == '__main__':
    main()
