# Implementation Plan: J0 Reproducible QEMU Laboratory

**Branch**: `feat/j0-qemu-laboratory` | **Date**: 2026-09-28 | **Spec**: [spec.md](spec.md)

## Summary

Provide a verifiable Linux-host QEMU AArch64 lab without claiming a Timeless kernel exists. A locked version and scripted preflight/DTB dump will establish the machine and future boot boundary; a test matrix, ADR and measurement protocol capture J0 evidence and J1 obligations.

## Technical Context

**Language/Version**: Python 3.13.5 (host harness); guest language undecided

**Primary Dependencies**: QEMU system Arm 10.0.13, Debian package `1:10.0.13+ds-0+deb13u1`; Python standard library; no guest runtime

**Storage**: Text/JSON evidence and raw DTB, not guest storage

**Testing**: Python `unittest`, QEMU machine introspection, explicit missing-image failure

**Target Platform**: Linux amd64 host (initially Debian 13), QEMU `virt-10.0` AArch64 guest

**Project Type**: OS research and laboratory tooling

**Performance Goals**: No numeric performance target or baseline before a running guest and observed traces

**Constraints**: TCG, single `cortex-a53` vCPU, 256 MiB, serial, NIC disabled, no KVM requirement, no private data

**Scale/Scope**: One virtual machine, one boot contract, one requirements/test matrix; no kernel implementation in J0.

## Constitution Check

| Principle | Gate and design response |
|---|---|
| I. Responsiveness/stability | Only measurement protocol, no fabricated latency; QEMU evidence marked virtual-only. |
| II. Portable core | Contract separates architecture boot, machine DTB devices and common core; no QEMU code in future common source. |
| III. Originality | Host QEMU/Python are tools, not guest components; exceptions register created for future shipped dependencies. |
| IV. Evidence | Preflight/DTB evidence is not a kernel boot; tests and docs report exact exercised scope. |
| V. Hardware | No device purchase, flash, firmware change or real-phone claim. |
| VI. Spec Kit | Spec → clarification (assumptions sufficient) → plan → tasks → read-only analysis → implementation/evidence. |
| VII. Git/PR | Dedicated `feat/` branch, Conventional Commits, PR required to merge into `main`. |

**Pre-research gate:** pass. **Post-design gate:** pass; final CPU/system-language and real-device decisions remain deferred, so the `virt` choice is a reversible J0 lab target, not a universal OS architecture claim.

## Research and Design

- [research.md](research.md): QEMU machine/boot alternatives, tool policy and evidence boundary.
- [data-model.md](data-model.md): manifest, evidence run, test matrix and exception records.
- [contracts/laboratory.md](contracts/laboratory.md): preflight, DTB inspection, kernel-run behavior and exit status.
- [quickstart.md](quickstart.md): commands and expected J0 verification states.

## Project Structure

### Documentation (this feature)

```text
specs/001-qemu-laboratory/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/laboratory.md
├── quickstart.md
├── test-matrix.md
├── checklists/requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
config/toolchain.lock.json     # Exact J0 host tool versions and VM parameters
scripts/qemu_lab.py            # Preflight, inspect, run (image required for run)
tests/test_qemu_lab.py         # Contract and failure-mode tests
docs/adr/0001-qemu-j0-lab.md  # Reversible lab choice and deferred OS decisions
docs/measurement.md            # Baseline protocol, not a measured baseline
```

**Structure Decision:** J0 has no `src/` or `ports/` directories. J1 will introduce them after its own Spec Kit lot; empty directories would misleadingly imply implemented OS components.
