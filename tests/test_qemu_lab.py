"""Contract tests for the J0 host-side laboratory."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from scripts import qemu_lab

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "qemu_lab.py"


class LaboratoryTests(unittest.TestCase):
    def invoke(self, *args, qemu=None):
        cmd = [sys.executable, str(CLI), *args]
        if qemu is not None:
            cmd += ["--qemu-bin", str(qemu)]
        return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)

    def test_missing_qemu_fails_visibly(self):
        result = self.invoke("preflight", qemu="/nonexistent/qemu-system-aarch64")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("QEMU executable not found", result.stderr)

    def test_wrong_qemu_version_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            fake = Path(directory) / "qemu"
            fake.write_text("#!/bin/sh\necho 'QEMU emulator version 9.2.0'\n")
            fake.chmod(0o755)
            result = self.invoke("preflight", qemu=fake)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("QEMU version mismatch", result.stderr)

    def test_debian_package_version_mismatch_is_rejected(self):
        lock = json.loads((ROOT / "config/toolchain.lock.json").read_text())
        observed = "python3\t3.13.5-1\nqemu-system-arm\t1:10.0.13+ds-0+deb13u2\n"
        with mock.patch.object(qemu_lab.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, observed)):
            with self.assertRaisesRegex(ValueError, "Debian package version mismatch: qemu-system-arm"):
                qemu_lab.checked_debian_packages(lock)

    def test_stock_preflight_rejects_path_shadowing_packaged_qemu(self):
        with tempfile.TemporaryDirectory() as directory:
            fake = Path(directory) / "qemu-system-aarch64"
            fake.write_text("#!/bin/sh\nif [ \"$1\" = '--version' ]; then echo 'QEMU emulator version 10.0.13'; else echo 'virt-10.0 QEMU ARM Virtual Machine'; fi\n")
            fake.chmod(0o755)
            result = subprocess.run(
                [sys.executable, str(CLI), "preflight"], cwd=ROOT,
                env={**os.environ, "PATH": directory + os.pathsep + os.environ.get("PATH", "")},
                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("QEMU executable does not match the packaged binary", result.stderr)

    def test_preflight_reports_pinned_machine_and_versions(self):
        with tempfile.TemporaryDirectory() as directory:
            fake = Path(directory) / "qemu"
            fake.write_text("#!/bin/sh\nif [ \"$1\" = '--version' ]; then echo 'QEMU emulator version 10.0.13'; else echo 'virt-10.0 QEMU ARM Virtual Machine'; fi\n")
            fake.chmod(0o755)
            result = self.invoke("preflight", qemu=fake)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["qemu_version"], "10.0.13")
        self.assertEqual(data["machine"]["type"], "virt-10.0")
        self.assertEqual(data["machine"]["network"], "none")
        self.assertIn("-nic", data["arguments"])
        self.assertEqual(data["arguments"][data["arguments"].index("-nic") + 1], "none")

    def test_repeated_preflight_preserves_source_and_returns_same_result(self):
        with tempfile.TemporaryDirectory() as directory:
            fake = Path(directory) / "qemu"
            fake.write_text("#!/bin/sh\nif [ \"$1\" = '--version' ]; then echo 'QEMU emulator version 10.0.13'; else echo 'virt-10.0 QEMU ARM Virtual Machine'; fi\n")
            fake.chmod(0o755)
            lock = ROOT / "config/toolchain.lock.json"
            before = lock.read_bytes()
            first = self.invoke("preflight", qemu=fake)
            second = self.invoke("preflight", qemu=fake)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(first.stdout, second.stdout)
            self.assertEqual(lock.read_bytes(), before)

    def test_missing_image_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            fake = Path(directory) / "qemu"
            fake.write_text("#!/bin/sh\nif [ \"$1\" = '--version' ]; then echo 'QEMU emulator version 10.0.13'; else echo 'virt-10.0 QEMU ARM Virtual Machine'; fi\n")
            fake.chmod(0o755)
            result = self.invoke("run", "--image", str(Path(directory) / "missing.img"), qemu=fake)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Kernel image missing", result.stderr)

    def test_custom_manifest_is_read_and_rejected_when_incompatible(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "lock.json"
            lock = json.loads((ROOT / "config/toolchain.lock.json").read_text())
            lock["qemu"]["version"] = "9.2.0"
            manifest.write_text(json.dumps(lock))
            fake = Path(directory) / "qemu"
            fake.write_text("#!/bin/sh\necho 'QEMU emulator version 10.0.13'\n")
            fake.chmod(0o755)
            result = self.invoke("preflight", "--manifest", str(manifest), qemu=fake)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("QEMU version mismatch", result.stderr)

    def test_missing_machine_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            fake = Path(directory) / "qemu"
            fake.write_text("#!/bin/sh\nif [ \"$1\" = '--version' ]; then echo 'QEMU emulator version 10.0.13'; else echo 'virt-9.2 Old'; fi\n")
            fake.chmod(0o755)
            result = self.invoke("preflight", qemu=fake)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("QEMU machine unavailable", result.stderr)

    def test_inspect_refuses_to_overwrite_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            fake = Path(directory) / "qemu"
            fake.write_text("#!/bin/sh\nif [ \"$1\" = '--version' ]; then echo 'QEMU emulator version 10.0.13'; else echo 'virt-10.0 QEMU ARM Virtual Machine'; fi\n")
            fake.chmod(0o755)
            output = Path(directory) / "board.dtb"
            output.write_bytes(b"original")
            result = self.invoke("inspect", "--output", str(output), qemu=fake)
            self.assertEqual(output.read_bytes(), b"original")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Output already exists", result.stderr)

    def test_inspect_refuses_dangling_symlink_without_touching_target(self):
        with tempfile.TemporaryDirectory() as directory:
            fake = Path(directory) / "qemu"
            fake.write_text("#!/bin/sh\nif [ \"$1\" = '--version' ]; then echo 'QEMU emulator version 10.0.13'; else echo 'virt-10.0 QEMU ARM Virtual Machine'; fi\n")
            fake.chmod(0o755)
            target = Path(directory) / "target"
            output = Path(directory) / "board.dtb"
            output.symlink_to(target)
            result = self.invoke("inspect", "--output", str(output), qemu=fake)
            self.assertTrue(output.is_symlink())
            self.assertFalse(target.exists())
        self.assertEqual(result.returncode, 2)
        self.assertIn("Output already exists", result.stderr)

    def test_inspect_rejects_qemu_option_separator_in_output_path(self):
        with tempfile.TemporaryDirectory() as directory:
            fake = Path(directory) / "qemu"
            fake.write_text("#!/bin/sh\nif [ \"$1\" = '--version' ]; then echo 'QEMU emulator version 10.0.13'; else echo 'virt-10.0 QEMU ARM Virtual Machine'; fi\n")
            fake.chmod(0o755)
            output = Path(directory) / "board.dtb,accel=kvm"
            result = self.invoke("inspect", "--output", str(output), qemu=fake)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Unsupported output path", result.stderr)

    def test_valid_image_uses_isolated_machine_arguments_without_boot_claim(self):
        with tempfile.TemporaryDirectory() as directory:
            fake = Path(directory) / "qemu"
            fake.write_text("#!/bin/sh\nif [ \"$1\" = '--version' ]; then echo 'QEMU emulator version 10.0.13'; elif [ \"$1\" = '-machine' ] && [ \"$2\" = 'help' ]; then echo 'virt-10.0 QEMU ARM Virtual Machine'; else printf '%s\\n' \"$@\"; fi\n")
            fake.chmod(0o755)
            image = Path(directory) / "j1.img"
            image.write_bytes(b"test image, not a real kernel")
            result = self.invoke("run", "--image", str(image), qemu=fake)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(),
                         ["-machine", "virt-10.0,dtb-randomness=off", "-cpu", "cortex-a53",
                          "-smp", "1", "-m", "256M", "-accel", "tcg", "-nographic",
                          "-nic", "none", "-nodefaults", "-serial", "mon:stdio",
                          "-no-reboot", "-kernel", str(image)])
        self.assertIn("NOT proof of Timeless boot", result.stderr)

    def test_python_version_mismatch_is_rejected_before_qemu(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "lock.json"
            lock = json.loads((ROOT / "config/toolchain.lock.json").read_text())
            lock["host"]["python"] = "0.0.0"
            manifest.write_text(json.dumps(lock))
            result = self.invoke("preflight", "--manifest", str(manifest), qemu="/nonexistent/qemu")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Python version mismatch", result.stderr)

    def test_manifest_rejects_empty_and_unsafe_machine_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "lock.json"
            lock = json.loads((ROOT / "config/toolchain.lock.json").read_text())
            lock["machine"]["cpu"] = ""
            lock["machine"]["network"] = "user"
            manifest.write_text(json.dumps(lock))
            result = self.invoke("preflight", "--manifest", str(manifest), qemu="/nonexistent/qemu")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Invalid laboratory manifest", result.stderr)

    def test_manifest_supplies_default_qemu_binary(self):
        with tempfile.TemporaryDirectory() as directory:
            fake = Path(directory) / "qemu"
            fake.write_text("#!/bin/sh\nif [ \"$1\" = '--version' ]; then echo 'QEMU emulator version 10.0.13'; else echo 'virt-10.0 QEMU ARM Virtual Machine'; fi\n")
            fake.chmod(0o755)
            manifest = Path(directory) / "lock.json"
            lock = json.loads((ROOT / "config/toolchain.lock.json").read_text())
            lock["qemu"]["executable"] = str(fake)
            manifest.write_text(json.dumps(lock))
            result = self.invoke("preflight", "--manifest", str(manifest))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["qemu_binary"], str(fake))
