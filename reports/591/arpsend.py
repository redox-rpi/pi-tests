#!/usr/bin/env python3
"""Row 591: stream to the Pi for N s, log send stalls > 0.5 s and TCP retransmits (TCP_INFO)."""
import socket, struct, sys, time
port, secs = int(sys.argv[1]), float(sys.argv[2])
srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); srv.bind(("", port)); srv.listen(1); srv.settimeout(120)
c, addr = srv.accept(); print(f"accepted at {time.strftime('%H:%M:%S')}", flush=True)
buf = b"x" * 65536; t0 = last = time.time(); total = 0; stalls = []; maxgap = 0
def retrans():
    ti = c.getsockopt(socket.IPPROTO_TCP, socket.TCP_INFO, 256); return struct.unpack_from("I", ti, 100)[0]
r0 = retrans(); sec = []; nsec = 1; sb = 0; sr = r0
while time.time() - t0 < secs:
    try: n = c.send(buf)
    except OSError as e: print("send error", e); break
    now = time.time(); g = now - last
    if g > 0.5: stalls.append((round(last - t0, 2), round(g, 2), retrans() - r0))
    maxgap = max(maxgap, g); last = now; total += n; sb += n
    if now - t0 >= nsec:
        r = retrans(); sec.append((nsec, sb, r - sr)); sr = r; sb = 0; nsec += 1
print(f"result: {total} bytes in {time.time()-t0:.1f} s ({total/(time.time()-t0)/1e6:.2f} MB/s), max gap {maxgap:.3f} s, {len(stalls)} send stalls > 0.5 s, retransmits {retrans()-r0}", flush=True)
for s in stalls: print(f"stall at {s[0]} s for {s[1]} s (retransmits so far {s[2]})")
print("per second: s bytes retransmits")
for x in sec: print(*x)
c.close()
