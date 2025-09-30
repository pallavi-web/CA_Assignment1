import re
import csv

def perf_to_csv(input_filename, output_filename):
    # Regex to parse each data line: time, counts, event_name
    line_regex = re.compile(r"""
        ^\s*([\d\.]+)           # time stamp (float)
        \s+([\d,]+)             # counts (with commas)
        \s+([a-zA-Z0-9\-]+)     # event name (no spaces)
    """, re.VERBOSE)

    data = {}
    times = set()

    with open(input_filename, 'r', encoding='utf-8') as f:
        for line in f:
            match = line_regex.match(line)
            if match:
                time_str, counts_str, event = match.groups()
                time = float(time_str)
                counts = int(counts_str.replace(',', ''))

                times.add(time)
                if time not in data:
                    data[time] = {}
                data[time][event] = counts

    times = sorted(times)
    all_events = sorted({event for t in times for event in data[t].keys()})

    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Header row
        writer.writerow(['time'] + all_events)
        # Data rows
        for t in times:
            row = [t]
            for event in all_events:
                row.append(data[t].get(event, ''))
            writer.writerow(row)

    print(f"Conversion done: {output_filename} created with {len(times)} rows.")

input_file = 'data2.txt'  # input file
output_file = 'data2.csv' # Output CSV file name
perf_to_csv(input_file, output_file)
