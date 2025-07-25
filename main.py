import tkinter as tk
from simulator.network import Network
from simulator.node import Node
from simulator.packet import Packet

def send_packet():
    pkt = Packet("A", "B", flags="DATA", seq=1)
    network.simulate_packet_flow("A", "B", pkt)

def retransmit_packet():
    pkt = Packet("A", "B", flags="DATA", seq=99)
    network.send_with_retransmission("A", "B", pkt)

def simulate_handshake():
    network.simulate_handshake("A", "B")

def simulate_congestion():
    network.simulate_congestion_window("A", "B")

# GUI Setup
root = tk.Tk()
root.title("🌐 Network Packet Simulator")
canvas = tk.Canvas(root, width=700, height=400, bg="white")
canvas.pack()

# Nodes
nodes = {
    "A": Node("A", 100, 200),
    "R1": Node("R1", 300, 200, is_router=True),
    "B": Node("B", 500, 200)
}

for node in nodes.values():
    canvas.create_oval(node.x, node.y, node.x+30, node.y+30, fill="red" if node.is_router else "green")
    canvas.create_text(node.x + 15, node.y + 45, text=node.name)

network = Network(canvas, nodes)

# Buttons
tk.Button(root, text="Send Packet", command=send_packet).pack(pady=5)
tk.Button(root, text="Retransmit Packet", command=retransmit_packet).pack(pady=5)
tk.Button(root, text="Simulate TCP Handshake", command=simulate_handshake).pack(pady=5)
tk.Button(root, text="Simulate Congestion", command=simulate_congestion).pack(pady=5)
tk.Button(root, text="Show Routing Table", command=network.show_routing_table).pack(pady=5)

root.mainloop()
