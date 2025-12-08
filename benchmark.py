import time
import json
from custom_csv_reader import CustomCsvReader
from custom_csv_writer import CustomCsvWriter

# File paths
read_file = "insurance_data.csv"
write_file = "benchmark_output.csv"

# Initialize reader
reader = CustomCsvReader(read_file)

# --- BENCHMARK READING PERFORMANCE ---
start_time = time.time()
_ = reader.load_data()
read_time = time.time() - start_time

# --- BENCHMARK WRITING PERFORMANCE ---
rows_to_write = [
    ["PolicyID", "CustomerName", "PlanType", "Premium", "Notes"],
    ["201", "Test User", "Test Plan", "9999", "Benchmark writing test"]
]

start_time = time.time()
with open(write_file, "w", encoding="utf-8", newline="") as f:
    writer = CustomCsvWriter(f)
    writer.writerows(rows_to_write)
write_time = time.time() - start_time

# --- SHOW RESULTS IN TERMINAL ---
print("---- CSV BENCHMARK RESULTS ----")
print(f"Read Speed  : {read_time:.6f} seconds")
print(f"Write Speed : {write_time:.6f} seconds")

# --- SAVE RESULTS TO JSON FILE ---
results = {
    "read_time_seconds": read_time,
    "write_time_seconds": write_time
}

with open("benchmark_results.json", "w", encoding="utf-8") as json_file:
    json.dump(results, json_file, indent=4)

print("\nBenchmark results saved to benchmark_results.json")
