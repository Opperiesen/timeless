# Feature Specification: J0 Reproducible QEMU Laboratory

**Feature Branch**: `feat/j0-qemu-laboratory`

**Created**: 2026-09-28

**Status**: Implemented (J0 laboratory; pull-request review pending)

**Input**: Start J0 of Timeless: establish verifiable requirements, a test matrix, pinned tooling, a documented QEMU machine and boot path, reproducible build/run scripts, an initial architecture record, and a measurement method without invented results.

## User Scenarios & Testing

### User Story 1 - Recreate the laboratory (Priority: P1)

A contributor can identify the exact required tools, reproduce the laboratory setup on a supported host, and launch the selected virtual machine without relying on undocumented local state.

**Why this priority**: A repeatable environment is a prerequisite for meaningful J1 boot evidence.

**Independent Test**: In a clean supported environment, follow the guide to provision or verify the pinned tools, run the laboratory command and inspect its machine configuration. No Timeless kernel is required for this J0 test.

**Acceptance Scenarios**:

1. **Given** a supported host with prerequisites available, **when** the contributor follows the documented setup and verification procedure, **then** the command reports the selected virtual-machine configuration and exact tool versions and either launches QEMU with a deliberately supplied image or clearly reports that a J1 image is not yet present.
2. **Given** a missing or mismatched required tool, **when** the contributor runs preflight, **then** it exits nonzero with an actionable diagnostic rather than silently selecting an unpinned substitute.
3. **Given** the same inputs and pinned toolchain, **when** the contributor runs the preparation procedure again, **then** it does not mutate tracked source or require hidden manual steps.

---

### User Story 2 - Trace the future boot and tests (Priority: P2)

A developer can see the target machine, the proposed boot interface, the boundary between common code and a QEMU port, and the acceptance tests that J1 must eventually satisfy, without mistaking the laboratory for an implemented kernel.

**Why this priority**: Architectural decisions and negative-space documentation prevent an emulator-specific prototype from masquerading as a portable OS.

**Independent Test**: Review the architecture record, boot contract and test matrix against the J1 constitution gate; each listed capability has an observable test or is explicitly marked future/unverified.

**Acceptance Scenarios**:

1. **Given** the J0 artifacts, **when** a developer traces a J1 capability, **then** they find its observable evidence, pass/fail rule and owning future component.
2. **Given** a claim about a running kernel or phone performance, **when** a reviewer checks the evidence record, **then** the claim is either backed by actual traces or marked not yet tested.

---

### User Story 3 - Prepare honest measurements (Priority: P3)

A tester can capture the exact environment, scenario, raw output and calculation method for a repeatable virtual-machine run, and can distinguish missing baseline data from a measured baseline.

**Why this priority**: Responsiveness and stability claims must be auditable rather than inferred from a successful emulator launch.

**Independent Test**: Use a dry-run or failed-run example to verify that the measurement record preserves environment metadata and does not fabricate latency or reliability numbers.

**Acceptance Scenarios**:

1. **Given** no runnable J1 image, **when** the tester opens the baseline record, **then** it states "not measured" and contains a reproducible measurement protocol, not an invented value.
2. **Given** a later actual run, **when** evidence is archived, **then** the run can be associated with tool versions, input scenario, raw trace, calculation script or steps, and a clear QEMU-only limitation.

### Edge Cases

- Nested virtualization or hardware acceleration is unavailable: the guide identifies the selected emulation mode and does not silently require acceleration.
- The requested guest image is absent or invalid: the runner fails visibly, without treating QEMU's process startup as an OS boot pass.
- A tool version differs across host packages: the recorded version is exact and preflight fails or explains the explicit, documented compatibility policy.
- QEMU hangs or exits unexpectedly: future boot validation has a bounded timeout, captures diagnostics and fails closed.
- The guest attempts network access: the laboratory starts without public networking; personal data is never an input.

## Requirements

### Functional Requirements

- **FR-001**: The laboratory MUST document one specific virtual machine, CPU model, memory configuration, console, and boot entry method, including the source of the guest's hardware description.
- **FR-002**: The J0 laboratory MUST declare exact versions of required emulation and host-side test tools and report observed versions in a reproducible preflight record. J1 compilation and linking tools MUST be pinned when selected after a comparative build experiment; any supported version range MUST be explicit rather than implicit.
- **FR-003**: Contributors MUST have a documented, repeatable procedure to prepare, check and launch the target machine from a clean supported host. A missing image or incompatible tool MUST fail visibly.
- **FR-004**: The launch procedure MUST use deterministic machine arguments and disable guest access to public networks by default.
- **FR-005**: The artifacts MUST define a boot-input/output contract for a future autonomous kernel and separate future common-system work from architecture and machine-port responsibilities. Defining the contract MUST NOT count as implementing J1 boot.
- **FR-006**: A requirements-to-tests matrix MUST map every J0 acceptance condition and each J1 constitution gate to an observable test, evidence artifact, owner and current verification status.
- **FR-007**: An initial architecture decision record MUST compare bounded target/boot alternatives, explain the temporary J0 selection and defer final CPU, kernel organization, system language, application format and driver strategy until comparative J1 prototypes where applicable.
- **FR-008**: The laboratory MUST publish a repeatable measurement protocol covering scenario, environment, raw trace, calculation and interpretation; it MUST distinguish an unmeasured baseline from actual results and prohibit QEMU data being reported as real-phone responsiveness.
- **FR-009**: Each runtime or build dependency and any future firmware/bootloader exception MUST be tracked with provenance, licence, technical reason, attack surface, isolation and replacement path as appropriate; build tools MUST be distinguished from shipped OS components.
- **FR-010**: J0 documentation and scripts MUST state what was actually run and verified, with instructions and evidence recorded in English. No kernel, device port, or performance capability may be marked functional without real execution evidence.

### Key Entities

- **Laboratory manifest**: Virtual machine configuration, boot method, required tools and version policy.
- **Test-matrix entry**: Requirement or milestone, observable test, expected result, evidence path, responsible component and status.
- **Evidence run**: Scenario, environment, command, exit status, raw trace, derivation method and explicit validity scope.
- **Architecture decision**: Context, options, selection, risks, reversibility and deferred decisions.
- **Dependency exception**: Provenance, licence, necessity, attack surface, isolation and replacement path, if the dependency is shipped or imposed.

## Success Criteria

### Measurable Outcomes

- **SC-001**: A contributor can follow one documented path from a fresh supported environment to either a launched configured virtual machine or an explicit missing-J1-image result, with zero undocumented manual configuration steps.
- **SC-002**: All required tools are recorded with observed versions and all absent or unsupported prerequisites produce a nonzero preflight result; no silent fallbacks occur.
- **SC-003**: 100% of J0 acceptance requirements and the enumerated J1 constitution gate have a corresponding observable test and honest status in the matrix.
- **SC-004**: 100% of published performance baseline values are derived from archived raw observations; in J0, before a runnable image, the baseline remains explicitly unmeasured.
- **SC-005**: At least one independent reviewer can distinguish, using the artifacts alone, what was exercised at J0 and what remains for J1, with no boot-success or phone-performance claim lacking evidence.

## Assumptions

- J0 is laboratory and design work only; implementing an autonomous kernel, interrupt handling, memory management and storage belongs to J1.
- Initial supported host is Linux; other host platforms are not claimed. The chosen QEMU machine is a virtual development target, not a phone compatibility claim.
- Build and test tools can be reused as tools without making Timeless a derivative OS. Any code shipped into a guest is separately scrutinized.
- There is no J1 image at the start of J0. A documented absent-image preflight is an honest success for laboratory readiness, not a boot demonstration.
- No public network exposure or personal data is permitted before the separate safety policy is ratified. Closed-firmware acceptance is deferred until real-device target selection.
