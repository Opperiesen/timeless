# Measurement protocol — no baseline yet

**Baseline status: not measured.** J0 has no Timeless guest image. DTB inspection and emulator startup do not measure boot completion, latency, stability or phone performance.

For a future J1/J2 run, archive (1) commit and exact host/guest versions plus machine args, (2) a scripted input scenario including warm-up and repetitions, (3) raw timestamped serial/input/display traces and exit status, (4) a versioned calculation method reporting distributions including tail latencies and stalls, (5) failures/timeouts as failures rather than omitted trials. Compare like-for-like runs on a fixed host and emulator; establish thresholds with Gabin only after observed baseline data. Do not use QEMU timings as proof of real-phone fluidity. Personal data and public networking remain excluded until a safety policy is ratified.

A future result without raw traces, environment and calculation method is **unverified**, not a baseline. Application-visible latency needs input-to-display observation; boot/serial output alone cannot substitute for it.
