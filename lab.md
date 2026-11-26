# Lab

The test hardware of redox-rpi and how to use it. The build host is
**The build host** (Linux, x86_64), on the same LAN as the boards. It is the
TFTP and HTTP server for network boot, and it records the Pi's serial
console. Everything here is on a private LAN; nothing is reachable from the
internet.

## Boards

| Board | Use | How it boots | Notes |
|---|---|---|---|
| Raspberry Pi 3B+ (rev `0x00a020d3`, 1 GiB) | the test Pi: every automated row and most person tests | network boot from the build host (`/srv/tftp/redox`), through the boot selector card (since 2026-11-10, [#313](reports/313.md): our serial monitor as `bootcode.bin`; Enter within 5 s keeps it open, otherwise it chains Broadcom's code; `bootcode-broadcom.bin` on the card is the way back); or an SD card for card tests | LAN7800 Ethernet, IP <Pi 3B+>, devsh on port 2323 in test images; serial console on the build host; HDMI to the NanoKVM |
| Raspberry Pi Zero 2 W | second board, release checks | SD card (`--zero2w` images) | network through a USB hub with an RTL8153 adapter; tested from the card for v0.4.0-rc2 (row 286) |
| Raspberry Pi 400 | Pi 400 rows (port work, [#311](https://github.com/redox-rpi/redox-rpi/issues/311)), automated and person tests | EEPROM network boot: firmware and `config.txt` from `/srv/tftp/pi400-fw/`, Redox from `/srv/tftp/pi400/`; serial console on its own port (`serial-pi400.log`) | U-Boot in `pi400-fw` is the #394 fix (main 61536688, patches/u-boot 0001–0003) since 2026-11-24 ([report 622](reports/622.md): 20 of 20 boots without a stop); the old one is `u-boot.bin.pre622`. A USB mouse stays plugged in since 2026-11-24 19:44 UTC (for #710/#711): until that fix is in, images without it can have `usbhubd` panic at boot (`Failed to address device … port 1.1`) and xhcid can block other USB control requests after the mouse's stall, so check keyboard/USB lines in Pi 400 rows. EEPROM BOOT_ORDER is SD first: a bootable card in the slot replaces `pi400-fw` (report 363). Display rows need `hdmi_force_hotplug=1`, `hdmi_drive=2` (restore afterwards) |

## Power: Shelly plug

The Pi 3B+ is powered through a Shelly Plug S Gen3 (`<smart plug>`),
controlled over its HTTP RPC API from <build host>:

- Read: `curl -m 15 'http://<smart plug>/rpc/Switch.GetStatus?id=0'` (output, power in W). Anyone may read it.
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

The Pi 3B+'s serial console is on the 3B+ console port of the build host (115200 baud).
Use the port's fixed `/dev/serial/by-path/` name as the service uses it, never a bare
`ttyUSBn`: the numbers can swap when the host restarts.
The systemd user service `redox-serial.service` records everything to
`~/redox-rpi/logs/serial.log` and restarts by itself.

- **Read** from that file (`tail -f`, `tail -c`), never from the device: a
  second reader on the console port takes bytes away from the log.
- **Type** with `printf '...\r'` to the 3B+ console port, only after the new boot's
  `redox login:` has appeared, one character every 0.15 s. Keys sent
  earlier reach the bootloader.
- **Old output:** `redox-serial-rotate.timer` moves the log every night at
  03:17 UTC to `~/redox-rpi/logs/serial/serial-<date>.log.gz` and keeps 14
  days. Copy what a report needs into the report.

## Stable image

<!-- stable-image: written by scripts/update-stable.sh -->
Staged on the TFTP server whenever no test runs: `v0.7.0-dev-83-g2fb1c217+x27b9`, tested
2026-11-26 with `scripts/pi-test.py` ([report](reports/stable-2026-11-26.md), starts:
0 of 300 failed). A copy is in `/srv/tftp/backup-v0.7.0-dev-83-g2fb1c217+x27b9/`, and
`/srv/tftp/stable` points to it.
<!-- /stable-image -->

The stable image is the newest build of redox-rpi main that passed
`pi-test.py` in the nightly run. Restore it after a test:

```bash
cp -p /srv/tftp/stable/* /srv/tftp/redox/
```

then reset the Pi. Older stable images stay in `/srv/tftp/backup-<build ID>/`.

### Nightly update

**The Pi may reboot at night.** Every night at 03:30 UTC the build host runs
redox-rpi [`scripts/update-stable.sh`](https://github.com/redox-rpi/redox-rpi/blob/main/scripts/update-stable.sh)
(systemd user timer `redox-stable.timer`) from its clone `~/redox-rpi-stable`:

1. It stops if `patches/`, `config/`, `scripts/` and `tools/` on redox-rpi
   `origin/main` are unchanged since the stable image's commit, or if a row
   in [queue.md](queue.md) on this repository's main is marked **on the Pi**.
   A test that runs over night must be marked so, or `paused`. Keep
   03:15–04:15 UTC free of tests.
2. It builds redox-rpi `origin/main` with the options in
   [config/stable-image.conf](https://github.com/redox-rpi/redox-rpi/blob/main/config/stable-image.conf),
   stages it, resets the Pi and runs `scripts/pi-test.py`.
3. Pass: the image becomes the stable image. The script backs it up,
   updates the block above, writes the report to `reports/stable-<date>.md`
   and pushes both to this repository's main (clone `~/pi-tests-stable`).
4. Fail: the previous stable image is staged again, and the redox-rpi issue
   "Nightly: main fails on the Pi" (`topic:ci`, `needs:pi`) gets the build ID
   and the failing checks.

Logs: `~/redox-rpi/logs/stable/<date>.log` on the build host. Run it by hand
by marking its queue row N **on the Pi** and running
`scripts/update-stable.sh --force --taken N` (`--force`: build even without
changes; `--taken N`: row N is this run, any other test on the Pi still
stops it; `--no-push`: no push, no issue).

### Nightly visit images

Images for tests with a person at the Pi are built every night after the
stable image ([redox-rpi ci.md](https://github.com/redox-rpi/redox-rpi/blob/main/docs/topics/ci.md#nightly-visit-images)),
one per line in [config/visit-images.conf](https://github.com/redox-rpi/redox-rpi/blob/main/config/visit-images.conf).
A row that needs one writes "nightly visit `desktop`" (the image's name) in
its Image column instead of a build ID; http://<build host>:8080/visit/ then
lists the row with the image, so a tester at the Pi sees what to check.
Before the test, check that the image is OK and new enough, then stage it
like the stable image:

```bash
cat /srv/tftp/visit/status.txt /srv/tftp/visit/desktop/latest/visit.txt
cp -p /srv/tftp/visit/desktop/latest/redox/* /srv/tftp/redox/
```

Write the build ID from `/srv/tftp/visit/desktop/latest/BUILD_ID` into the
report. An image with `--sdcard` in the config is also on the image server
as family `redox-rpi-visit-<name>`; the tester flashes the newest build with
`sudo swiftflash redox:redox-rpi-visit-<name>`.

**SD images in a row:** publish them with redox-rpi `scripts/publish-sdcard.sh`
and write the SwiftFlash command it prints into the row, for example "For
the person: `sudo swiftflash redox:redox-rpi-openfw-3bp`" (the newest build
of that family), and the file name when the test needs exactly that build.

## Images

- Network images: `scripts/netboot.sh --server <host> --tftp-dir /srv/tftp --image <harddrive.img>`.
- SD card images for a person: http://<build host>:8080/sdcard/ or the image
  server (`sudo swiftflash redox:<family>`).
- Nightly visit images for person tests: http://<build host>:8080/visit/.
- Images and raw logs never go into this repository (see the
  [rules](README.md#rules)).
