#!/usr/bin/env python3
"""Emit deterministic canary PII personas for an ObservePoint PII-leak engagement.

Usage: python3 canary_persona.py <flows> <base_inbox_address> [--seed N] [--email-mode subaddress|shared]
  flows              comma-separated flow slugs, e.g. checkout,signup,quote
  base_inbox_address the account's single PII-CANARY inbox address (local@domain)
  --seed N           integer; same seed+inputs -> identical output (default 0)
  --email-mode       subaddress (base+flow@) or shared (all flows use base). Default set from the
                     inbox sub-addressing verification (see the design spec section 4).

Emits JSON to stdout. PURE: no network/filesystem/random/time. Advisory only — the operator
provisions ONE inbox (reuse-or-create) and builds the journeys; this only emits the values to use.
"""
import argparse
import json
import sys

# Rare-but-plausible full names — distinctive enough to be unique canaries yet pass form/fraud
# validation. Deterministically indexed; extend if an engagement needs more flows than this list.
NAMES = [
    "Sylvester Ashcombe", "Marisol Trewick", "Cornelius Fennimore", "Odalys Brightwater",
    "Thaddeus Kellsworth", "Ingrid Vasquez-Roe", "Lucian Marchetti", "Philippa Nkemdirim",
    "Ezekiel Dornbusch", "Saoirse Kavanagh", "Bartholomew Ozanne", "Wilhelmina Fairbanks",
    "Federico Santangelo", "Anneliese Vandermeer", "Dashiell Thornbury", "Rosalind Achterberg",
    "Ignatius Prendergast", "Clementine Aldous", "Leopold Winterbourne", "Marguerite Ellery",
    "Casimir Dubois-Lang", "Petronella Haywood", "Augustin Belrose", "Delphine Cartwright",
]
STREETS = ["Kestrel Hollow Rd", "Marlowe Vale", "Ptarmigan Way", "Alderwick Terrace",
           "Sable Creek Ln", "Hawthorne Reach", "Bellamy Court", "Wexford Rise"]

def parse_base(addr):
    if "@" not in addr or addr.startswith("@") or addr.endswith("@"):
        raise ValueError(f"base_inbox_address must be local@domain, got: {addr!r}")
    local, domain = addr.split("@", 1)
    return local, domain

def build_persona(flow, index, seed, base_local, base_domain, mode):
    pick = (index + seed) % len(NAMES)
    name = NAMES[pick]
    # E.164 fictional: +1 (555-01xx block is reserved for fictional use). Line number varies by
    # index so digits are unique per flow; area code fixed at 202.
    phone = f"+1202555{100 + index:04d}"
    address = f"{1400 + index * 7} {STREETS[index % len(STREETS)]}, Cedar Junction, MT 59000"
    account_id = f"OPCANARY-{seed:03d}-{index:03d}"
    if mode == "shared":
        email = f"{base_local}@{base_domain}"
    else:
        email = f"{base_local}+{flow}@{base_domain}"
    return {"flow": flow, "name": name, "email": email, "phone": phone,
            "address": address, "accountId": account_id}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("flows")
    ap.add_argument("base_inbox_address")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--email-mode", choices=["subaddress", "shared"], default="shared")
    args = ap.parse_args()

    flows = [f.strip() for f in args.flows.split(",") if f.strip()]
    if not flows:
        print("no flows given", file=sys.stderr); sys.exit(2)
    if len(flows) > len(NAMES):
        print(f"too many flows ({len(flows)}); max {len(NAMES)} — extend NAMES or split the engagement",
              file=sys.stderr); sys.exit(1)
    try:
        base_local, base_domain = parse_base(args.base_inbox_address)
    except ValueError as e:
        print(str(e), file=sys.stderr); sys.exit(1)

    personas = [build_persona(f, i, args.seed, base_local, base_domain, args.email_mode)
                for i, f in enumerate(flows)]
    print(json.dumps({"baseInbox": args.base_inbox_address, "emailMode": args.email_mode,
                      "personas": personas}, indent=2))

if __name__ == "__main__":
    main()
