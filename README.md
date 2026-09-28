# Timeless

An original, responsive, and portable mobile operating system designed to extend the useful life of
older smartphones without bloatware.

> **Project status: J0 — a QEMU laboratory, not a guest OS.** Preflight, tests and DTB
> inspection ran both on a provisioned host and in a fresh Debian 13 rootfs with pinned packages.
> No second-host reproduction, Timeless kernel, autonomous boot, phone port, or performance baseline is claimed.

## Principles

- Measured perceived responsiveness and stability before feature count.
- A portable common core with hardware adaptations isolated by architecture and device.
- Public system source code, build tools, specifications, and documentation.
- Real evidence before any compatibility or performance claim.
- Reversible, documented hardware work requiring explicit approval.
- Mandatory workflow: Spec Kit → clarification → plan → tasks → analysis → implementation → evidence.

Read the complete project constitution in
[`.specify/memory/constitution.md`](.specify/memory/constitution.md).

## Licensing

Project code is distributed under **GPL-3.0-or-later**. Specifications, documentation, and design
artifacts are distributed under **CC-BY-SA-4.0** unless a third-party item states otherwise. Required
hardware firmware remains an external, documented dependency and is not part of Timeless.

See [`LICENSE`](LICENSE).

## J0 laboratory

The [J0 specification](specs/001-qemu-laboratory/spec.md),
[quickstart](specs/001-qemu-laboratory/quickstart.md),
[test matrix](specs/001-qemu-laboratory/test-matrix.md), and
[execution evidence](specs/001-qemu-laboratory/evidence.md) describe the `virt-10.0`
AArch64 board and its limits. Run `python3 -m unittest discover -s tests -v`, then
`python3 scripts/qemu_lab.py preflight` once the pinned host tools are available.
`inspect --output PATH` produces a DTB; `run --image PATH` requires a future J1 image and does
not itself prove a successful boot. No device purchase, flashing, personal data, or guest Internet
access belongs to J0.

## Contributing

Every work item uses a dedicated branch and a documented pull request. Commits follow Conventional
Commits; pull requests link the relevant Spec Kit artifacts, test and measurement evidence, and
corresponding documentation updates.
