# MethylEZ AI Coding Agent Instructions

## Project Overview
**methylEZ** is a Tkinter-based GUI application for bisulfite sequencing (WBGS/RRBS) workflow preparation and analysis. The application generates command-line templates and R scripts for bioinformatic pipelines, bundling Picard Tools and providing three main workflows: Methylseq preparation, HsMetrics collection, and DMR analysis.

## Architecture Pattern: Single-Container Frame Stack

The application uses a **container pattern** to manage navigation between GUI pages without creating/destroying widgets dynamically:

```
App (tk.Tk)
  └─ container (ttk.Frame) [single grid location (0,0)]
      ├─ MainMenu (ttk.Frame)
      ├─ MethylSeqGUI (Navigation)
      ├─ MainPicardGUI (Navigation)
      └─ DMRAnalysisGUI (Navigation)
```

- **Key file**: [methylEZ/main.py](methylEZ/main.py#L87-L103) - App class instantiates all pages once in `self.frames` dict
- **Navigation method**: `tkraise()` brings desired frame to front; pages are stacked at same grid position
- **State preservation**: Each page maintains its state (file lists, settings) when user navigates away and back
- **Back button mixin**: [methylEZ/navigation.py](methylEZ/navigation.py) - Navigation base class injects back button if callback provided

**Why**: Avoids widget duplication, keeps user selections persistent, improves performance on slower machines.

## Three Main Workflows

### 1. Methylseq Preparation (MethylSeqGUI)
**Files**: [methylEZ/gui.py](methylEZ/gui.py) (316 lines), [methylEZ/command_generator.py](methylEZ/command_generator.py)

Flow: File selection → Mark as single/paired-end → Custom sample naming → Generate samplesheet + command

**Key functions**:
- `generate_samplesheet()`: Parses FASTQ filenames (R1/R2 detection), groups by sample, builds CSV
- `generate_command()`: Constructs Nextflow command with aligner, genome, profile settings
- File management ([methylEZ/file_manager.py](methylEZ/file_manager.py)): Add/clear/reorder files in listbox

**R1/R2 Parsing Logic** (critical): Regex detects read markers (case-insensitive: r1/r2, R1/R2, _1/_2, -1/-2). Order-independent: matches first R1 and first R2 regardless of file order.

### 2. HsMetrics Collection (MainPicardGUI)
**Files**: [methylEZ/hsmetrics_main_gui.py](methylEZ/hsmetrics_main_gui.py), [methylEZ/hsmetrics_gui.py](methylEZ/hsmetrics_gui.py), [methylEZ/hsmetrics_command_generator.py](methylEZ/hsmetrics_command_generator.py)

Layout: Two-pane horizontal split - left pane (PicardPreparationFrame) + right pane (HSMetricsGUI)
Shared state: `output_dir` (StringVar) passed between both panes

Generates Picard CollectHsMetrics command for coverage analysis.

### 3. DMR Analysis (DMRAnalysisGUI)
**Files**: [methylEZ/dmr_gui.py](methylEZ/dmr_gui.py), [methylEZ/dmr_template_generator.py](methylEZ/dmr_template_generator.py)

Generates R/methylKit template for differential methylation region analysis. Configurable parameters: genome assembly, coverage thresholds, tile sizes, group recoding.

## Development Workflows

### Installation & Running Locally
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate        # Windows
source .venv/bin/activate     # Linux/macOS

# Install in editable mode (recommended for dev)
pip install -e .

# Run app
methylEZ
```

### Building & Distribution
```bash
# Build wheel/sdist
python -m build

# Install from wheel
pip install dist/methylEZ*.whl
```

**Entry point** ([setup.py](setup.py)): `methylEZ.main:main` callable function (not if __name__ == "__main__")

### Dependencies (No External Heavy Libs)
- **GUI**: tkinter (bundled), ttkthemes (aesthetic), click (CLI)
- **Data**: pandas (samplesheet), pyperclip (copy-to-clipboard), biopython
- **Bundled**: Picard.jar (MIT license) in assets/

**Note**: Tkinter must be present - installation instructions in [README.md](README.md) cover different OS requirements.

## Key Conventions & Patterns

### String Variables for GUI State
All user inputs stored as `tk.StringVar()`, `tk.IntVar()`, `tk.DoubleVar()` (not plain strings):
```python
self.aligner = tk.StringVar(value="bismark")
self.genome = tk.StringVar(value="GRCh37")
output = self.aligner.get()  # retrieve value
self.aligner.set("new_value")  # update
```

### Listbox ↔ List Sync
[methylEZ/file_manager.py](methylEZ/file_manager.py): When reordering files in Tkinter Listbox, **always sync underlying `self.file_paths` list**. Both must stay in same order.

### Exception Handling: messagebox Pattern
All user-facing errors use `messagebox.showerror()`, confirmations use `messagebox.askyesno()`:
```python
if not output_dir:
    messagebox.showerror("Error", "Output directory is not set.")
    return
```

### Asset Loading
Logo/images in [methylEZ/assets/](methylEZ/assets/) loaded via pathlib:
```python
current_dir = Path(__file__).resolve().parent
logo_path = current_dir / "assets" / "METHYLEZ_LOGO3.png"
```

## Cross-Component Data Flow

1. **File selection** (MethylSeqGUI) → stored in `self.file_paths` list
2. **Samplesheet generation** → pandas DataFrame → CSV export
3. **Command generation** → text concatenation → displayed in Text widget + clipboard
4. **State persistence** → each GUI page keeps references (`self.output_dir`, `self.sample_names`, `self.file_type`)

**Shared output_dir**: MainPicardGUI passes `tk.StringVar` to both child frames (PicardPreparationFrame + HSMetricsGUI) for coordinated output location.

## Testing Data
[TestData/](TestData/) folder contains sample FASTQ files for testing R1/R2 detection and file grouping logic.

## Common Modifications

- **Add new workflow**: Create new class inheriting `Navigation` in new file, add to [main.py](methylEZ/main.py) App.frames loop
- **Fix file parsing**: Modify regex patterns in `key_without_read()` and `read_of()` functions in [methylEZ/command_generator.py](methylEZ/command_generator.py#L15-L33)
- **Extend UI**: Frames use `pack()` geometry manager (not grid) in most pages; be consistent
- **Add validation**: Use `messagebox` + early return pattern before proceeding with operations
