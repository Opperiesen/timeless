# ADR 0001 — Provisional AArch64 QEMU laboratory

**Status:** Accepted for J0 laboratory only (2026-09-28). **Scope:** `specs/001-qemu-laboratory/`.

## Context and alternatives

The first research environment must expose a reproducible boot interface without claiming a real-phone port. A versioned `virt-10.0` AArch64 board supports an emulated CPU, generated DTB and serial diagnostics. We considered an unversioned `virt` (machine drifts with emulator upgrades), x86 PC (less representative of likely ARM ports), UEFI (additional firmware/bootloader), and hardware acceleration (host-dependent). We chose one fixed machine/CPU and software emulation for J0; another target will eventually be needed for port-separation evidence.

## Decision and boundaries

Pin QEMU 10.0.13 and `virt-10.0`, `cortex-a53`, one vCPU, 256 MiB RAM, TCG, serial console and no guest NIC. Generate and inspect QEMU's DTB. A later raw-image experiment must verify the loader/header, entry state and x0 DTB handoff rather than assuming every binary boots. Guest boot and diagnostics are J1 work. Future source layout separates CPU startup, QEMU board adaptation, and common kernel; no guest runtime code is reused from QEMU.

This is **not** a final choice of CPU coverage, language, kernel organization, driver architecture or app ABI. Compare bounded prototypes and write later ADRs before locking those. Real hardware requires a separately approved target, recovery plan and firmware policy. The network/personal-data policy remains unratified; no public guest networking.

## Consequences

Reproduction requires the exact QEMU release and Python tool. Host tooling QEMU/Python is not shipped OS code; its package licences are external tool licences. Runtime exceptions: **none in J0**. For any later shipped component record provenance, licence, technical reason, attack surface, isolation and replacement path in a reviewed register. Device-tree contents and timing are specific to this virtual board; no real-phone capability or latency follows from them.

## Dependency inventory and licence boundary

| Host dependency | Provenance and licence evidence | Purpose / scope / replacement |
|---|---|---|
| CPython 3.13.5 (`python3=3.13.5-1`) | Debian 13 package from upstream Python; `/usr/share/doc/python3.13/copyright` contains the Python/PSF licence and notices for bundled components | Runs the host CLI and standard-library `unittest`; not linked into or shipped in the guest. Replace with a reviewed equivalent host runner after validation. |
| QEMU `qemu-system-arm=1:10.0.13+ds-0+deb13u1` (provides `qemu-system-aarch64`) | Debian 13 package from QEMU; `/usr/share/doc/qemu-system-common/copyright` states GPL-2 for QEMU as a whole and documents component-specific licences | Host-only virtual board, generated DTB and future guest execution. TCG and no guest NIC do **not** sandbox the host process; only trusted local inputs may be supplied at J0. For untrusted images, use a separate host-side confinement policy before execution. Replace or update only after machine/DTB comparison and lock revision. |
| QEMU package's transitive shared-library dependencies | Resolved by Debian APT. [Fresh-rootfs inventory](../../specs/001-qemu-laboratory/evidence/clean-host-packages.json) records 136 installed packages (minbase plus Python/QEMU closure), version, copyright-file path/digest and any parseable licence fields; no copyright files were missing. This is not a standalone redistributable tool bundle. | Host process only; package manager handles provenance/licences, not copied into the Timeless runtime. An offline distributable lab would need separate legal review and a complete redistribution manifest. |

This inventory is limited to the two direct host tools and their package-managed dependencies; no guest firmware, third-party runtime library, or proprietary blob is approved. QEMU is a development tool, not the kernel. The first actual shipped runtime dependency would require the exception record specified in [the data model](../../specs/001-qemu-laboratory/data-model.md) before inclusion.

**References:** [QEMU Arm virt](https://www.qemu.org/docs/master/system/arm/virt), [QEMU Arm target](https://www.qemu.org/docs/master/system/target-arm), [laboratory research](../../specs/001-qemu-laboratory/research.md).
