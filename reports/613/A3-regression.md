## Regression set (9 pass, 0 fail, 3 skip in 113 s)

| Check | Result | Detail |
|---|---|---|
| basics | PASS | 6 of 6 pass in 43 s |
| signals-stop | PASS | inputd 10, logd 2; after STOP/CONT: {'logd': '2', 'inputd': '10'}; /scheme/log line on the serial console |
| waitpid | PASS | WAITPID-OK status=7 |
| sig-pipe | SKIP | no /usr/share/sig-pipe/check.ion or no tcc (experiments sig-pipe, tcc) |
| scanf-pipe | SKIP | no /usr/share/scanf-pipe/check.ion or no tcc (experiments scanf-pipe, tcc) |
| tcc | PASS | 48.9 s; all 5 steps and TCC-TEST done; bench total 1468.2 ms; tcc.c built in 887 ms |
| dns | PASS | name server <router>; unknown names: nosuch-3ca559.invalid 0.06 s; nosuch-3ca559 0.06 s (limit 1 s) |
| launcher-sopwith | PASS | name=Sopwith, binary=/usr/bin/sopwith, icon=/usr/share/icons/hicolor/128x128/apps/sopwith.png; both exist |
| ifconfig-mac | PASS | ifconfig shows <mac>, as netstack has it |
| gamepad-console | SKIP | no gamepad-test (experiment gamepad-test) |
| tcp | PASS | 4 MiB from the build host in 2.3 s, 1.7 MiB/s, SHA-256 matches |
| serial | PASS | 0 bad lines; no pcid, no rtcd |

