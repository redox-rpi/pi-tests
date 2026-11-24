#!/usr/bin/env python3
"""Unprivileged ICMP echo (SOCK_DGRAM, needs ping_group_range): pyping.py HOST COUNT"""
import socket, struct, sys, time
host, n = sys.argv[1], int(sys.argv[2]); s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP); s.settimeout(1.0)
got = 0
for seq in range(1, n + 1):
    pkt = struct.pack("!BBHHH", 8, 0, 0, 0, seq) + b"pitest-icmp"; t0 = time.time(); s.sendto(pkt, (host, 0))
    try:
        while True:
            d, _ = s.recvfrom(1024)
            if d[0] == 0 and struct.unpack("!H", d[6:8])[0] == seq:
                got += 1; print(f"reply seq={seq} time={(time.time()-t0)*1000:.2f} ms"); break
    except socket.timeout: print(f"no reply seq={seq}")
    time.sleep(max(0, 1 - (time.time() - t0)))
print(f"{n} packets transmitted, {got} received, {100*(n-got)/n:.0f}% packet loss")
