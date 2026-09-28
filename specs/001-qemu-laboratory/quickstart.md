# J0 Quickstart (Linux amd64)

Supported setup: Debian 13 (trixie) Linux amd64, Python **3.13.5** (`python3=3.13.5-1`) and `qemu-system-aarch64` **10.0.13** (`qemu-system-arm=1:10.0.13+ds-0+deb13u1`). On a fresh Debian 13 host, check the available candidates with `apt-cache policy python3 qemu-system-arm`. If those exact package versions are available, explicitly install them yourself with `sudo apt update` and `sudo apt install python3=3.13.5-1 qemu-system-arm=1:10.0.13+ds-0+deb13u1`. If the versions are unavailable, stop rather than substituting another release. The repository never elevates privileges or silently installs packages. Other versions and distributions are unsupported until tested and the lock updated. QEMU is a host-side tool, not a Timeless guest dependency.

From the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/qemu_lab.py preflight
python3 scripts/qemu_lab.py inspect --output /path/to/new/board.dtb
python3 scripts/qemu_lab.py run --image /path/to/future/j1-kernel.img
```

`preflight` prints observed tool versions and VM parameters. With the stock manifest and no override, it requires the running executables to match Debian's `/usr/bin/python3` and `/usr/bin/qemu-system-aarch64` and checks the installed package revisions; an explicit `--qemu-bin` or custom manifest skips that package-level check and labels the result accordingly. `inspect` generates a DTB and digest and exits; it does **not** boot an OS. Until J1 supplies an image, `run` fails clearly and nonzero. Output paths should be outside the repository; do not commit generated DTBs or traces of private data. Use only trusted local inputs: `-nic none` and TCG do **not** sandbox the QEMU host process. `inspect` refuses existing outputs (including dangling symlinks) and paths containing QEMU's comma option separator. On a host without matching tools, preflight must fail nonzero; this is a diagnostic, not a successful laboratory verification. These CLI commands were also executed inside a newly bootstrapped Debian 13 amd64 rootfs with APT-installed exact package versions (same physical host, isolated userspace); see [evidence.md](evidence.md). Direct installation on an independently provisioned second host was not exercised.

The test matrix is [test-matrix.md](test-matrix.md). A measured baseline does not exist yet; the procedure is [docs/measurement.md](../../docs/measurement.md). The boot and CLI contract is [contracts/laboratory.md](contracts/laboratory.md). No QEMU result implies phone performance or compatibility.
