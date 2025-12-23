import time
from custom_csv import CustomCsvReader, CustomCsvWriter

read_file = "insurance_data.csv"
write_file = "benchmark_output.csv"

# ---- Benchmark Reading ----
start = time.time()
with open(read_file, "r", encoding="utf-8") as f:
    reader = CustomCsvReader(f)
    _ = list(reader)
read_time = time.time() - start

# ---- Benchmark Writing ----
rows = [
    ["PolicyID", "CustomerName", "PlanType", "Premium", "Notes"],
    ["201", "Test User", "Test Plan", "9999", "Benchmark test"]
]

start = time.time()
with open(write_file, "w", encoding="utf-8", newline="") as f:
    writer = CustomCsvWriter(f)
    writer.writerows(rows)
write_time = time.time() - start

print("---- CSV BENCHMARK RESULTS ----")
print(f"Read Time : {read_time:.6f} sec")
print(f"Write Time: {write_time:.6f} sec")
