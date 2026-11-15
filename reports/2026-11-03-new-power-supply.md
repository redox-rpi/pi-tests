# New power supply (2026-11-03, Pi test agent)

The user put a new power supply on the Pi. The old one showed `throttled 0x50000`
in row 202 (under-voltage had happened).

- Stable `v0.4.0-dev-64-g954be33+x9f76` on the netboot card booted at 16:18 UTC and
  devsh answers. `throttled` 0x0 at idle (44 °C), after pi-test (all pass) and during
  2-core dd load (6 readings, peak 50 °C, plug 3.2 W).
- On the #205 direct-boot card (dev-36-g1107e5f7): `throttled` 0x0 at idle, after
  pi-test, at 10 readings during 5 min of dd on all 4 cores (peak 55.8 °C, plug 4.4 W),
  at 3 readings during 4 cores plus 3×50 MB of network output over devsh, and after
  the load.
- The image has no `netget`, so the download was replaced by output over devsh.
- **Result:** no under-voltage with the new supply. Details in the #205 report above.
