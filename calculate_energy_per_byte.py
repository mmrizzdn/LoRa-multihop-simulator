# Simulate max distance between two nodes
import pandas as pd
import os

from multihop.Packets import *
from multihop.config import settings
from multihop.Nodes import power_of_state, NodeState
from multihop.preambles import preambles

sizes = range(1, 255 - 7, 1)
energies = []
energies_per_byte = []

for size in sizes:
    # Fixed: Added settings as first argument, and proper values for all parameters
    # Arguments: settings, msg_type, hops, lqi, dst, src, own_data, own_data_created_at, src_node, forwarded_msgs
    p = Message(settings, MessageType.TYPE_ROUTED, 0, 0, 0, 1, [1] * size, 0, None, [])
    # Fixed: power_of_state requires settings as first argument
    energy = preambles[settings.LORA_SF][settings.MEASURE_INTERVAL_S] * power_of_state(settings, NodeState.STATE_PREAMBLE_TX) + p.time() * power_of_state(settings, NodeState.STATE_TX)
    energies.append(energy)
    energies_per_byte.append(energy/size)

df = pd.DataFrame({
    "size": sizes,
    "energy": energies,
    "energy_per_byte": energies_per_byte
})

os.makedirs("results", exist_ok=True)
filename = "./results/energy_per_byte_calculation.csv"
df.to_csv(filename, index=False)

print("The end")