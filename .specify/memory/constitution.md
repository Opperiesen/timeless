# Timeless Constitution

## Core Principles

### I. Measured Responsiveness and Stability First
Every design, implementation, and port MUST prioritize perceived input-to-visible-response latency,
absence of prolonged stalls, recovery from faults, and data integrity over feature count, average FPS,
or boot-time claims. Measurements MUST archive the fixed environment, scenario, raw traces, and
calculation method. QEMU measurements MAY detect regressions only; they MUST NOT be presented as
proof of real-phone fluidity.

Rationale: the project exists to make old phones pleasant and dependable to use, not merely to
produce a booting kernel.

### II. Portable Core, Explicit Ports
The common core MUST remain independent of QEMU and any individual device. CPU-specific startup,
interrupts, memory primitives, and device adaptation MUST be isolated behind documented interfaces.
A port MUST contain only the code and metadata required for its target. Applications compatible with
the same ABI MUST run unchanged; a CPU-architecture port MAY require recompilation but MUST NOT
require application rewrites.

Rationale: portability is a primary outcome, so device shortcuts cannot become hidden global
assumptions.

### III. Original System With Accountable Exceptions
Timeless MUST implement its own kernel, essential services, hardware abstraction, mobile interface,
and application model rather than ship a themed Linux distribution, Android ROM, or launcher.
Each reused runtime component, imposed bootloader, firmware blob, or external library MUST have an
exception record stating provenance, licence, technical reason, attack surface, isolation, and
replacement path. Timeless source code, build and test tooling, specifications, architecture records,
and documentation MUST be publicly available to the community. Project code MUST be licensed
GPL-3.0-or-later unless a separately approved exception record establishes that a compatible licence
is technically necessary. Cryptography MUST use reviewed components or well-established primitives;
it MUST NOT be improvised to satisfy a zero-dependency claim.

Rationale: originality is an objective, while security and practical hardware constraints forbid
unexamined absolutism.

### IV. Evidence Before Capability Claims
A capability MUST be documented only at its verified state: tested functional, partial, untested, or
blocked. A successful boot MUST NOT be described as daily-usable telephony. Code, automated tests,
reproducible execution instructions, traces or other proof, and matching documentation MUST be
submitted together for a feature to be complete. Documentation commands MUST have been executed in
a clean environment or be explicitly marked unverified.

Rationale: portable operating-system work is unusually vulnerable to plausible but untested claims.

### V. Reversible and Safe Hardware Work
No device purchase, destructive flash, firmware/baseband modification, or irrecoverable hardware
operation may occur without Gabin's explicit approval. Real-device work MUST first document the exact
variant, boot and recovery paths, backups, testable rollback procedure, required firmware, and known
risks. The radio/baseband firmware MUST remain outside the project's required modification path.

Rationale: physical targets are scarce, heterogeneous, and can be permanently damaged or made
unrecoverable.

### VI. Spec Kit Traceability Is Mandatory
Every functional lot MUST follow Spec Kit in order: specification, clarification, technical plan,
tasks, consistency analysis, implementation, then validation with real evidence. Requirements,
assumptions, decisions, tests, code, measurements, and documentation MUST remain traceable in the
repository. Subagents MUST own non-overlapping files or lots; the integrator remains responsible for
cross-artifact consistency.

Rationale: the project requires parallel work without losing evidence, intent, or architectural
coherence.

### VII. Auditable Git and Pull-Request Workflow
All repository changes MUST be attributable to a narrowly scoped branch and an intelligible commit
history. Each functional lot MUST use a branch named by purpose (`feat/`, `fix/`, `docs/`, `test/`,
`refactor/`, or `ci/`), make conventional commits, and land through a pull request into `main`.
Every pull request MUST state its linked Spec Kit artifact or issue, scope, architectural or dependency
exceptions, test and measurement evidence, documentation impact, and explicit remaining limitations.
Direct pushes to `main`, force-pushes of shared history, opaque bulk commits, and undocumented manual
changes are prohibited. The single bootstrap commit establishing a previously empty default branch MAY
be pushed directly, provided it records the repository's licence, constitution, and Spec Kit baseline.
Any other exception requires an emergency repair followed immediately by a documented ADR and pull
request.

Rationale: a public systems project needs a reviewable, reproducible history as much as it needs
reviewable source code.

## Safety, Scope, and Dependency Constraints

The first usable system MUST prove itself under QEMU before real-device porting. Selection of CPU
architecture, kernel structure, language, application format, and driver strategy MUST follow a
bounded comparative prototype documented by architecture decisions; none is presumed by this
constitution.

Until a network and personal-data safety policy is ratified, experimental builds MUST NOT be exposed
to the public Internet or used with personal data. The project MUST NOT promise universal hardware
support, a single binary for every device, Android/iOS compatibility, native WhatsApp, app-store
scope, cellular calling, VoLTE, universal Wi-Fi drivers, or unmeasured performance.

The project licence is GPL-3.0-or-later for project code. Documentation, specifications, and design
artifacts MUST use CC-BY-SA-4.0 unless an individual third-party item requires an identified compatible
licence. Required third-party firmware remains outside this licensing choice and MUST be recorded as
an exception.
TODO(CLOSED_FIRMWARE_POLICY): Gabin must define acceptance conditions for unavoidable closed firmware
before selecting a real-device target.
TODO(NETWORK_DATA_POLICY): Gabin must ratify the safety policy before personal data or Internet
exposure.

## Spec Kit Workflow and Evidence Gates

J0 establishes reproducible tooling, a QEMU machine and boot path, a test matrix, baseline method,
and initial architecture records without invented performance values. J1 requires an autonomous
kernel under QEMU, diagnostics, clock/interrupt handling, memory and isolated task foundations,
basic storage, automated failing-on-regression boot tests, and an explicit common-code/QEMU-port
boundary.

J2 requires a navigable mobile interface, physical-keyboard and simulated-touch input where available,
working application lifecycle and persistence, an actually functional demonstration application,
guest networking, error handling, repeatable trace scenarios, and documented normal/load behavior.
J3 requires a materially distinct virtual target or equivalent port-separation proof. J4 begins only
after J2/J3 evidence and Gabin's approval, then adds real-device capabilities incrementally with a
published device matrix and evidence for every reported state.

Architecture decisions that materially change scope, priority, safety, or portability require an ADR
and Gabin's approval before implementation proceeds. Performance thresholds and resource budgets are
set jointly after an observed baseline; no arbitrary target is treated as a promise.

## Governance

This constitution supersedes local conventions and planning artifacts. Every specification, plan,
task set, implementation review, and release/readiness decision MUST include an explicit compliance
check against its principles. A conflict with a MUST requirement blocks the affected work until the
artifact is corrected or this constitution is formally amended.

Amendments require: a written rationale; an impact review covering code, requirements, tests,
documentation, evidence, and device ports; Gabin's approval when scope, hardware risk, safety,
licensing, or project priorities change; and an updated Sync Impact Report. The report is temporary
review material and MUST be removed before committing the constitution.

Versioning is semantic: MAJOR for incompatible removal or redefinition of a governing principle;
MINOR for a new principle or materially expanded governance; PATCH for clarifications that do not
change obligations. Compliance reviews MUST reject aspirational claims unsupported by current,
reproducible evidence.

**Version**: 1.1.0 | **Ratified**: 2026-09-28 | **Last Amended**: 2026-09-28
