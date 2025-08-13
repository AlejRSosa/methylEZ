
#!/usr/bin/env python3
import os
import glob
import shutil

# Get the current directory (which contains the sample subdirectories)
base_dir = os.getcwd()

# Loop over each item in the base directory
for sample in sorted(os.listdir(base_dir)):
    sample_path = os.path.join(base_dir, sample)
    if not os.path.isdir(sample_path):
        continue  # Skip non-directories

    print(f"Processing sample: {sample}")

    # Find all files ending with _1.fq.gz and _2.fq.gz
    files1 = glob.glob(os.path.join(sample_path, "*_1.fq.gz"))
    files2 = glob.glob(os.path.join(sample_path, "*_2.fq.gz"))

    # Sort the lists to ensure a consistent order
    files1.sort()
    files2.sort()

    if len(files1) != 2:
        print(f"Warning: expected 2 files for _1 in {sample} but found {len(files1)}")
    if len(files2) != 2:
        print(f"Warning: expected 2 files for _2 in {sample} but found {len(files2)}")

    # Define the output file paths using the sample (directory) name as a prefix
    out_file1 = os.path.join(sample_path, f"{sample}_merged_1.fq.gz")
    out_file2 = os.path.join(sample_path, f"{sample}_merged_2.fq.gz")

    # Concatenate the _1 files
    with open(out_file1, "wb") as outfile:
        for file in files1:
            with open(file, "rb") as infile:
                shutil.copyfileobj(infile, outfile)

    # Concatenate the _2 files
    with open(out_file2, "wb") as outfile:
        for file in files2:
            with open(file, "rb") as infile:
                shutil.copyfileobj(infile, outfile)

    print(f"Created: {out_file1} and {out_file2}")

