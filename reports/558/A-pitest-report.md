
## 2026-11-20: `v0.6.0-dev-123-gf68f4bc1+x2d42`

Built 2026-11-20T21:51:27Z, `libc.so` `ab934a66e0c35c30…`, real Pi 3B+ over netboot. Experiments: `netstack-watch`, `rtl8152`, `timesync`.

| Check | Result | Detail |
|---|---|---|
| version | pass | v0.6.0-dev-123-gf68f4bc1+x2d42 |
| manifest | pass | build ID and libc.so hash match manifest.toml |
| ps | pass | 58 processes (piped) |
| ps-tty | pass | 58 lines straight to the terminal, rc=0 |
| sdcard | pass | write, read back, delete on /scheme/data |
| audio | pass | mode pwm-dma, measured 44117 Hz, dma_faults 0, pwm_errors 0; tone -s 3 took 2.99 s, rc=0; audiod running |
| time | **fail** | no NTP answer yet (/tmp/timesync.synced missing): cat: /tmp/timesync.synced: No such file or directory; 1795211497 |
| tcp | pass | 10 MiB from the build host in 3.1 s, 3.2 MiB/s, SHA-256 matches |
| starts | pass | 0 of 300 failed |
| cpu | pass | ARM clock up to 1400 MHz, throttled 0x00000000 |
| reboot | pass | devsh back 36 s after reboot |
