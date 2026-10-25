#!/usr/bin/env python3
import re

# Paste the raw decompilation block here
RAW_INPUT = """
  local_78[0] = 0x25;
  local_78[1] = 0x2b;
  local_78[2] = 0x20;
  local_78[3] = 0x26;
  local_78[4] = 0x3a;
  local_78[5] = 0x2d;
  local_78[6] = 0x2e;
  local_78[7] = 0x33;
  local_78[8] = 0x1e;
  local_78[9] = 0x33;
  local_78[10] = 0x27;
  local_78[0xb] = 0x20;
  local_78[0xc] = 0x33;
  local_78[0xd] = 0x1e;
  local_78[0xe] = 0x2a;
  local_78[0xf] = 0x28;
  local_78[0x10] = 0x2d;
  local_78[0x11] = 0x23;
  local_78[0x12] = 0x1e;
  local_78[0x13] = 0x2e;
  local_78[0x14] = 0x25;
  local_78[0x15] = 0x1e;
  local_78[0x16] = 0x24;
  local_78[0x17] = 0x2b;
  local_78[0x18] = 0x25;
  local_78[0x19] = 0x3c;
  local_78[0x1a] = 0xffffffbf;
"""

def solve_ghidra_array(c_code: str):
    # Regex specifically extracts the assigned hex values: local_78[...] = 0xXX;
    assigned_hex = re.findall(r'=\s*(0x[0-9a-fA-F]+);', c_code)
    
    bytes_list = []
    for h in assigned_hex:
        val = int(h, 16) & 0xFF
        bytes_list.append(val)

    print(f"[*] Parsed {len(bytes_list)} exact array bytes.\n")

    # Brute force Addition, XOR, and Subtraction
    for key in range(256):
        add_res = "".join([chr((b + key) & 0xFF) for b in bytes_list if ((b + key) & 0xFF) != 0])
        xor_res = "".join([chr((b ^ key) & 0xFF) for b in bytes_list if ((b ^ key) & 0xFF) != 0])
        
        if "flag{" in add_res.lower():
            print(f"[+] [ADD] Key 0x{key:02X} ({key}): {add_res}")
        if "flag{" in xor_res.lower():
            print(f"[+] [XOR] Key 0x{key:02X} ({key}): {xor_res}")

if __name__ == "__main__":
    solve_ghidra_array(RAW_INPUT)
