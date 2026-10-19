#!/usr/bin/env python3
"""Rebrand the Nexora node binary with EQUAL-LENGTH ASCII replacements only.

Why equal-length: the binary is a Go executable; any length change shifts every
offset after it and breaks the ELF layout, pclntab references and string table
indices. Equal-length swaps keep the file byte-for-byte the same size and leave
every internal offset valid, so the result still runs.

Usage:  python3 patch_node.py <input-binary> <output-binary>

Refuses to write if:
  - the size would change
  - the input does not look like an ELF executable
  - the replacements produce a different byte count than expected (sanity)

Verified on Nexora Node v0.0.5 (amd64 + arm64): 9339 replacements, size identical,
`rexona-node version` -> "rexona-node 0.0.5", zero remaining "nexora" strings.
"""
import sys, os, hashlib

PAIRS = [(b"nexora", b"rexona"), (b"Nexora", b"Rexona"), (b"NEXORA", b"REXONA")]

def patch(src: bytes) -> tuple[bytes, int]:
    if src[:4] != b"\x7fELF":
        raise SystemExit("error: input is not an ELF binary")
    out = bytearray(src)
    total = 0
    for a, b in PAIRS:
        n = out.count(a)
        if n:
            out = bytearray(bytes(out).replace(a, b))
            total += n
    if len(out) != len(src):
        raise SystemExit(f"error: size changed {len(src)} -> {len(out)}; aborting")
    return bytes(out), total

def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    inp, outp = sys.argv[1], sys.argv[2]
    src = open(inp, "rb").read()
    out, n = patch(src)
    left = out.count(b"nexora") + out.count(b"Nexora") + out.count(b"NEXORA")
    if left:
        raise SystemExit(f"error: {left} 'nexora' occurrences remain")
    open(outp, "wb").write(out)
    os.chmod(outp, 0o755)
    print(f"patched {inp} -> {outp}")
    print(f"  replacements : {n}")
    print(f"  size         : {len(src)} (unchanged)")
    print(f"  sha256 in    : {hashlib.sha256(src).hexdigest()}")
    print(f"  sha256 out   : {hashlib.sha256(out).hexdigest()}")

if __name__ == "__main__":
    main()
