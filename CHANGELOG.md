# Changelog

All notable changes to Meta-Agent-Protocol (MAP) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.1] — 2026-06-17

### Added

- **INTEGRATION.md**: Universal host repo integration guide — covers both Greenfield (new repo) and Migration (from embedded conventions) paths, with complete {{PLACEHOLDER}} reference table, Makefile template, verification checklist, and daily operations

### Fixed

- **scripts/setup_map.sh**: Correct HOST_ROOT path — use `MAP_ROOT/..` (one level up) instead of `../..` (two levels up). MAP is installed at `conventions/` directly under repo root.
- **scripts/heartbeat.sh**: Same HOST_ROOT path fix

---

## [1.0.0] — 2026-06-16

### Added — Initial Scaffold

- **THE_CODEX.md**: 9 universal laws for AI Agent behavior — Persona Shifting, TDD Gate, No-Go Zones, Cross-System Change Declaration, SLAIB Git Flow, Global Test Orchestration, Cascading Conventions, API-First Prompting, Micro-loop Metronome
- **rules/arch-rules.md**: Architecture-level anti-pollution red lines + Contract-First Development methodology (3-layer contract model)
- **rules/agent-loop.md**: Dual-engine (Claude Code + Aider) collaboration specification — role separation, task file format, standard execution loop, task granularity levels
- **templates/**: 3 parameterized templates (AI_RULES.md, aider.conf.yml, importlinter.ini) with `{{PLACEHOLDER}}` markers for host repo customization
- **scripts/setup_map.sh**: Bootstrap script — auto-detects git submodule, generates AI_RULES.md + .aider.conf.yml + .importlinter from templates, provides post-setup instructions
- **scripts/heartbeat.sh**: Loop Engineering heartbeat — periodic git status check + test suite execution, designed for cron/systemd integration
- **sub-project-conventions/**: 6 reference CONVENTIONS.md templates (SROS, ARC-Engine, GraphMRI-Lite, Hermes-Workflows, AgenticOps, SXMU_MDD_Twin)
- **LICENSE**: MIT
- **README.md**: Project homepage with quick start, directory structure, core concept diagrams
