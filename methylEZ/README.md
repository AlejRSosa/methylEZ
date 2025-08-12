# methylEZ

A GUI for methylation sequencing workflow.

## Install

```powershell
pip install .
```

Or directly from GitHub (requires a release with a source distribution):

```powershell
pip install git+https://github.com/AlejRSosa/methylEZ.git#subdirectory=methylEZ
```

## Run

Once installed, run:

```powershell
methylEZ
```

This launches the GUI.

## Requirements
- Python 3.9+
- Java (for Picard jar)
- samtools (on PATH)

Assets such as `picard.jar` are bundled under `methylEZ/assets/`.
