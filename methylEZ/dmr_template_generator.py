import os
from tkinter import filedialog, messagebox

def export_metkit_template(self):
        """
        Exports a self-contained R template script for running differential methylation.
        The template contains inline code (no external dependencies).
        """
        template_code = '''
# methylKit analysis template
# Created by methylEZ
# This script is a template for running differential methylation analysis using methylKit.
# It includes user-configurable settings and example code for reading data, filtering, and analyzing DMRs.

# You can also modify the settings in the User Configurable Settings section as needed for your dataset.

# == 0. Install Required Packages ==
# If you haven’t already installed the following packages, uncomment and run:

# if (!require("BiocManager", quietly = TRUE))
#   install.packages("BiocManager")
# BiocManager::install(version = "3.21")

# required_pkgs <- c(
#   "openxlsx",
#   "methylKit",
#   "pheatmap",
#   "ComplexHeatmap",
#   "TxDb.Hsapiens.UCSC.hg19.knownGene",
#   "genomation",
#   "dplyr",
#   "annotatr",
#   "matrixStats"
# )

# installed <- rownames(installed.packages())
# for (pkg in required_pkgs) {
#   if (!pkg %in% installed) {
#     message("Installing ", pkg, " …")
#     BiocManager::install(pkg, ask = FALSE, update = FALSE)
#   }
# }
# 
# # Load libraries
# lapply(required_pkgs, library, character.only = TRUE)

# == 1. User Configurable Settings ==
# Base directory for your project
base_dir <- "{config['base_dir']}"  # <--- MODIFY

# Directories for data and results
data_dir     <- file.path(base_dir, "data")
analysis_dir <- file.path(base_dir, "analysis")
output_dir   <- file.path(base_dir, "results")

# Paths to sample sheets
samplesheet_path      <- file.path(data_dir, "samplesheet.csv")
full_samplesheet_path <- file.path(data_dir, "full_samplesheet.csv")

# Path to full genome BED file (for genomation annotation)
bedfile_path <- "{config['bedfile_path']}"  # <--- MODIFY

# Genome assembly (e.g., "hg19", "hg38")
genome_assembly <- "{config['genome_assembly']}"  # <--- MODIFY

# Thresholds for filtering
min_coverage <- {config['min_coverage']} # <--- MODIFY
max_coverage_percentile <- {config['max_coverage_percentile']} # <--- MODIFY
sd_cutoff <- {config['sd_cutoff']} # <--- MODIFY


# Binning parameters (region-level analysis)
tile_win_size  <- {config['tile_win_size']} # <--- MODIFY
tile_step_size <- {config['tile_step_size']} # <--- MODIFY


# Sample group recoding: named vector mapping original group names to numeric codes
# e.g., c("Control"=0, "TreatmentA"=1, "TreatmentB"=2)
# sample_group_recode <- c("Group1"=0, "Group2"=1, "Group3"=2)  
sample_group_recode <- {config['sample_group_recode']} # <--- MODIFY

# Column names in your samplesheet
group_column <- "{config['group_column']}" # <--- MODIFY
file_column  <- "{config['file_column']}" # <--- MODIFY
id_column    <- "{config['id_column']}" # <--- MODIFY


# Create output directory if it doesn't exist
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

# == 2. Load Required Libraries ==
library(openxlsx)
library(methylKit)
library(pheatmap)
library(ComplexHeatmap)
library(TxDb.Hsapiens.UCSC.hg19.knownGene)
library(genomation)
library(dplyr)
library(annotatr)
library(matrixStats)

# == 3. Read Sample Sheet and Prepare Sample Info ==
samples_df <- read.csv(samplesheet_path, header = TRUE, stringsAsFactors = FALSE)

# Recode sample groups to numeric treatment codes
samples_df$treatment <- unname(sample_group_recode[samples_df[[group_column]]])
samples_df <- subset(samples_df, !is.na(treatment))

# Prepare vectors for methRead
sample_ids   <- samples_df[[id_column]]
sample_files <- file.path(data_dir, samples_df[[file_column]])
treatment    <- samples_df$treatment

# == 4. Read Methylation Coverage Files ==
# Reads bismarkCoverage pipeline outputs (.cov or .cov.gz)
meth_obj <- methRead(location     = sample_files,
                     sample.id    = sample_ids,
                     assembly     = genome_assembly,
                     treatment    = treatment,
                     pipeline     = "bismarkCoverage",
                     header       = FALSE)

# == 5. Coverage and Methylation Statistics ==
# Plot coverage distributions for each sample
pdf(file.path(output_dir, "coverage_stats.pdf"))
for (i in seq_along(meth_obj)) {
  getCoverageStats(meth_obj[[i]], plot = TRUE)
}
dev.off()

# Plot methylation percentage distributions
pdf(file.path(output_dir, "methylation_stats.pdf"))
for (i in seq_along(meth_obj)) {
  getMethylationStats(meth_obj[[i]], plot = TRUE, both.strands = FALSE)
}
dev.off()

# == 6. Filtering and Normalization ==
filtered_obj   <- filterByCoverage(meth_obj,
                                  lo.count = min_coverage,
                                  hi.percent = max_coverage_percentile)
normalized_obj <- normalizeCoverage(filtered_obj)

# == 7. Unite Samples ==
# Combine all samples into one object at base-pair resolution
meth_united <- methylKit::unite(normalized_obj, destrand = FALSE)
meth_data    <- getData(meth_united)

# == 8. Outlier Filtering by Standard Deviation ==
# Calculate per-CpG methylation percentages and their SD
pm  <- percMethylation(meth_united)
sds <- matrixStats::rowSds(pm)

pdf(file.path(output_dir, "sd_distribution.pdf"))
hist(sds, breaks = 100,
     main = "SD of Methylation Percentages",
     xlab = "Standard Deviation")
dev.off()

# Filter out CpGs with low variability
meth_filtered <- meth_united[sds > sd_cutoff]

# == 9. Exploratory Data Analysis ==
# Correlation scatterplot
pdf(file.path(output_dir, "correlation_scatter.pdf"))
getCorrelation(meth_filtered, plot = TRUE)
dev.off()

# Sample clustering dendrogram
pdf(file.path(output_dir, "dendrogram.pdf"))
clusterSamples(meth_filtered, dist = "correlation", method = "ward.D2", plot = TRUE)
dev.off()

# PCA plot
pdf(file.path(output_dir, "PCA_plot.pdf"))
methylKit::PCASamples(meth_filtered)
dev.off()

# == 10. Differential Methylation at Base Level ==
# For two-group comparison: omit 'groups' argument
# For multi-group comparison: define 'groups_vec' according to recoded treatments
# Example for multi-group:
# groups_vec <- unique(treatment)
# myDiff <- calculateDiffMeth(meth_filtered, groups = groups_vec, adjust = "BH")
myDiff <- calculateDiffMeth(meth_filtered, adjust = "BH")

# Volcano plot of differential methylation
pdf(file.path(output_dir, "volcano_plot.pdf"))
with(getData(myDiff), {
  plot(meth.diff, -log10(qvalue),
       pch = 16, cex = 0.8,
       main = "Volcano Plot",
       xlab = "Methylation Difference (%)",
       ylab = "-log10(q-value)")
  abline(v = 0, col = "red", lty = 2)
})
dev.off()

# Chromosome-level summary
pdf(file.path(output_dir, "diffMeth_per_chromosome.pdf"))
diffMethPerChr(myDiff)
dev.off()

# Export hyper- and hypo-methylated sites
hyper_sites <- getMethylDiff(myDiff, difference = 25, qvalue = 0.01, type = "hyper")
hypo_sites  <- getMethylDiff(myDiff, difference = 25, qvalue = 0.01, type = "hypo")
write.csv(getData(hyper_sites),
          file = file.path(output_dir, "hyper_methylated_sites.csv"),
          row.names = FALSE)
write.csv(getData(hypo_sites),
          file = file.path(output_dir, "hypo_methylated_sites.csv"),
          row.names = FALSE)

# == 11. Differential Methylation at Region Level (Bins) ==
# Define comparisons: named list with code pairs
comparisons <- list(
  Comparison1 = c(0, 1),
  Comparison2 = c(0, 2)
  # Add more as needed
)

region_results <- lapply(names(comparisons), function(comp_name) {
  groups <- comparisons[[comp_name]]
  sel_ids <- sample_ids[treatment %in% groups]
  sel_tr  <- treatment[treatment %in% groups]
  meth_sub <- reorganize(meth_filtered,
                        sample.ids = as.character(sel_ids),
                        treatment  = sel_tr)
  tiles <- tileMethylCounts(meth_sub,
                            win.size   = tile_win_size,
                            step.size  = tile_step_size,
                            cov.bases  = 1)
  dmr   <- calculateDiffMeth(tiles)
  df    <- getData(dmr)
  df$Comparison <- comp_name
  return(df)
})

region_df <- do.call(rbind, region_results)
write.csv(region_df,
          file = file.path(output_dir, "region_level_DMRs.csv"),
          row.names = FALSE)

# == 12. Annotation with annotatr ==
# Build annotations
annots_cpg       <- c(paste0(genome_assembly, "_cpgs"), paste0(genome_assembly, "_genes_intergenic"))
annots_promoters <- build_annotations(genome = genome_assembly, annotations = paste0(genome_assembly, "_genes_promoters"))[[paste0(genome_assembly, "_genes_promoters")]]
annots_enhancers <- build_annotations(genome = genome_assembly, annotations = paste0(genome_assembly, "_enhancers_fantom")]

annotate_and_save <- function(df, prefix) {
  gr <- as(df, "GRanges")
  seqlevelsStyle(gr) <- "UCSC"
  # Promoter annotation
  prom_annot <- annotate_regions(regions = gr,
                                 annotations = annots_promoters,
                                 ignore.strand = TRUE)
  write.csv(unique(prom_annot),
            file = file.path(output_dir, paste0(prefix, "_promoter_annot.csv")),
            row.names = FALSE)
  # Enhancer annotation
  enh_annot <- annotate_regions(regions = gr,
                                annotations = annots_enhancers,
                                ignore.strand = TRUE)
  write.csv(unique(enh_annot),
            file = file.path(output_dir, paste0(prefix, "_enhancer_annot.csv")),
            row.names = FALSE)
  # CpG annotation
  cpg_annot <- annotate_regions(regions = gr,
                                annotations = build_annotations(genome = genome_assembly, annotations = annots_cpg),
                                ignore.strand = TRUE)
  write.csv(unique(cpg_annot),
            file = file.path(output_dir, paste0(prefix, "_cpg_annot.csv")),
            row.names = FALSE)
}

# Example: annotate hypermethylated sites
annotate_and_save(hyper_sites, "hyper_sites")

# == 13. (Optional) Annotation with genomation ==
# Uncomment and modify the following to perform genomation-based annotation:
# txdb <- TxDb.Hsapiens.UCSC.hg19.knownGene
# genes <- genes(txdb)
# promoters <- promoters(genes, upstream = 1000, downstream = 1000)
# promoter_flanks <- flank(promoters, width = 2000)
# dmr_gr <- as(hyper_sites, "GRanges")
# anno_g <- annotateWithFeatureFlank(target = dmr_gr,
#                                    feature = promoters,
#                                    flank = promoter_flanks)
# write.csv(anno_g, file = file.path(output_dir, "hyper_sites_genomation_annot.csv"))

    '''
        # Where to save the file (ask user input)
        filename = filedialog.asksaveasfilename(title="Save Methylkit Template", defaultextension=".R",
                                                initialfile="methylkit_template.R")
        if filename:
            try:
                with open(filename, "w") as f:
                    f.write(template_code)
                messagebox.showinfo("Success", f"Template exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error writing file: {e}")
        else:
            messagebox.showinfo("Canceled", "No file selected.")