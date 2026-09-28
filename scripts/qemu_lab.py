#!/usr/bin/env python3
"""Host-side J0 QEMU laboratory; no Timeless guest image is provided."""
import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LOCK = Path(__file__).resolve().parents[1] / "config/toolchain.lock.json"


def machine_args(machine, dumpdtb=None):
    board = machine["type"] + ",dtb-randomness=off"
    if dumpdtb is not None:
        board += ",dumpdtb=" + str(dumpdtb)
    return ["-machine", board, "-cpu", machine["cpu"], "-smp", str(machine["cpus"]),
            "-m", str(machine["memory_mib"]) + "M", "-accel", machine["accelerator"],
            "-nographic", "-nic", "none", "-nodefaults", "-serial", "mon:stdio", "-no-reboot"]


def checked_tool(binary, lock):
    resolved = shutil.which(binary)
    if not resolved:
        raise ValueError("QEMU executable not found: " + binary)
    observed = subprocess.run([resolved, "--version"], capture_output=True, text=True, timeout=10, check=True).stdout
    match = re.search(r"QEMU emulator version (\d+\.\d+\.\d+)", observed)
    if not match or match.group(1) != lock["qemu"]["version"]:
        raise ValueError("QEMU version mismatch: " + observed.strip())
    listing = subprocess.run([resolved, "-machine", "help"], capture_output=True, text=True, timeout=10, check=True).stdout
    if not re.search(r"^" + re.escape(lock["machine"]["type"]) + r"\s", listing, re.MULTILINE):
        raise ValueError("QEMU machine unavailable: " + lock["machine"]["type"])
    return resolved, match.group(1)


def checked_debian_packages(lock):
    try:
        result = subprocess.run(
            ["dpkg-query", "-W", "-f=${binary:Package}\t${Version}\n", "python3", "qemu-system-arm"],
            capture_output=True, text=True, timeout=10, check=True)
    except (OSError, subprocess.SubprocessError) as error:
        raise ValueError("Pinned Debian packages unavailable: " + str(error)) from error
    installed = dict(line.split("\t", 1) for line in result.stdout.splitlines() if "\t" in line)
    expected = {"python3": lock["host"]["debian_package"],
                "qemu-system-arm": lock["qemu"]["debian_package"]}
    for name, version in expected.items():
        if installed.get(name) != version:
            raise ValueError("Debian package version mismatch: " + name +
                             " expected " + version + ", observed " + str(installed.get(name)))
    return installed


def require_packaged_tools(qemu_binary):
    for label, actual, packaged in (
        ("QEMU", qemu_binary, "/usr/bin/qemu-system-aarch64"),
        ("Python", sys.executable, "/usr/bin/python3"),
    ):
        try:
            matches = os.path.samefile(actual, packaged)
        except OSError:
            matches = False
        if not matches:
            raise ValueError(label + " executable does not match the packaged binary: " + str(actual))


def validate_manifest(lock):
    try:
        host, qemu, machine = lock["host"], lock["qemu"], lock["machine"]
        valid = (
            lock["schema_version"] == 1
            and all(isinstance(host[key], str) and host[key] for key in ("system", "machine", "python", "debian_package"))
            and all(isinstance(qemu[key], str) and qemu[key] for key in ("version", "debian_package", "executable"))
            and all(isinstance(machine[key], str) and machine[key] for key in ("type", "cpu"))
            and all(isinstance(machine[key], int) and not isinstance(machine[key], bool) and machine[key] > 0
                    for key in ("cpus", "memory_mib"))
            and machine["network"] == "none" and machine["accelerator"] == "tcg"
        )
    except (KeyError, TypeError):
        valid = False
    if not valid:
        raise ValueError("Invalid laboratory manifest")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["preflight", "inspect", "run"])
    parser.add_argument("--qemu-bin", help="Override the executable in the manifest")
    parser.add_argument("--manifest", type=Path, default=LOCK)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--image", type=Path)
    args = parser.parse_args()
    try:
        lock = json.loads(args.manifest.read_text())
        validate_manifest(lock)
        python_version = platform.python_version()
        if python_version != lock["host"]["python"]:
            raise ValueError("Python version mismatch: " + python_version)
        if platform.system() != lock["host"]["system"] or platform.machine() != lock["host"]["machine"]:
            raise ValueError("Unsupported host platform: " + platform.platform())
        binary, version = checked_tool(args.qemu_bin or lock["qemu"]["executable"], lock)
        stock = args.qemu_bin is None and args.manifest.resolve() == LOCK
        if stock:
            require_packaged_tools(binary)
        package_versions = checked_debian_packages(lock) if stock else None
        observed = {"qemu_version": version, "python_version": python_version,
                    "qemu_binary": binary, "machine": lock["machine"],
                    "arguments": machine_args(lock["machine"]),
                    "debian_packages": package_versions,
                    "package_verification": "verified" if package_versions is not None else "skipped (override/custom manifest)"}
        if args.command == "preflight":
            print(json.dumps(observed, indent=2))
            return 0
        if args.command == "inspect":
            if args.output is None:
                raise ValueError("inspect requires --output PATH")
            if "," in str(args.output):
                raise ValueError("Unsupported output path (QEMU option separator): " + str(args.output))
            if os.path.lexists(args.output):
                raise ValueError("Output already exists: " + str(args.output))
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix="qemu-inspect-", dir=args.output.parent) as directory:
                temporary_output = Path(directory) / "board.dtb"
                subprocess.run([binary, *machine_args(lock["machine"], temporary_output)],
                               check=True, timeout=30)
                data = temporary_output.read_bytes()
                if not data:
                    raise ValueError("QEMU produced an empty DTB")
                try:
                    os.link(temporary_output, args.output)
                except FileExistsError:
                    raise ValueError("Output already exists: " + str(args.output)) from None
                print(json.dumps({"dtb": str(args.output), "bytes": len(data),
                                  "sha256": hashlib.sha256(data).hexdigest(), **observed}, indent=2))
            return 0
        if args.image is None or not args.image.is_file() or args.image.stat().st_size == 0:
            raise ValueError("Kernel image missing or empty (J1 has not produced one): " + str(args.image))
        print("Starting QEMU; process startup is NOT proof of Timeless boot.", file=sys.stderr)
        return subprocess.call([binary, *machine_args(lock["machine"]), "-kernel", str(args.image)])
    except (OSError, ValueError, subprocess.SubprocessError, KeyError) as error:
        print("Laboratory error: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
