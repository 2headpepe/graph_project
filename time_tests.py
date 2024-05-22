import time
from generator import create_random_graph
from edmond import edmonds_karp
from pre_flow import pre_flow

U = [10, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000]
edmond_data = []
flow_data = []

for n in range(10, 101, 10):
    for m_factor in range(25, 101, 25):
        m = int(n * (n - 1) / 2 * m_factor / 100)
        for u in U:
            edmonds_karp_times = []
            pre_flow_times = []
            for _ in range(50):
                graph = create_random_graph(n, m, u)

                start = time.time()
                edmonds_karp(graph)
                finish = time.time()
                diff = finish - start
                edmonds_karp_times.append(diff)

                start = time.time()
                pre_flow(graph)
                finish = time.time()
                diff = finish - start
                pre_flow_times.append(diff)

            avg_time_e = sum(edmonds_karp_times) / len(edmonds_karp_times)
            edmond_data.append((n, m, avg_time_e))

            avg_time_f = sum(pre_flow_times) / len(pre_flow_times)
            flow_data.append((n, m, avg_time_f))
            print(f"V:{n}, E:{m}, U:{u}")
            print(f"Avg e:{avg_time_e}. Avg f:{avg_time_f}")

