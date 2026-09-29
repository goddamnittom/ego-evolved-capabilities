#!/usr/bin/env python3
"""CLI bridge so Antigravity (`agy`) can call Ego modules as tools."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def cmd_entropy(args: argparse.Namespace) -> int:
    from cognitive.cognitive_entropy_monitor import CognitiveEntropyMonitor

    predicted = [s.strip() for s in args.predicted.split(",") if s.strip()]
    observed = [s.strip() for s in args.observed.split(",") if s.strip()]
    mon = CognitiveEntropyMonitor(threshold=args.threshold)
    mon.logs_path = args.log
    print(json.dumps(mon.audit_perimeter(predicted, observed), indent=2))
    return 0


def cmd_semantic(args: argparse.Namespace) -> int:
    from cognitive.semantic_entropy_monitor import SemanticEntropyMonitor

    probs = [float(x) for x in args.probs.split(",") if x.strip()]
    mon = SemanticEntropyMonitor(entropy_threshold=args.threshold)
    print(json.dumps(mon.evaluate_mode(probs), indent=2))
    return 0


def cmd_gravity(_args: argparse.Namespace) -> int:
    from engines.antigravity import AntigravityEngine

    engine = AntigravityEngine()
    engine.load_context("")
    engine.audit_gravity()
    engine.synthesize_antigravity_paths()
    print(json.dumps(engine.generate_report(), indent=2))
    return 0


def cmd_phase(args: argparse.Namespace) -> int:
    from engines.antigravity_orchestrator import AntigravityOrchestrator

    orch = AntigravityOrchestrator()
    orch.state_file = args.state
    orch.load_state()
    print(orch.trigger_phase(args.phase))
    print(json.dumps(orch.state, indent=2))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="agy_bridge", description="Ego modules for Antigravity CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("entropy", help="predicted vs observed miss-rate")
    e.add_argument("--predicted", required=True, help="comma-separated expected signals")
    e.add_argument("--observed", required=True, help="comma-separated actual signals")
    e.add_argument("--threshold", type=float, default=0.7)
    e.add_argument("--log", default=str(ROOT / "logs" / "entropy_logs.json"))
    e.set_defaults(func=cmd_entropy)

    s = sub.add_parser("semantic", help="Shannon entropy explore/exploit")
    s.add_argument("--probs", required=True, help="comma-separated probabilities")
    s.add_argument("--threshold", type=float, default=0.5)
    s.set_defaults(func=cmd_semantic)

    g = sub.add_parser("gravity", help="AntigravityEngine capability audit")
    g.set_defaults(func=cmd_gravity)

    ph = sub.add_parser("phase", help="advance AntigravityOrchestrator phase")
    ph.add_argument("--phase", type=int, required=True)
    ph.add_argument("--state", default=str(ROOT / "logs" / "evolution_state.json"))
    ph.set_defaults(func=cmd_phase)

    args = p.parse_args()
    Path(getattr(args, "log", ROOT / "logs" / ".keep")).parent.mkdir(parents=True, exist_ok=True)
    Path(getattr(args, "state", ROOT / "logs" / ".keep")).parent.mkdir(parents=True, exist_ok=True)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
