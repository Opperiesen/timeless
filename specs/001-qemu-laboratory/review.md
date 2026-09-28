# Independent J0 review and disposition — 2026-09-28

An independent, read-only reviewer inspected the specification, CLI, unit tests and actual evidence. The reviewer verified that the archived DTB matches its reported length, SHA-256 and header, that the Debian-rootfs package inventory has 136 entries, and that the fresh rootfs replay is clearly distinguished from a second-host reproduction. The reviewer **did not rerun the tests**. Initial verdict: J0 laboratory demonstrated, but acceptance partial pending the following fixes.

| Finding | Disposition and verification |
|---|---|
| Upstream versions checked but pinned Debian package revisions not enforced | Added `checked_debian_packages()` for stock manifest/default executable; preflight JSON now records observed package versions or labels an override/custom manifest as unverified at package level. Regression test rejects a mismatched QEMU Debian revision. Fresh-rootfs preflight reports both pinned revisions. |
| `inspect` could follow a dangling output symlink or accept comma-separated QEMU options in the output path | Regression tests first reproduced both failures. `inspect` now refuses comma-containing paths and existing paths including dangling symlinks; QEMU writes into a private temporary directory, then a no-overwrite hard link promotes the result. All tests and real fresh-rootfs DTB inspection pass. |
| TCG / no guest NIC described as a QEMU host sandbox | ADR and quickstart now state explicitly that QEMU is not host-sandboxed and that only trusted local inputs are accepted at J0. Untrusted image execution needs a future host confinement policy. |
| J0 scenario traceability and repeated preparation were underspecified | Matrix now gives FR-001–010, SC-001–005, each of seven acceptance scenarios and J1 gates distinct pass rules, evidence, owner and status. Added a repeated-preflight no-source-mutation test. |

The author reran the full 15-test suite and the fresh Debian 13 rootfs replay after the first corrections. These checks demonstrate J0 laboratory behavior, **not** a Timeless boot or phone performance. No second physical host or independent legal licence audit was used. A second-host replay is an optional portability confirmation, not a claimed J0 observation.

## Second independent read-only pass

The second reviewer confirmed the four original corrections, reran the 15 host tests successfully, checked the DTB magic/length/digest, package inventory and manifest digest, but did **not** rerun the real QEMU/rootfs. They found one further blocker: the stock CLI resolved QEMU through `PATH` while separately checking the installed Debian package version; a shadow executable could claim the same upstream version and be misidentified as package-verified. They also reiterated the pending Git commit/PR gate.

The author added `test_stock_preflight_rejects_path_shadowing_packaged_qemu` (RED then GREEN); the stock CLI now requires the running QEMU and Python executables to be the same files as the Debian-installed `/usr/bin` executables before validating package revisions. Overrides/custom manifests continue to label package verification skipped. The final **16-test** suite passes both on the provisioned host and in the fresh Debian 13 rootfs; real preflight/DTB inspection/missing-image behavior was replayed again in that rootfs after this correction. This is the author's post-review verification, not a third independent certification of the final tree.
