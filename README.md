# pi-tests

Test queue, test reports and test evidence of
[redox-rpi](https://github.com/redox-rpi/redox-rpi), Redox OS on the
Raspberry Pi. The code stays in redox-rpi: `scripts/pi-test.py`, the other
test scripts, `tools/` and [docs/testing.md](https://github.com/redox-rpi/redox-rpi/blob/main/docs/testing.md).
This repository holds what the tests found.

Owner: verification and validation (V&V, the Pi test agent). The coordinator
sets the order of the queue. The maintainer decided on 2026-11-09 (RFC 0002
phase 2) that V&V pushes to `main` here directly, without pull requests.

Since 2026-11-10 ([redox-rpi PR #318](https://github.com/redox-rpi/redox-rpi/pull/318))
this is the only test queue. redox-rpi `docs/test-plan.md` and
`docs/test-reports.md` point here, and the nightly stable run
(`scripts/update-stable.sh`) reads [queue.md](queue.md) and writes to
[lab.md](lab.md) and `reports/stable-<date>.md`.

## What is where

| File | What it holds |
|---|---|
| [queue.md](queue.md) | the rules for the test Pi, the open test rows, and the "Done" list with one line per result |
| [reports/](reports/) | one file per row, `reports/<row>.md` (for example [reports/292.md](reports/292.md)); nightly stable runs as `reports/stable-<date>.md`; everything before v0.4.0 development in [reports/archive-before-v0.4.0-dev.md](reports/archive-before-v0.4.0-dev.md) |
| [lab.md](lab.md) | the test hardware (Pi 3B+, Zero 2 W, Pi 400, Shelly plug, NanoKVM), the serial console and the stable image |
| [releases/](releases/) | the test evidence of each release, with build IDs, manifest hashes and commits, for example [releases/v0.4.0.md](releases/v0.4.0.md) |

Each release gets a tag here with the same name as in redox-rpi
(`v0.4.0`). The tag marks the state of the evidence when the release was
made.

## How to read a row

A row in [queue.md](queue.md) has these columns:

1. **Number.** Reports and commits name it, as in "#292". These numbers are
   test rows, not redox-rpi issues; links to issues and pull requests are
   written out in full.
2. **Purpose.** The milestone, the issue or requirement (`REQ-…`) that the
   row verifies, the steps with their exact commands, and what counts as
   pass.
3. **Owner.** The session or person who asked for the test and gets the result.
4. **Image.** The exact build ID and where the image and its manifest are on
   the build host.
5. **Needs.** For example network boot, the serial console, a person or a
   card swap.
6. **Status.** One of `waiting`, `ready`, **on the Pi**, `paused`,
   `superseded` or `replaced by #N`.

What a row and a report must contain is set in
[docs/process/test-standards.md](https://github.com/redox-rpi/redox-rpi/blob/main/docs/process/test-standards.md)
in redox-rpi: test levels, verdicts (pass, fail, flaky, open) and the rerun
rule.

## Rules

1. **Build ID and manifest.** Every result names the build ID read from the
   running Pi (`/etc/redox-rpi-release`), and the manifest it was checked
   against: its file name and the first 16 hex digits of its SHA-256.
   `pi-test.py --manifest` also checks the build ID and the `libc.so` hash.
2. **No images or binaries.** Images stay on the build host or the image
   server. A report names the path.
3. **Large logs stay on the build host.** Raw logs over about 1 MB stay on
   homenodellm under `~/pitest-tools/t<row>/`, and the report gives that
   path. Short excerpts go into the report.
4. **No secrets.** No passwords, tokens, Wi-Fi settings or keys, not even in
   a log excerpt. Check excerpts before you commit them.
5. **Plain English.** Reports start with the verdict and say what it means
   for the issue. A person's own observations are quoted as theirs.
6. **Commits** end with the `Co-Authored-By` line that the session's rules
   ask for.
