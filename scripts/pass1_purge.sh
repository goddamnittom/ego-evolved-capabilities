#!/usr/bin/env bash
# Finish pass 1 in one commit. Run from repo root.
set -euo pipefail

STUBS=(
  axiomatic_stress_simulator
  cognitive_convergence_engine
  cognitive_evidence_ledger
  cognitive_orchestration_engine
  cognitive_value_weighting_engine
  deep_scan_sota
  extract_key_sections
  fetch_readmes
  fractal_gen
  gateway_rni
  gemini_test
  get_sections
  get_trending
  ioc_evidence_hunter
  logic_stress_tester
  mct_telemetry_t3
  nuance_preservation_anchor
  parse_pdf
  pivot_prediction_engine
  predictive_adversary_simulation
  prepare_repo
  prescriptive_hardening_engine
  risk_surface_quantifier
  search_skills
  sota_analysis
  strategic_divergence_analyzer
  synthesis_engine
  threat_projection_engine
  unified_threat_landscape
  update_evolution
  urgency_engine
)

for d in "${STUBS[@]}"; do
  rm -rf "$d"
done

# generated per-module READMEs; keep root README.md
find . -mindepth 2 -type f -name README.md -delete

git add -A
git status --short | head
echo
echo "Review, then: git commit -m 'pass1: remove stubs and generated READMEs' && git push"
