class Packet:
    def __init__(self, src, dest, ttl=5, flags="SYN", seq=1, packet_type="DATA"):
        self.src = src
        self.dest = dest
        self.ttl = ttl
        self.flags = flags
        self.seq = seq
        self.packet_type = packet_type  # SYN, ACK, FIN, DATA
        self.status = "In Transit"

    def __str__(self):
        return f"{self.flags} | Seq: {self.seq} | TTL: {self.ttl}"
