import sys
import pandas as pd

print("arguments", sys.argv)

day = int(sys.argv[1])
print(f"Running pipeline for day {day}")

# Create sample data
df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
print(df)

# Save to parquet
df.to_parquet(f"output_day_{day}.parquet")
print(f"Saved to output_day_{day}.parquet")