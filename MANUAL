# MethylEZ User Manual

## 📦 Overview
MethylEZ is a graphical user interface (GUI) that streamlines the preprocessing and differential methylation analysis of bisulfite sequencing (BS-seq) data. The tool provides three main modules:

1. **nf-core/methylseq Preparation** – Manage FASTQ files and generate pipeline-ready samplesheets.
2. **Collect HsMetrics (Picard Tools)** – Calculate coverage metrics as an extra QC step. Bundles picard.
3. **DMR Analysis (methylKit Template)** – Generate a customizable R script for differential methylation analysis.

This manual describes how to use each module within the MethylEZ application.

---

## 🧬 1. nf-core/methylseq Preparation
### 📁 Goals
Organize FASTQ files and easily generate a usable samplesheet plus a vanilla command line for the `nf-core/methylseq` pipeline.

### 📝 How to Use
- Use the **Browse** button to add one or more FASTQ files.
- Specify whether each is paired- or single-end.
- Optionally, rename samples.
- Select the aligner (e.g., `bismark`, `bwa-meth`) and profile (`docker`, `singularity`, etc.).
- Choose where to save the output.
- Click **Generate Samplesheet**, **Generate Command**, or **Generate Both**.

### 📤 Output
- A CSV samplesheet
- A ready-to-run `nextflow` command (copy and paste in terminal to run, or integrate in SLURM script)

---

## 📊 2. Collect HsMetrics (Picard Tools)
### 📁 Goals
To generate a script to compute hybrid selection metrics from BAM files using Picard Tools CollectHSMetrics as an extra QC layer.

### 🧱 Components
#### Left Pane – Preparation (Optional)
- **Sort & Index FASTA**: Select your reference genome, sort it, and create an index and dictionary.
- **Sort & Index BAM**: Prepare BAM files.
- **BED to Interval List**: Convert BED files to interval lists with Picard.

#### Right Pane – Script Generator
- Choose folder containing BAM files.
- Browse and attach:
  - Target Intervals (.interval_list)
  - Bait Intervals (.interval_list)
  - Reference Dictionary (.dict)
- Click **Export Template Code** to generate a Python script.

### 📤 Output
- A customizable Python script that runs Picard's `CollectHsMetrics` across multiple BAM files.
- picard.jar requires >= Java 1.8 to run. Check README to learn how to navigate this.

---

## 🔬 3. DMR Analysis (R Template for methylKit)
### 📁 Goals
Generate an R script to perform differential methylation analysis using the `methylKit` package in R.

### 🧱 How to Use
- Fill in:
  - Base directory
  - BED file path for annotation
  - Genome assembly (e.g., `hg19`, `hg38`)
  - Filtering thresholds (min coverage, max percentile, SD cutoff)
  - Binning parameters (window size, step size)
  - Sample group recoding (e.g., `c("Control"=0, "Treatment"=1)`)
  - Column names for group, file, and sample ID
- Choose an output folder
- Click **Export R Template**

### 📤 Output
- A self-contained `.R` script with all settings customised, ready to be run in R.

---

## 🛠️ Notes & Tips
- MethylEZ does **not execute** the pipelines or scripts directly. Its main purpose is to prepare ready-to-use templates and commands.
- Always verify paths and parameters in the generated scripts before running them.
- Template outputs are readable and modifiable — feel free to adapt them.

---

## 📁 Files Generated
| Module             | Output File(s)                                |
|--------------------|-----------------------------------------------|
| nf-core Preparation| `samplesheet.csv`, `run_nfcore.sh`           |
| HsMetrics          | `run_hsmetrics.py`                            |
| DMR Analysis       | `methylkit_template.R`                        |

---

## 🧩 Requirements
- Python 3.8+
- Installed via pip or conda
- Optional (Linux): `samtools`, `java`, `Picard jar`, and R with required packages

---

## 💬 Support
For bug reports, suggestions, or contributions, visit:
https://github.com/AlejRSosa/methylEZ

---

Thank you for using MethylEZ! 🎉

