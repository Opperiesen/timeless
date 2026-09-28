# Tasks: J0 Reproducible QEMU Laboratory

**Input**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/laboratory.md`. Tests are required by the specification. All paths are repository-relative.

## Phase 1: Setup

- [x] T001 Create pinned Linux-host tool and machine manifest with exact QEMU 10.0.13, Python 3.13.5, `virt-10.0`, `cortex-a53`, 256 MiB, one CPU, TCG and no NIC in `config/toolchain.lock.json`.

## Phase 2: Foundational

- [x] T002 Create CLI skeleton and manifest validation (`schema_version` = 1, required fields nonempty and positive memory/CPU) in `scripts/qemu_lab.py`.

## Phase 3: User Story 1 — Recreate the laboratory (P1, MVP)

**Independent test:** preflight reports actual versions, incompatible/missing tools fail; DTB inspection works on matching QEMU; missing image fails.

- [x] T003 [US1] Add failing tests for missing/wrong QEMU, missing image, machine argument safety and idempotence in `tests/test_qemu_lab.py`.
- [x] T004 [US1] Implement exact Python/QEMU version checks, machine availability and JSON preflight in `scripts/qemu_lab.py`.
- [x] T005 [US1] Implement DTB inspection without overwrite and missing-image rejection in `scripts/qemu_lab.py`.
- [x] T006 [US1] Implement `run --image` using fixed arguments and explicit guest NIC disabling, without claiming boot success, in `scripts/qemu_lab.py`.
- [x] T007 [US1] Execute commands from `specs/001-qemu-laboratory/quickstart.md` on provisioned QEMU and in a fresh Debian 13 rootfs with installed pinned packages; record versions, DTB digest and failure states in `specs/001-qemu-laboratory/evidence.md`. *(Second physical host not tested.)*

## Phase 4: User Story 2 — Trace the future boot and tests (P2)

**Independent test:** reviewer maps every J0 requirement and J1 gate to a test and confirms no autonomous-kernel claim.

- [x] T008 [P] [US2] Validate J1 raw-image, DTB-pointer and CPU/board/common boundaries as future contracts in `specs/001-qemu-laboratory/contracts/laboratory.md` and `docs/adr/0001-qemu-j0-lab.md`.
- [x] T009 [P] [US2] Map FR-001–FR-010, SC-001–SC-005 and J1 gates to evidence owners/statuses in `specs/001-qemu-laboratory/test-matrix.md`.
- [x] T010 [US2] Inventory host-tool licences separately from shipped runtime exceptions in `docs/adr/0001-qemu-j0-lab.md`; document a reusable exception record in `specs/001-qemu-laboratory/data-model.md`. *(136-package host closure inventoried; redistribution/legal review remains out of scope.)*

## Phase 5: User Story 3 — Prepare honest measurements (P3)

**Independent test:** no synthetic performance value appears; a reviewer can reproduce the specified future scenario and raw-trace derivation.

- [x] T011 [P] [US3] Document scenario, environment, raw traces, tail calculations, failure handling and QEMU-only validity in `docs/measurement.md`.
- [x] T012 [US3] Cross-check baseline status against actual available evidence in `specs/001-qemu-laboratory/evidence.md` and keep `docs/measurement.md` marked not measured.

## Final Phase: Integration and review

- [x] T013 Run `python3 -m unittest discover -s tests -v` and documented preflight/inspect/missing-image procedures; archive genuine outcomes in `specs/001-qemu-laboratory/evidence.md`.
- [x] T014 Review constitutional gates, verify `git diff --check` and documentation claims, and update `README.md` with actual J0 status and entrypoint. *(Two independent read-only review passes in review.md; findings corrected and re-tested by the author.)*
- [ ] T015 Commit reviewed artifacts on `feat/j0-qemu-laboratory`; open a PR with Spec Kit link, evidence and limitations, without pushing to `main` directly.

## Dependencies & Execution Order

T001 → T002 → T003 (observe failure) → T004–T006 → T007. T008 and T009 can proceed in parallel after foundational setup; T011 can proceed independently in parallel. T010 follows T008; T012 follows T007 and T011. T013–T015 integrate all stories. MVP is T001–T007 (US1); J0 complete includes US2/US3 and review.

## Parallel Examples

- `[US2] T008` and `[US2] T009` edit different files and can run together.
- `[US3] T011` can proceed while `[US1] T003–T006` changes only tests/scripts.

## Implementation Strategy

Write failure-mode tests before CLI behavior. Keep QEMU local tooling out of the shipped guest; record real observations and do not infer kernel readiness from DTB generation. A missing QEMU package is an explicit blocker, not a reason to invent emulator output.
