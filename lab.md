# Lab

The test hardware of redox-rpi and how to use it. The build host is
**homenodellm** (Linux, x86_64), on the same LAN as the boards. It is the
TFTP and HTTP server for network boot, and it records the Pi's serial
console. Everything here is on a private LAN; nothing is reachable from the
internet.

## Boards

| Board | Use | How it boots | Notes |
|---|---|---|---|
| Raspberry Pi 3B+ (rev `0x00a020d3`, 1 GiB) | the test Pi: every automated row and most person tests | network boot from homenodellm (`/srv/tftp/redox`), netboot card with the U-Boot boot menu; or an SD card for card tests | LAN7800 Ethernet, IP 192.168.178.148, devsh on port 2323 in test images; serial console on homenodellm; HDMI to the NanoKVM |
| Raspberry Pi Zero 2 W | second board, release checks | SD card (`--zero2w` images) | network through a USB hub with an RTL8153 adapter; tested from the card for v0.4.0-rc2 (row 286) |
| Raspberry Pi 400 | coming soon | | port work on the `pi400` branches ([#311](https://github.com/redox-rpi/redox-rpi/issues/311)); not on the test network yet |

## Power: Shelly plug

The Pi 3B+ is powered through a Shelly Plug S Gen3 (`shellyplug-01.fritz.box`),
controlled over its HTTP RPC API from homenodellm:

- Read: `curl -m 15 'http://shellyplug-01.fritz.box/rpc/Switch.GetStatus?id=0'` (output, power in W). Anyone may read it.
- Switch: `Switch.Set?id=0&on=false|true`. Only the Pi test agent switches
  it, to recover a hung Pi or for a test that needs a power cycle. Never
  switch it while a person works at the Pi.

A power-cycled Pi boots whatever is staged in `/srv/tftp/redox`.

## Screen: NanoKVM

The Pi's HDMI goes to a Sipeed NanoKVM on the LAN. It shows the Pi's screen
in a browser and can act as a USB keyboard and mouse if its USB cable is in
the Pi. A person signs in to it; sessions do not type its password. When
nothing is on HDMI, the firmware picks 656x416 (rows 291 and 294).

## Serial console

The Pi's serial console is on `/dev/ttyUSB0` of homenodellm (115200 baud).
The systemd user service `redox-serial.service` records everything to
`~/redox-rpi/logs/serial.log` and restarts by itself.

- **Read** from that file (`tail -f`, `tail -c`), never from the device: a
  second reader on `/dev/ttyUSB0` takes bytes away from the log.
- **Type** with `printf '...\r' > /dev/ttyUSB0`, only after the new boot's
  `redox login:` has appeared, one character every 0.15 s. Keys sent
  earlier reach the bootloader.
- **Old output:** `redox-serial-rotate.timer` moves the log every night at
  03:17 UTC to `~/redox-rpi/logs/serial/serial-<date>.log.gz` and keeps 14
  days. Copy what a report needs into the report.

## Stable image

Whenever no test runs, the stable image is staged in `/srv/tftp/redox`. It
is the newest build of redox-rpi main that passed `pi-test.py` in the
nightly run. `/srv/tftp/stable` points to its copy in
`/srv/tftp/backup-<build ID>/`. Restore it after a test:

```bash
cp -p /srv/tftp/stable/* /srv/tftp/redox/
```

then reset the Pi. The current build ID and the nightly's rules are in
redox-rpi [docs/test-plan.md, "Stable image"](https://github.com/redox-rpi/redox-rpi/blob/main/docs/test-plan.md#stable-image)
until the switch-over. Each nightly report is in `reports/stable-<date>.md`.

**The Pi may reboot at night.** At 03:30 UTC `scripts/update-stable.sh`
builds origin/main, stages it, resets the Pi and runs `pi-test.py`. It
skips the night if a row is marked **on the Pi**. Keep 03:15–04:15 UTC free
of tests, and mark a row that runs overnight **on the Pi** (or `paused`).

## Images

- Network images: `scripts/netboot.sh --server 192.168.178.120 --tftp-dir /srv/tftp --image <harddrive.img>`.
- SD card images for a person: http://homenodellm:8080/sdcard/ or the image
  server (`sudo swiftflash redox:<family>`).
- Nightly visit images for person tests: http://homenodellm:8080/visit/.
- Images and raw logs never go into this repository (see the
  [rules](README.md#rules)).
