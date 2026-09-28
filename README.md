# Timeless

An original, responsive, and portable mobile operating system designed to extend the useful life of
older smartphones without bloatware.

> **Project status: J0 — specification and reproducible laboratory.** No kernel, QEMU prototype, or
> hardware port is currently claimed to exist.

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

## Starting Work

The first work item will be a J0 specification for a reproducible QEMU laboratory and proof of
independent kernel boot. No device purchase, device flashing, or exposure to personal data or the
public Internet belongs to this initial repository state.

## Contributing

Every work item uses a dedicated branch and a documented pull request. Commits follow Conventional
Commits; pull requests link the relevant Spec Kit artifacts, test and measurement evidence, and
corresponding documentation updates.
