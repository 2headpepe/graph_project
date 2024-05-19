import os
import time
from reader import create_graph_from_file
from edmond import edmonds_karp

directory_path = "tests"

files = os.listdir(directory_path)

with open("output.txt", "w") as output_file:
    for file in files:
        graph = create_graph_from_file(directory_path + '/' + file)
        start = time.time()
        maxflow = edmonds_karp(graph)
        end = time.time()
        output_file.write("Test " + file + "\n")
        output_file.write(file + " took " + str(end - start) + " seconds" + "\n")
        output_file.write(file + " maxflow is " + str(maxflow) + "\n")