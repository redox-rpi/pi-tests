# Test 656 rerun: homesync on PR #738's current head (#712)

**Result: pass.** Pi 3B+, network boot, 2026-11-27 13:50–13:52 UTC. Run with the user's own OK for the throwaway sshd on the build host.

Image `P-harddrive.img.gz`, `v0.7.0-dev-100-g1977ea28+x11c8` (main merged in, getsockname fix now as default relibc 0028), from `~/zrtl-q/p738-1977ea28/`; checksums OK. `run-homesync-pi.sh` is byte for byte the same as in the first run ([656](656.md)).

| Step | Result |
|---|---|
| Boot to `redox login:` | 41 s after reboot; experiments `homesync netstack-watch oom-test sshd` |
| `run-homesync-pi.sh` | exit 0, **21/21 pass**, `homesync Pi test: pass` |
| Pi key, plain `ssh … id` | refused (forced command) |
| Serial log | panic 0, RELIBC PANIC 0, UNHANDLED 0 |
| sshd of the script left | none; temporary folder removed |
| Afterwards | stable `v0.7.0-dev-83-g2fb1c217+x27b9` staged, `redox login:` at 13:52:31 |

## Times (devsh command time), first run in brackets

| Step | Time |
|---|---|
| setup 1 / setup 2 | 1.0 s / 0.8 s (1.0 / 0.8) |
| first push, 107 files 6.55 MB | 2.9 s (2.9) |
| push after a change / after a delete | 1.2 s / 1.1 s (1.2 / 1.1) |
| push of a 20 MiB file | **6.7 s** (6.8) |
| status | 1.1 s (1.2) |
| pull data, 99 files | 3.2 s (3.4) |

`commands.log`: the setup `mkdir`, one `id` (refused) and 6 `rsync --server` inside the server folder, nothing else.

Same side note as the first run: no timesync in the image, so backup folder names start with `1970-01-01-`.

Files: [656-rerun/result.txt](656-rerun/result.txt), [656-rerun/commands.log](656-rerun/commands.log), [656-rerun/sshd.log](656-rerun/sshd.log), [656-rerun/events.txt](656-rerun/events.txt) (addresses, user and temp folder names replaced).
