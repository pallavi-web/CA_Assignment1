import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt

samples = {}
import sys
# while running this code pass path of perf_raw1.txt file as argument to clean that file and convert it to dataframe and get IPC graph.
with open(sys.argv[1]) as file:
    for line in file.readlines():
        if line.startswith('#') or line.strip() == '':
            continue
        fs = line.split()
        ts = float(fs[0])
        try:
            count = int(fs[1].replace(',',''))
        except:
            continue
        label = fs[2]

        if samples.get(label) is None:
            samples[label] = []
        samples[label].append((ts, count))

# print(samples)



# Convert dict into DataFrame
df = pd.DataFrame()

for label, values in samples.items():
    for ts, count in values:
        df.loc[ts, label] = count

# Reset index to get 'time' column
df = df.reset_index().rename(columns={'index': 'time'})

print(df)


# Compute IPC
df["IPC"] = df["instructions"] / df["cpu-cycles"]

# ---- Step 2: Cumulative instructions ----
df["cum_instructions"] = df["instructions"].cumsum()

# ---- Step 3: Define coarse phases of 100M instructions ----
interval_size = 100_000_000  # 100M
df["phase"] = df["cum_instructions"] // interval_size

# ---- Step 4: Compute IPC per phase ----
phase_ipc = df.groupby("phase").apply(
    lambda x: x["instructions"].sum() / x["cpu-cycles"].sum()
)

# ---- Step 5: Plot IPC ----
plt.figure(figsize=(12,6))
plt.plot(phase_ipc.index, phase_ipc.values, marker='o', linestyle='-')
plt.xlabel("Phase (100M instructions each)")
plt.ylabel("IPC")
plt.title("IPC across execution phases")
plt.grid(True)
plt.show()

# Save the parsed raw counter DataFrame to CSV for regression model
df.to_csv("perf_counters_intervals.csv", index=False)
print("Saved parsed counters to perf_counters_intervals.csv")