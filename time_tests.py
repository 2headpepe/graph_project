import pandas as pd
import time
from generator import create_random_graph
from edmond import edmonds_karp
from pre_flow import pre_flow

# Data to be collected
data = {
    "Vertices": [],
    "Edges": [],
    "Capacity": [],
    "Edmonds-Karp": [],
    "Preflow": []
}

U = [10, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000]

for n in range(10, 101, 10):
    for m_factor in range(10, 101, 10):
        m = int(n * (n - 1) / 2 * m_factor / 100)
        for u in U:
            edmonds_karp_times = []
            pre_flow_times = []
            for _ in range(50):
                graph = create_random_graph(n, m, u)

                start = time.time()
                ek_result = edmonds_karp(graph)
                finish = time.time()
                edmonds_karp_times.append(finish - start)

                start = time.time()
                pf_result = pre_flow(graph)
                finish = time.time()
                pre_flow_times.append(finish - start)

            avg_time_e = sum(edmonds_karp_times) / len(edmonds_karp_times)
            avg_time_f = sum(pre_flow_times) / len(pre_flow_times)

            data["Vertices"].append(n)
            data["Edges"].append(m)
            data["Capacity"].append(u)
            data["Edmonds-Karp"].append(avg_time_e)
            data["Preflow"].append(avg_time_f)

            print(f"V:{n}, E:{m}, U:{u}")
            print(f"Avg e:{avg_time_e}. Avg f:{avg_time_f}")

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
output_file_path = "graph_algorithms_results_10edges.xlsx"
df.to_excel(output_file_path, index=False)

print(f"Results saved to {output_file_path}")
