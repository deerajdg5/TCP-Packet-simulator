import time
import random
from .packet import Packet
from .node import Node
import tkinter.messagebox as msg

class Network:
    def __init__(self, canvas, nodes):
        self.canvas = canvas
        self.nodes = nodes

    def get_path(self, src, dest):
        return [self.nodes[src], self.nodes["R1"], self.nodes[dest]]

    def simulate_packet_flow(self, src, dest, packet):
        path = self.get_path(src, dest)
        for i in range(len(path) - 1):
            a, b = path[i], path[i+1]
            self.animate_packet(a, b, packet)

            if random.random() < 0.1:
                packet.status = "Dropped"
                print(f"❌ Packet dropped between {a.name} → {b.name}")
                return False

            time.sleep(0.3)
            packet.ttl -= 1
            if packet.ttl <= 0:
                packet.status = "Expired"
                print(f"⚠️ TTL expired for packet {packet.seq}")
                return False

        self.nodes[dest].receive_packet(packet)
        packet.status = "Delivered"
        return True

    def animate_packet(self, node_a, node_b, packet):
        x1, y1 = node_a.x, node_a.y
        x2, y2 = node_b.x, node_b.y
        oval = self.canvas.create_oval(x1, y1, x1+20, y1+20, fill="skyblue")
        text = self.canvas.create_text(x1+10, y1-10, text=packet.flags)
        self.canvas.update()
        time.sleep(0.2)
        self.canvas.move(oval, x2 - x1, y2 - y1)
        self.canvas.move(text, x2 - x1, y2 - y1)
        self.canvas.update()
        self.canvas.delete(oval)
        self.canvas.delete(text)

    def simulate_handshake(self, src, dest):
        print("\n🔄 Starting TCP Handshake:")
        self.simulate_packet_flow(src, dest, Packet(src, dest, flags="SYN", packet_type="SYN"))
        self.simulate_packet_flow(dest, src, Packet(dest, src, flags="SYN-ACK", packet_type="ACK"))
        self.simulate_packet_flow(src, dest, Packet(src, dest, flags="ACK", packet_type="ACK"))

    def simulate_congestion_window(self, src, dest):
        print("\n📶 Simulating TCP Slow Start:")
        cwnd = 1
        while cwnd <= 8:
            for i in range(cwnd):
                pkt = Packet(src, dest, flags="DATA", seq=i+1, packet_type="DATA")
                self.simulate_packet_flow(src, dest, pkt)
            cwnd *= 2
            print(f"↑ cwnd increased to {cwnd}")

    def send_with_retransmission(self, src, dest, packet, max_retries=3):
        print(f"\n🔁 Sending with retransmission (max {max_retries} retries)")
        retries = 0
        while retries < max_retries:
            success = self.simulate_packet_flow(src, dest, packet)
            if success:
                print("✅ Packet delivered.")
                return
            retries += 1
            print(f"Attempt {retries}: Retrying...")
        print("❌ Packet delivery failed after retries.")

    def show_routing_table(self):
        table = "Routing Table:\n"
        for node in self.nodes:
            table += f"{node} → via R1\n"
        msg.showinfo("Routing Table", table)
