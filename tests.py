import os
import time
import pandas as pd
from reader import create_graph_from_file
from edmond import edmonds_karp
from pre_flow import pre_flow

directory_path = "tests"
files = os.listdir(directory_path)

# Initialize a dictionary to hold the results
results = {
    "Algorithm": [],
    "Test": [],
    "Time (seconds)": []
}

# =======================Edmonds-Karp=======================
for file in files:
    print(f'ek: test {file} in progress')
    graph = create_graph_from_file(directory_path + '/' + file)
    start = time.time()
    maxflow = edmonds_karp(graph)
    end = time.time()
    duration = end - start
    print(f'ek: test {file} complete. Time {duration}')

    # Store the results
    results["Algorithm"].append("Edmonds-Karp")
    results["Test"].append(file)
    results["Time (seconds)"].append(duration)

# =========================Pre-Flow=========================
for file in files:
    print(f'pf: test {file} in progress')
    graph = create_graph_from_file(directory_path + '/' + file)
    start = time.time()
    maxflow = pre_flow(graph)
    end = time.time()
    duration = end - start
    print(f'pf: test {file} complete. Time {duration}')

    # Store the results
    results["Algorithm"].append("Pre-Flow")
    results["Test"].append(file)
    results["Time (seconds)"].append(duration)

# Create a DataFrame from the results
df = pd.DataFrame(results)

# Pivot the DataFrame to get the desired format
df_pivot = df.pivot(index="Algorithm", columns="Test", values="Time (seconds)")

# Save the DataFrame to an Excel file
df_pivot.to_excel("test_results.xlsx")

print("Results saved to test_results.xlsx")
