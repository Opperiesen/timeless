# J0 Data Model

## Laboratory manifest

`config/toolchain.lock.json` declares `schema_version` (1), `host` (Linux amd64; Python 3.13.5), `qemu` (`version`: 10.0.13, Debian package version and executable), and `machine` (`type`: virt-10.0, `cpu`: cortex-a53, `memory_mib`: 256, `cpus`: 1, `accelerator`: tcg, `network`: none). Configuration is committed; observed versions belong in evidence output, never silently copied as a claimed observation.

## Evidence run

The J0 evidence bundle consists of CLI JSON (`preflight` or `inspect`), a human-readable execution record (`evidence.md`) and, for inspection, the compressed raw DTB. CLI JSON reports observed Python/QEMU versions, selected machine and arguments; `inspect` also reports output path, byte count and SHA-256. The execution record contains the date, commands, exit statuses, manifest digest, base revision (with uncommitted-work caveat), and limits. J0 did **not** capture per-command UTC timestamps, full host build metadata or a committed J0 revision; these are future evidence-harness improvements, not fields to infer from the manifest. A future J1 boot record needs a real serial trace and expected sentinel; a missing image is an error, not a successful boot. Raw evidence is archived alongside the record and must not be replaced by calculated numbers alone.

## Test matrix entry

Each row contains stable requirement or constitution-gate ID, scenario, observable pass condition, intended evidence file, owner (`J0 lab` or `J1 OS`), and one state: `tested functional`, `partial`, `untested`, `blocked`. Status changes require a trace and commit reference. See [test-matrix.md](test-matrix.md).

## Architecture decision / exception

An ADR records context, alternatives, decision, impact, reversibility and deferred choices. QEMU and Python are build/test tools, not guest-runtime exceptions. Before introducing a shipped dependency, record a reviewed exception with:

| Field | Required content |
|---|---|
| Component, version, upstream and source digest | Precisely identify what would ship. |
| Licence and distribution obligations | Include the full licence identifier, notices and compatibility review. |
| Technical necessity and alternatives | Explain why original implementation is unsafe or impractical and what was rejected. |
| Attack surface and trust boundary | Describe parsed inputs, privileges, exposed interfaces and threat assumptions. |
| Isolation and update policy | Specify containment, monitoring, patch owner and vulnerability response. |
| Replacement or removal path | State what would allow the exception to be retired. |
| Approval and evidence | Link the ADR, reviewer, test artifacts, date and scope of approval. |
