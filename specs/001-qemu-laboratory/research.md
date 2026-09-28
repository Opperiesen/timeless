# J0 Research: Reproducible QEMU Laboratory

## Decision 1 — Development machine and boot contract

**Decision:** Use QEMU's versioned `virt-10.0` Arm virtual board, an AArch64 `cortex-a53` guest with one CPU, 256 MiB RAM, a PL011 serial console, TCG emulation, no guest NIC, and a raw AArch64 kernel image via `-kernel` for the first J1 boot experiment. The image is not produced by J0. QEMU generates the DTB and supplies its address in `x0` for this non-ELF direct-boot path. The startup stub must preserve `x0` for the machine port, which must discover devices from the DTB rather than hard-code peripheral addresses. Versioned machine selection is provisional and validated against the actual emulator in preflight.

**Rationale:** QEMU documents `virt` as a development board rather than real phone hardware; its machine revisions stabilize the board model. The direct-boot convention avoids a shipped third-party bootloader in the first experiment. The fixed CPU and TCG avoid host-specific acceleration or `-cpu max` variability. Explicit `-nic none` disables the default user-mode networking. Serial is an observable first J1 test output, not evidence of a mobile UI.

**Alternatives considered:** Unversioned `virt` (moving target); x86_64 PC (mature tooling but less directly comparable to likely ARM handset ports); 32-bit Arm (memory-model constraints); UEFI plus disk image (extra firmware and boot surface); ELF bare-metal boot (DTB starts at RAM base rather than the x0 Linux-style protocol, so a different contract); KVM (host dependent). These are not final OS architecture decisions.

**Primary references:** [QEMU Arm virt](https://www.qemu.org/docs/master/system/arm/virt), [QEMU Arm system target](https://www.qemu.org/docs/master/system/target-arm), [QEMU command-line and `-nic none`](https://www.qemu.org/docs/master/system/qemu-manpage.html).

## Decision 2 — Tool version policy

**Decision:** Maintain a `toolchain.lock` with exact Debian package versions and upstream tool versions observed when actually installed. Preflight checks the executable version and `virt-10.0` machine availability; compilation requirements remain recorded but cannot be marked verified until an actual build. Never infer installed versions from an apt candidate. Host shell/Python standard library can implement the J0 verification harness; the future J1 compiler/linker choice remains subject to a bounded comparison.

**Rationale:** An explicit lock is testable and does not silently accept a future emulator whose board behavior might differ. Debian package version pinning gives clean-host provisioning an auditable path, but repository scripts do not silently install system packages.

**Alternatives considered:** Container digest (reproducible but unavailable container runtime in the current environment); unconstrained apt latest (unreproducible); vendored emulator binaries (large, licensing and update burden).

## Decision 3 — Evidence boundary

**Decision:** J0 preflight and machine introspection have independently verifiable pass/fail states. Actual kernel boot, response-time distributions and phone performance remain `untested` until their own raw traces exist. A future guest boot test will check a Timeless-specific sentinel emitted over serial, bounded by a timeout; QEMU process startup alone is never boot evidence. Store raw output and metadata with any measured result.

**Rationale:** The constitution forbids presenting a bootless emulator as a working OS or applying QEMU timing to phones.

**Alternatives considered:** Screenshots or human-only run notes (weak regression detection); a synthetic baseline (invalid evidence).

## Unresolved by design

Final kernel language, microkernel/monolith organization, driver APIs, application ABI and real-device firmware policy are **not** selected by J0. J1 comparison experiments and later approved ADRs will determine these; no claimed J1 image exists in this record.
