# J0/J1 Test Matrix

Status after J0 validation on 2026-09-28. See [evidence.md](evidence.md) for actual commands, fresh Debian 13 rootfs replay, raw JSON and compressed DTB. A second-host replay remains untested. [Independent review](review.md) identified issues that were corrected and re-tested; the reviewer did not rerun the tests. `tested functional` applies only to J0 laboratory behavior, never to a guest OS.

| Requirement/gate | Observable test and pass condition | Evidence | Owner | Status |
|---|---|---|---|---|
| FR-001 | Introspection emits a nonempty DTB for exact board/CPU/RAM and logs parameters | [inspect JSON](evidence/inspect.json), [compressed raw DTB](evidence/board.dtb.gz), SHA-256 in [evidence.md](evidence.md) | J0 lab | tested functional |
| FR-002 | Preflight rejects wrong/missing Python/QEMU and mismatched Debian package versions; reports actual versions and machine | [fresh-rootfs preflight](evidence/clean-preflight.json), version-error unit tests | J0 lab | tested functional (stock manifest) |
| FR-003 | Guide executed in fresh Debian 13 rootfs with APT-installed pinned tools; absent image exits nonzero | [rootfs replay](evidence.md), [captured stderr](evidence/clean-missing-image.stderr); second physical host not tested | J0 lab | tested functional (fresh rootfs) |
| FR-004 | CLI args explicitly disable guest NIC and acceleration dependency | unit test and [fresh-rootfs preflight arguments](evidence/clean-preflight.json); no real guest boot | J0 lab | tested functional (launch arguments only) |
| FR-005 | Contract distinguishes boot stub, port and common code; no kernel claim | [contract](contracts/laboratory.md) + [ADR](../../docs/adr/0001-qemu-j0-lab.md) | J0 lab | tested functional (documentation only) |
| FR-006 | Every listed J0 scenario/requirement and J1 gate mapped to pass rule, evidence, owner and status | this matrix, [review](review.md) | J0 lab | reviewed (J0 scope) |
| FR-007 | ADR compares alternatives and deferred choices | [ADR](../../docs/adr/0001-qemu-j0-lab.md) | J0 lab | tested functional (documentation only) |
| FR-008 | Measurement method exists; baseline explicitly unmeasured | [measurement protocol](../../docs/measurement.md), [evidence](evidence.md) | J0 lab | tested functional (documentation only) |
| FR-009 | Tool-vs-runtime inventory and exception template reviewed | [ADR](../../docs/adr/0001-qemu-j0-lab.md), [data model](data-model.md), [fresh host package closure](evidence/clean-host-packages.json); guest runtime has no dependencies | J0 lab | tested functional (host inventory; not legal audit) |
| FR-010 | Claims match actual runs, distinguish QEMU laboratory and guest OS | [evidence](evidence.md), [review](review.md) | J0 lab | reviewed (J0 scope) |
| SC-001 | Repeat path from fresh supported userspace to missing-image diagnosis | [rootfs replay](evidence.md), [stderr](evidence/clean-missing-image.stderr) | J0 lab | tested (same physical host) |
| SC-002 | Exact observed upstream and Debian package versions; missing/mismatch nonzero | [fresh-rootfs preflight](evidence/clean-preflight.json), unit tests | J0 lab | tested (stock manifest) |
| SC-003 | All J0 scenarios and J1 gates have observable rule and honest status | this matrix and [review](review.md) | J0 lab | reviewed |
| SC-004 | No invented performance values; baseline not measured | [measurement protocol](../../docs/measurement.md), [evidence](evidence.md) | J0 lab | tested (documentation only) |
| SC-005 | Independent reviewer distinguishes J0 evidence from future J1 claims | [review](review.md), [evidence](evidence.md) | J0 lab | reviewed; fixes re-tested by author |
| J1 autonomous boot/console | Timeless-specific serial sentinel after image boot, bounded timeout | future serial trace | J1 OS | untested |
| J1 clock/interrupts | Timer IRQ count and fault cases exercised | future trace/test | J1 OS | untested |
| J1 memory/isolated tasks | Separate tasks cannot corrupt each other's memory; failure reported | future isolation test | J1 OS | untested |
| J1 basic storage | Write/read/restart persistence and error test | future trace/test | J1 OS | untested |
| J1 automated regression | Regressed image fails CI with nonzero result | future CI log | J1 OS | untested |
| J1 common/port boundary | Separate modules and interface tests inspected | future code/test review | J1 OS | untested |

## Acceptance scenarios (from [spec.md](spec.md))

| Scenario | Observable pass rule | Evidence | Owner | Status |
|---|---|---|---|---|
| US1-1 | Fresh Debian userspace reports exact versions and machine; `run` without J1 image fails clearly | [rootfs replay](evidence.md), [preflight](evidence/clean-preflight.json), [stderr](evidence/clean-missing-image.stderr) | J0 lab | tested in fresh rootfs; second host untested |
| US1-2 | Absent/mismatched binary, upstream or Debian package version exits nonzero with diagnostic | `test_missing_qemu_fails_visibly`, `test_wrong_qemu_version_is_rejected`, `test_python_version_mismatch_is_rejected_before_qemu`, `test_debian_package_version_mismatch_is_rejected` in [tests](../../tests/test_qemu_lab.py) | J0 lab | tested |
| US1-3 | Repeated preparation leaves tracked inputs intact and preflight stable | `test_repeated_preflight_preserves_source_and_returns_same_result` in [tests](../../tests/test_qemu_lab.py); [rootfs replay](evidence.md) | J0 lab | tested for preflight; inspection uses fresh output path |
| US2-1 | J1 gate has named future component, pass rule and honest status | J1 rows above; [contract](contracts/laboratory.md) | J1 OS | specified, not run |
| US2-2 | Any boot/performance claim has real trace or is explicitly untested | [evidence](evidence.md), [measurement](../../docs/measurement.md), [review](review.md) | J0 lab | reviewed; boot/performance untested |
| US3-1 | Baseline says not measured and contains no synthetic latency | [measurement](../../docs/measurement.md), [review](review.md) | J0 lab | reviewed |
| US3-2 | Future measurement record associates tool versions, scenario, raw trace, calculation, QEMU-only limit | [measurement](../../docs/measurement.md), [data model](data-model.md) | J1 measurement | specified, no guest to measure |
