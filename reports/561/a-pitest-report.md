
## 2026-11-21: `v0.6.0-dev-133-g9b1ce300+x2d42`

Built 2026-11-21T00:14:10Z, `libc.so` `5eb7f8c303980996…`, real Pi 3B+ over netboot. Experiments: `netstack-watch`, `rtl8152`, `timesync`.

| Check | Result | Detail |
|---|---|---|
| version | pass | v0.6.0-dev-133-g9b1ce300+x2d42 |
| manifest | pass | build ID and libc.so hash match manifest.toml |
| ps | pass | 59 processes (piped) |
| ps-tty | pass | 59 lines straight to the terminal, rc=0 |
| sdcard | pass | write, read back, delete on /scheme/data |
| audio | pass | mode pwm-dma, measured 44125 Hz, dma_faults 0, pwm_errors 0; tone -s 3 took 3.00 s, rc=0; audiod running |
| time | pass | set by NTP at 00:18:23 UTC; Pi clock -1 s against this host |
| tcp | pass | 10 MiB from the build host in 3.1 s, 3.2 MiB/s, SHA-256 matches |
| starts | pass | 0 of 300 failed |
| cpu | pass | ARM clock up to 1400 MHz, throttled 0x00000000 |
| reboot | **fail** | devsh did not answer within 120 s after reboot |
