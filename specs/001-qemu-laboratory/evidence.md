# J0 execution evidence — 2026-09-28

**Scope:** two actual executions: one provisioned Linux x86_64 host (QEMU extracted from Debian packages, with `LD_LIBRARY_PATH`) and a newly bootstrapped, isolated Debian 13 amd64 root filesystem. The latter was provisioned with `mmdebstrap` in root mode from `deb.debian.org/debian`, minbase plus exact `python3=3.13.5-1` and `qemu-system-arm=1:10.0.13+ds-0+deb13u1`, then exercised through `chroot` with a clean environment and no host QEMU libraries. It is a **fresh rootfs replay on the same physical host**, not an independently provisioned second machine. No Timeless guest boot was attempted.

Manifest SHA-256 after review fixes: `cf2138e92ec528e4d3464df69090e042e0878eb7d9a0b6325e0dd12f827b8192`. Repository base revision at execution: `e03a5ae`; the J0 changes were still **uncommitted**, so this hash alone does not identify the exact working tree. The evidence was captured on 2026-09-28; no per-command timestamps were collected. The original provisioned-host JSON files predate the review fixes and the manifest revision; the fresh-rootfs JSON files below reflect the updated CLI and lock.

## Observed outcomes

- Original `python3 -m unittest discover -s tests -v`: **11 tests, OK** at the first provisioned-host capture. After two independent-review passes the full suite contains **16 tests, OK**; these use synthetic QEMU executables to test failures, argument construction and CLI contract, not guest boot.
- `python3 scripts/qemu_lab.py preflight --qemu-bin /home/hermes/.hermes/cache/scratch/timeless-qemu/usr/bin/qemu-system-aarch64`: **exit 0** with actual Python `3.13.5`, QEMU `10.0.13`, machine `virt-10.0`, CPU `cortex-a53`, one CPU, 256 MiB, TCG and `-nic none`. Raw JSON: [evidence/preflight.json](evidence/preflight.json).
- `python3 scripts/qemu_lab.py inspect --qemu-bin ... --output /home/hermes/.hermes/cache/scratch/timeless-qemu/repeat-j0.dtb`: **exit 0**; QEMU generated a 1,048,576-byte DTB. SHA-256 `268dd1a19173588a4d7e25f21cc1eee1d4fe4dd1acd8efc202b8d31c0002b030`. Raw JSON: [evidence/inspect.json](evidence/inspect.json); compressed raw DTB: [evidence/board.dtb.gz](evidence/board.dtb.gz). `gzip -dc evidence/board.dtb.gz | sha256sum` returned the same digest. A second inspection produced the same digest on this host. The temporary absolute paths in the JSON describe the original run, not portable output locations.
- `python3 scripts/qemu_lab.py run --qemu-bin ... --image /home/hermes/.hermes/cache/scratch/timeless-qemu/no-j1-image.img`: **exit 2**, stderr `Laboratory error: Kernel image missing or empty (J1 has not produced one): /home/hermes/.hermes/cache/scratch/timeless-qemu/no-j1-image.img`. This is the intended absence-of-image diagnostic, **not** an autonomous boot test.
- `git diff --check`: **exit 0**. Generated raw DTBs and caches are ignored by Git; only the explicitly archived compressed sample is retained.

## Fresh Debian 13 rootfs replay

The bootstrap and replay ran on 2026-09-28. An initial unprivileged `mmdebstrap --mode=chrootless` attempt failed at package ownership/permissions; it was **not** treated as success. The successful path invoked root *inside the existing Hermes LXC* via `pct exec 107` to run `mmdebstrap --mode=root`; it wrote only to `/home/hermes/.hermes/cache/scratch/j0-clean-host/rootfs-root`. Root privilege was an explicit one-off operator action, **not** used by the repository or its quickstart. The rootfs contains Debian GNU/Linux 13 (trixie), `python3` package `3.13.5-1` and `qemu-system-arm` package `1:10.0.13+ds-0+deb13u1`. Only `config/`, `scripts/` and `tests/` were copied into `/work` for testing; no host Python or QEMU binary/library was bind-mounted. The rootfs is disposable and is not committed.

- `python3 -m unittest discover -s tests -v`: **16 tests, OK** within the rootfs after both review fixes.
- `python3 scripts/qemu_lab.py preflight`: **exit 0**; [raw result](evidence/clean-preflight.json) records the installed `/usr/bin/qemu-system-aarch64`, Python `3.13.5`, QEMU `10.0.13`, installed Debian package revisions `3.13.5-1` and `1:10.0.13+ds-0+deb13u1`, the fixed machine and `-nic none`.
- `python3 scripts/qemu_lab.py inspect --output /work/out/board-provenance.dtb`: **exit 0**; [raw result](evidence/clean-inspect.json) records `1048576` bytes and SHA-256 `268dd1a19173588a4d7e25f21cc1eee1d4fe4dd1acd8efc202b8d31c0002b030`, matching the archived [compressed DTB](evidence/board.dtb.gz). The actual fresh-rootfs DTB magic is `0xd00dfeed`.
- `python3 scripts/qemu_lab.py run --image /work/out/no-j1-image.img`: **exit 2** with [captured stderr](evidence/clean-missing-image.stderr). No image was fabricated to make a boot test pass.
- [Installed-package inventory](evidence/clean-host-packages.json): **136 installed Debian packages**, all with a copyright file path and SHA-256, plus any machine-readable `License:` declarations present. This is package/licence provenance for the fresh host tooling closure, **not** an assertion that those host packages are Timeless guest dependencies or an independent legal opinion.

This proves the documented CLI path on a newly bootstrapped Debian environment; it does not prove installation on an independently provisioned physical/virtual Debian host, phone behavior, or J1 boot.

## Boundaries and next verification

No Timeless image, serial sentinel, kernel, timing baseline, phone hardware test, or second-host replay was available. `run` with a real J1 image was **not exercised**. The QEMU-only DTB validates the chosen virtual board, not a physical device. The proposed image header/entry handoff remains a J1 hypothesis to verify with a boot experiment. No performance value is published; [docs/measurement.md](../../docs/measurement.md) says **not measured**.

To recheck the archived raw artifact: `gzip -dc specs/001-qemu-laboratory/evidence/board.dtb.gz | sha256sum`.

## Constitution compliance review (J0 scope)

- **I — measurement:** no baseline or phone-latency claim; raw DTB evidence and a future measurement protocol are kept separate.
- **II — portability:** the machine port, CPU startup, and common code are future contracts; no guest code exists to assess yet.
- **III — originality/dependencies:** no guest runtime dependency or firmware exception exists; host Python/QEMU and their licence evidence are documented in ADR 0001.
- **IV — evidence:** local QEMU and fresh Debian rootfs preflight/inspection are distinguished from a second-host setup and untested J1 boot.
- **V — hardware safety:** no real-device purchase, flash, personal data, or public guest networking; `-nic none` is visible in the actual preflight arguments.
- **VI — traceability:** requirements, plan, tasks, per-scenario matrix, CLI, tests and evidence are linked; two [independent review passes](review.md) identified gaps, then corrections were re-tested by the author.
- **VII — auditable Git:** work is on `feat/j0-qemu-laboratory`; at evidence capture no commit or pull request had been made. This remains an **open gate** until the branch/PR are read back.
