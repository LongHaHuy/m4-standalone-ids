import numpy as np
import pandas as pd

#Create random seed 
rng = np.random.default_rng(42)

def make_class(n, attack=False):
    if not attack:
        duration = rng.lognormal(0.0, 0.5, n)
        packets = rng.poisson(12, n) + 1
        byte_rate = rng.lognormal(7.0, 0.45, n)
        dst_port = rng.choice([80, 443, 53, 22], n, p=[.35, .45, .1, .1])
    else:
        duration = rng.lognormal(-0.3, 0.6, n)
        packets = rng.poisson(35, n) + 1
        byte_rate = rng.lognormal(8.0, 0.55, n)
        dst_port = rng.choice([22, 80, 443, 3389], n)
    
    src_rate = packets / np.maximum(duration, 1e-3) * rng.uniform(.45, .75, n)
    dst_rate = packets / np.maximum(duration, 1e-3) - src_rate
    total_bytes = byte_rate * duration
    mean_bytes = total_bytes / packets
    packet_ratio = rng.lognormal(0, 0.45, n)
    byte_ratio = rng.lognormal(0, 0.55, n)
    
    return pd.DataFrame({
      "duration_s": duration,
      "total_packets": packets,
      "total_bytes": total_bytes,
      "src_packet_rate": src_rate,
      "dst_packet_rate": dst_rate,
      "byte_rate": byte_rate,
      "mean_packet_bytes": mean_bytes,
      "packet_ratio": packet_ratio,
      "byte_ratio": byte_ratio,
      "dst_port": dst_port,
      "label": "SIM_ATTACK" if attack else "NORMAL"
    })

# Create 1000 samples NORMAL & SIM_ATTACK, combine and mix together
df = pd.concat([make_class(1000, False), make_class(1000, True)],
             ignore_index=True).sample(frac=1, random_state=42)

#Save data to .csv
df.to_csv("data/synthetic_ids.csv", index=False)

print("Kích thước dataset:", df.shape)
print("Số lượng các nhãn:")
print(df["label"].value_counts())