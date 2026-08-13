from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from cosmos_bio_cns.adapters.mock import DeterministicCardiacAdapter
from cosmos_bio_cns.persistence import SQLiteEventStore
from cosmos_bio_cns.runtime import BioCNSRuntime


def cmd_demo(args: argparse.Namespace) -> int:
    store = SQLiteEventStore(args.db)
    runtime = BioCNSRuntime([DeterministicCardiacAdapter()], store=store)
    runtime.start()
    try:
        for _ in range(args.steps):
            frame, state = runtime.step()
            print(json.dumps({"frame": asdict(frame), "state": asdict(state)}, indent=2))
    finally:
        runtime.stop()
        valid = store.verify()
        count = store.count()
        store.close()
    print(f"ledger_events={count} hash_chain_valid={valid}")
    return 0 if valid else 2


def cmd_verify(args: argparse.Namespace) -> int:
    if not Path(args.db).exists():
        print(f"missing database: {args.db}")
        return 2
    store = SQLiteEventStore(args.db)
    valid = store.verify()
    print(f"events={store.count()} head={store.head_hash()} valid={valid}")
    store.close()
    return 0 if valid else 1


def main() -> int:
    parser = argparse.ArgumentParser(prog="cosmos-bio-cns")
    sub = parser.add_subparsers(required=True)
    demo = sub.add_parser("demo", help="run deterministic local cardiac/CNS demo")
    demo.add_argument("--steps", type=int, default=5)
    demo.add_argument("--db", default="cosmos_bio_cns.sqlite3")
    demo.set_defaults(func=cmd_demo)
    verify = sub.add_parser("verify-ledger", help="verify append-only event hash chain")
    verify.add_argument("--db", default="cosmos_bio_cns.sqlite3")
    verify.set_defaults(func=cmd_verify)
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
