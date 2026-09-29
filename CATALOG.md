# ego-evolved-capabilities

Catalog of https://github.com/goddamnittom/ego-evolved-capabilities  
Snapshot: 2026-09-29 (after pass 1 purge, pass 2 fold, pass 3 flatten).

Ego’s evolved autonomous capabilities: multi-agent orchestration, symbolic-style checks, memory synthesis, adversarial and hardening tooling. Most modules are standalone Python files with a class or a few functions. Many assume sandbox paths like `/root/`.

## Layout

```
engines/       IOAI, MoA, coder daemons, orchestrators, bridges
cognitive/     monitors, synthesizers, strategy / tactics
adversarial/   red team, evidence, threat, OSINT
hardening/     hardening, IR, security trackers
memory/        dreaming / hyper memory, temporal graph
docs/          mission notes and proposals
scripts/       one-shot trim scripts (pass 1–3)
README.md
ego_evolution_report.md
CATALOG.md     this file
```

Import example:

```python
from engines.ioai_protocol import IoAIAgent
from cognitive.cognitive_entropy_monitor import CognitiveEntropyMonitor
from cognitive.semantic_entropy_monitor import SemanticEntropyMonitor
```

## Root docs

| File | Role |
| --- | --- |
| `README.md` | Short layout + import paths |
| `ego_evolution_report.md` | 2026-05-20 audit: RMCA, IAPS, ACST, strengths/weaknesses |
| `CATALOG.md` | Full module map |

## engines/

Runtime and product engines.

| Module | Notes |
| --- | --- |
| `ioai_protocol.py` | Core IoAI agent + security errors |
| `ioai_protocol_update.py` | Protocol revisions |
| `ioai_task_coordination.py` | Multi-agent task board |
| `ioai_cognitive_bridge.py` | Bridge into cognitive layer |
| `ioai_system_tester.py` | IoAI integration tests |
| `moa_attention.py` | Mixture-of-attention |
| `moa_benchmark.py` / `moa_benchmark_fast.py` | Attention benchmarks |
| `moa_hf_llama_patch.py` | Hugging Face LLaMA attention patch |
| `moa_pos_integration.py` | Position / RoPE-style integration |
| `moa_t3_simulation.py` / `moa_t4_extreme_pos.py` | Scaled MoA sims |
| `moa_triton_kernel_alpha.py` | Triton kernel experiment |
| `autonomous_coder_daemon.py` | Background coder loop |
| `autonomous_coder_daemon_codex.py` | Codex-oriented coder daemon |
| `integrate_codex_daemon.py` | Wire-up helper |
| `antigravity.py` / `antigravity_orchestrator.py` | Antigravity agent / orchestrator |
| `maop_framework.py` | Multi-agent orchestration (roles, task board) |
| `personal_lifecycle_orchestrator.py` | Largest orchestrator (~520 LOC) |
| `life_state_orchestrator.py` | Life-state machine |
| `micro_mission_orchestrator.py` | Small mission runner |
| `user_strategic_manifest_orchestrator.py` | Manifest-driven goals |
| `mission_initiator.py` / `mission_control_telemetry.py` | Mission start + telemetry |
| `mission_t2_mapping.py` / `mission_t3_simulation.py` | Mission stages |
| `pilot_high_roi_mission.py` | High-ROI pilot |
| `async_deployment_pipeline.py` | Async deploy |
| `discord_bridge.py` | Discord I/O |
| `ingest_all_sms.py` | SMS ingest |
| `trending_repos.py` | GitHub trend fetch |
| `test_agentic_orchestration.py` | Orchestration smoke test |
| `visual_signature_manager.py` | Brand / visual assets |

## cognitive/

World-model health, planning mode, synthesis.

**Entropy / health**

| Module | Role |
| --- | --- |
| `cognitive_entropy_monitor.py` | Predicted vs observed signal miss-rate; silent-pivot / model-decay flag |
| `semantic_entropy_monitor.py` | Shannon entropy over hypothesis weights → explore vs exploit |
| `cognitive_health_monitor.py` | Aggregate health |
| `cognitive_coherence_auditor.py` | Internal consistency |
| `cognitive_infrastructure_monitor.py` | Infra / runtime health |
| `cognitive_performance_tracker.py` | Performance metrics |
| `cognitive_load_balancer.py` | Load split across cognitive work |
| `cognitive_resource_governor.py` | Resource caps |
| `cognitive_friction_reducer.py` | Cut process friction |
| `intent_drift_analyzer.py` | Goal drift vs original intent |

**Orchestration / routing**

| Module | Role |
| --- | --- |
| `cognitive_orchestrator.py` | Cognitive task routing |
| `cognitive_feedback_loop.py` | Feedback into next cycle |
| `fidelity_driven_execution_router.py` | Route by fidelity / confidence |
| `decision_weighting_engine.py` | Weight options |
| `truth_weighting_engine.py` | Weight claims |
| `dialectic_consensus_engine.py` | Argue / converge |
| `positive_reinforcement_loop.py` | Reinforce successful paths |
| `inertia_breaking_protocol.py` | Break stuck plans |
| `user_bandwidth_optimizer.py` | Limit user-facing load |

**Synthesis / strategy**

| Module | Role |
| --- | --- |
| `axiomatic_synthesizer.py` / `axiom_interaction_graph.py` / `axiom_stress_tester.py` | Axiom graph + stress |
| `heuristic_synthesis_engine.py` | Heuristic build |
| `meta_pattern_synthesizer.py` | Cross-pattern synthesis |
| `cognitive_template_synthesizer.py` | Template generation |
| `cross_domain_analogical_mapper.py` | Analogy map |
| `predictive_outcome_simulator.py` / `predictive_signal_synthesizer.py` | Forecast outcomes / signals |
| `synthetic_divergence_engine.py` | Generate divergent futures |
| `simulation_reality_delta_auditor.py` | Sim vs reality gap |
| `dual_manifold_mapping.py` | Dual-space mapping |
| `horizon_scanning_protocol.py` | Far-horizon scan |
| `proposal_generator.py` / `trend_to_proposal_synthesizer.py` / `research_synthesizer.py` | Research → proposals |
| `sota_semantic_analyzer.py` | SOTA scan |
| `real_time_implication_synthesizer.py` | Live implications |
| `strategic_*` / `tactical_*` | Alignment, drift, chaos, synergy, blueprints |
| `fsve_framework.py` / `sope.py` / `t3_complexity_model.py` | Named cognitive frameworks |
| `cognitive_schema_exporter.py` / `cognitive_state_versioning.py` | Export / version state |
| `kinematic_translation_layer.py` | Map abstract intent to motion-like steps |
| `social_logistical_synthesizer.py` | Social / logistics synthesis |

### Cognitive entropy (detail)

`CognitiveEntropyMonitor` is **not** Shannon entropy. It scores how many expected markers failed to appear:

```
divergence = 1 - (predicted ∩ observed) / predicted
```

- `< 0.3` LOW · `< 0.7` ELEVATED · else HIGH
- `> 0.7` CRITICAL, else STABLE
- Logs last 100 reports to `/root/entropy_logs.json`

`SemanticEntropyMonitor` **is** Shannon entropy `H = -sum p log2 p` over hypothesis probabilities. High H → EXPLORATION; low H → EXPLOITATION.

## adversarial/

| Cluster | Modules |
| --- | --- |
| Red team / paths | `adversarial_learning_loop`, `adversarial_path_simulator`, `adversarial_validation_layer`, `autonomous_redteam_synthesizer`, `active_counter_move_monitor` |
| Attack surface | `attack_intensity_monitor`, `attack_surface_delta_mapper`, `blast_radius_mapper`, `blast_radius_visualizer`, `bleed_rate_monitor`, `collateral_damage_estimator`, `leakage_simulation_engine` |
| Behavior / identity | `actor_behavioral_profiling`, `behavioral_anomaly_detector`, `cross_identity_trust_graph`, `cross_platform_fingerprinter`, `digital_footprint_mapper`, `osint_username_tool` |
| Deception / signals | `deception_asset_orchestrator`, `ambient_signal_synthesizer`, `signal_collector`, `signal_correlation_engine`, `animate_smoke` |
| Evidence | `evidence_collector`, `evidence_correlator`, `evidence_verification_engine`, `smoking_gun_hunter`, `mission_temporal_forensics`, `verification_tiering_system` |
| Trust / risk | `dynamic_risk_engine`, `trust_outcome_correlation_auditor`, `volatility_adjusted_trust_scale` |
| Perimeter | `perimeter_watchdog`, `persistence_audit_engine`, `session_integrity_auditor`, `sentinel_delta_analyzer` |
| Threat products | `threat_model_synthesizer`, `threat_timeline_generator` |

## hardening/

- Hardening cycle: `hardening_audit_intelligence`, `hardening_bypass_simulator`, `hardening_manifest_manager`, `hardening_sequence_orchestrator`, `hardening_signal_synthesizer`, `hardening_validation_matrix`
- IR / recovery: `incident_response_framework`, `crisis_interface_generator`, `recovery_roadmap_generator`, `remediation_state_guardrail`
- Security ops: `security_baseline_attestor`, `security_monitor`, `security_remediation_tracker`, `stability_watchdog`
- Managers: `oerg_manager`, `rsg_manager`, `pmr_engine`

## memory/

- `dreaming_memory_daemon.py` — offline / dream consolidation
- `hyper_memory.py` — dense long-term store
- `temporal_knowledge_graph.py` — time-stamped graph
- `moa_memory_simulator.py` — MoA-side memory sim

## docs/

- `mission_t1_analysis.md`
- `physical_action_layer_proposal.md`
- `prismatic_recursion.md`

## scripts/

`pass1_purge.sh`, `pass2_fold.sh`, `pass3_flatten.sh` — already applied on `main`.

## Trim history

1. **Pass 1** — dropped generated per-module READMEs, stub modules, helpers, `algorithmic_philosophy.md`.
2. **Pass 2** — folded remaining dirs into `engines/`, `cognitive/`, `adversarial/`, `hardening/`, `memory/`, `docs/`.
3. **Pass 3** — flattened `pkg/name/name.py` → `pkg/name.py`.

## Caveats

- Modules are mostly independent; there is no single runtime that wires all of them.
- Several write under `/root/`.
- Names overclaim vs implementation (cognitive entropy monitor is a miss-rate).
