import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data2.csv')

# Calculate IPC for each row
df['IPC'] = df['instructions'] / df['cpu-cycles']

# Plot IPC characteristics
plt.figure(figsize=(10, 6))
plt.plot(df['time'], df['IPC'], marker='o', linestyle='-', color='b', label='IPC')
plt.xlabel('Sample Index')
plt.ylabel('IPC (Instructions per Cycle)')
plt.title('IPC Characteristics Plot')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
