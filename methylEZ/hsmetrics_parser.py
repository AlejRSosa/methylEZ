import os
import glob
import pandas as pd

def parse_picard_output(directory, output_csv):
    """Parses Picard CollectHsMetrics output files and consolidates them into a CSV."""
    files = glob.glob(os.path.join(directory, "*_hs_metrics.txt"))
    data = []

    if not files:
        print("No Picard output files found.")
        return

    for file in files:
        sample_id = os.path.basename(file).replace("_hs_metrics.txt", "")
        with open(file, "r") as f:
            lines = f.readlines()
            try:
                start_idx = next(i for i, line in enumerate(lines) if "## METRICS CLASS" in line) + 1
                end_idx = next(i for i, line in enumerate(lines) if "## HISTOGRAM" in line)
                metrics = lines[start_idx:end_idx]
                if len(metrics) > 1:
                    data.append([sample_id] + metrics[1].strip().split("\t"))  # Skipping header
            except StopIteration:
                print(f"Skipping file {file}: Incorrect format.")
                continue

    df = pd.DataFrame(data)
    df.to_csv(output_csv, sep="\t", index=False)
    print(f"Parsed data saved to {output_csv}")