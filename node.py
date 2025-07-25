class Node:
    def __init__(self, name, x, y, is_router=False):
        self.name = name
        self.x = x
        self.y = y
        self.is_router = is_router
        self.buffer = []

    def receive_packet(self, packet):
        self.buffer.append(packet)
        print(f"[{self.name}] Received packet: {packet}")
