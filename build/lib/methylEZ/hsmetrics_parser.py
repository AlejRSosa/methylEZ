import os
import glob
import pandas as pd

def parse_picard_output(directory, output_csv):
    """
    Parses Picard CollectHsMetrics output files and consolidates them into a CSV.
    
    Write the header to the output CSV, ensuring that fields are tab-separated.
    Loop through all .txt files in the directory.
    Skip empty lines and avoid reprinting the header, make sure the output is tab-separated
    """
    files = glob.glob(os.path.join(directory, "*_hs_metrics.txt"))
    if not files:
        print("No Picard output files found.")
        return

    all_lines = []

    header_written = False
    for file in files:
        base = os.path.basename(file)
        # Remove the known suffix to get a sample ID
        sample_id = base[:-len("_hs_metrics.txt")] if base.endswith("_hs_metrics.txt") else os.path.splitext(base)[0]
        with open(file, "r") as f:
            lines = f.readlines()
        try:
            start_idx = next(i for i, line in enumerate(lines) if "## METRICS CLASS" in line) + 1
            end_idx = next(i for i, line in enumerate(lines) if "## HISTOGRAM" in line)
            metrics = lines[start_idx:end_idx]
            if not metrics or len(metrics) < 2:
                print(f"Skipping file {file}: Not enough data.")
                continue

            # If header not written, assume the first line of metrics is the header
            if not header_written:
                # Prepend a "SAMPLE_IDENTIFIER" column.
                header = "SAMPLE_IDENTIFIER" + "\t" + metrics[0].strip()
                all_lines.append(header)
                header_written = True

            # Process each line after the header, filtering out unwanted lines.
            for line in metrics[1:]:
                clean_line = line.strip()
                # If the line is empty or contains "BAIT_SET", skip it.
                if not clean_line or "BAIT_SET" in clean_line:
                    continue
                # Prepend sample identifier and append the line.
                all_lines.append(f"{sample_id}\t{clean_line}")
        except StopIteration:
            print(f"Skipping file {file}: Incorrect format.")
            continue

    # Write all_lines to the output CSV (tab-separated)
    with open(output_csv, "w") as f:
        f.write("\n".join(all_lines))
    print(f"Parsed data saved to {output_csv}")