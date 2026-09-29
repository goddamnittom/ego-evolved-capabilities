#!/usr/bin/env bash
set -eu
cd "$(git rev-parse --show-toplevel)"

mkdir -p cognitive adversarial hardening memory engines

move_into() {
  dest="$1"; shift
  for d in "$@"; do
    if [ -d "$d" ]; then
      git mv "$d" "$dest/" 2>/dev/null || mv "$d" "$dest/"
    fi
  done
}

move_into cognitive \
  cognitive_coherence_auditor cognitive_entropy_monitor cognitive_feedback_loop \
  cognitive_friction_reducer cognitive_health_monitor cognitive_infrastructure_monitor \
  cognitive_load_balancer cognitive_orchestrator cognitive_performance_tracker \
  cognitive_resource_governor cognitive_schema_exporter cognitive_state_versioning \
  cognitive_template_synthesizer \
  axiom_interaction_graph axiom_stress_tester axiomatic_synthesizer \
  cross_domain_analogical_mapper decision_weighting_engine dialectic_consensus_engine \
  fidelity_driven_execution_router heuristic_synthesis_engine horizon_scanning_protocol \
  inertia_breaking_protocol intent_drift_analyzer kinematic_translation_layer \
  meta_pattern_synthesizer positive_reinforcement_loop real_time_implication_synthesizer \
  research_synthesizer semantic_entropy_monitor sota_semantic_analyzer \
  strategic_alignment_matrix strategic_chaos_simulator strategic_drift_monitor \
  strategic_heuristic_auditor strategic_intelligence_dashboard strategic_synergy_synthesizer \
  symmetric_synthesis_bridge synthetic_divergence_engine tactical_alignment_mirror \
  tactical_execution_blueprint trend_to_proposal_synthesizer truth_weighting_engine \
  user_bandwidth_optimizer proposal_generator fsve_framework sope t3_complexity_model \
  simulation_reality_delta_auditor predictive_signal_synthesizer dual_manifold_mapping \
  predictive_outcome_simulator social_logistical_synthesizer

move_into adversarial \
  active_counter_move_monitor actor_behavioral_profiling adversarial_learning_loop \
  adversarial_path_simulator adversarial_validation_layer ambient_signal_synthesizer \
  attack_intensity_monitor attack_surface_delta_mapper autonomous_redteam_synthesizer \
  behavioral_anomaly_detector blast_radius_mapper blast_radius_visualizer bleed_rate_monitor \
  collateral_damage_estimator cross_identity_trust_graph cross_platform_fingerprinter \
  deception_asset_orchestrator digital_footprint_mapper dynamic_risk_engine \
  evidence_collector evidence_correlator evidence_verification_engine \
  leakage_simulation_engine mission_temporal_forensics osint_username_tool \
  perimeter_watchdog persistence_audit_engine sentinel_delta_analyzer \
  session_integrity_auditor signal_collector signal_correlation_engine \
  smoking_gun_hunter threat_model_synthesizer threat_timeline_generator \
  trust_outcome_correlation_auditor verification_tiering_system \
  volatility_adjusted_trust_scale animate_smoke

move_into hardening \
  hardening_audit_intelligence hardening_bypass_simulator hardening_manifest_manager \
  hardening_sequence_orchestrator hardening_signal_synthesizer hardening_validation_matrix \
  incident_response_framework crisis_interface_generator recovery_roadmap_generator \
  remediation_state_guardrail security_baseline_attestor security_monitor \
  security_remediation_tracker oerg_manager rsg_manager pmr_engine stability_watchdog

move_into memory \
  dreaming_memory_daemon hyper_memory temporal_knowledge_graph moa_memory_simulator

move_into engines \
  antigravity antigravity_orchestrator async_deployment_pipeline autonomous_coder_daemon \
  autonomous_coder_daemon_codex discord_bridge ingest_all_sms integrate_codex_daemon \
  ioai_cognitive_bridge ioai_protocol ioai_protocol_update ioai_system_tester \
  ioai_task_coordination life_state_orchestrator maop_framework micro_mission_orchestrator \
  mission_control_telemetry mission_initiator mission_t2_mapping mission_t3_simulation \
  moa_attention moa_benchmark moa_benchmark_fast moa_hf_llama_patch moa_pos_integration \
  moa_t3_simulation moa_t4_extreme_pos moa_triton_kernel_alpha personal_lifecycle_orchestrator \
  pilot_high_roi_mission test_agentic_orchestration trending_repos \
  user_strategic_manifest_orchestrator visual_signature_manager

# leftover dirs that are still capability modules
for d in */; do
  name="${d%/}"
  case "$name" in
    cognitive|adversarial|hardening|memory|engines|scripts|.github) continue ;;
  esac
  if [ -d "$name" ]; then
    git mv "$name" cognitive/ 2>/dev/null || mv "$name" cognitive/
  fi
done

# root markdown that is not the project README
for f in mission_t1_analysis.md physical_action_layer_proposal.md prismatic_recursion.md; do
  if [ -f "$f" ]; then
    mkdir -p docs
    git mv "$f" docs/ 2>/dev/null || mv "$f" docs/
  fi
done
