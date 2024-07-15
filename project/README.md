<<<<<<< HEAD
# Solutions
Boaz Yaari's repository for solutions to the WIS python course
=======
## Background

This program is based on research presented in the paper "RNA stores tau reversibly in complex coacervates" (Zhang et al., 2017). The study found that tau protein can bind to tRNA, particularly in stress conditions, potentially affecting protein synthesis. The scoring system in this program aims to identify transcripts that may be susceptible to translation issues due to lack of tRNA availability that results from tau (NFT) binding in Alzheimer's Disease.

# Codon Analyzer

Codon Analyzer is a Python program designed to analyze the human transcriptome for potential translation stalling, stopping or mistranslation related to tRNA availability. It downloads transcriptome data, processes coding sequences (CDS), and scores them based on codon usage to identify transcripts that may experience stalled, stopped, or mistranslated protein synthesis.

## Features

- Download the complete human transcriptome or a subset based on gene IDs
- Convert transcripts to coding sequences (CDS)
- Score CDS based on codon usage
- Identify transcripts with potential translation issues
- Graphical user interface for easy interaction

## Usage

1. Run the main script:
python main.py

2. Use the graphical interface to:
- Download or load transcriptome data
- Convert transcripts to CDS or load CDSs
- Set scoring parameters
- Analyze sequences
- View and save results

4. Since large lists of transcripts take time to download
-Save each stage as CSV for later usage

5. Logging and debugging
-The program is still relatively unstable, for this purpose we added a logging feature. Be sure to use this log when trying to understand what needs to be changed.

## Parameters of the chain scoring
Since the user is looking for different parameters for a "chain" it's important to understand what these "chains" are. 
Chains are made up of repeats of specific codons, stretches where they appear in certain amounts.
-Minimum initial stretch: the minimum number of codons from the scoring table to be present in sequence for the program to start the chain counting process
-Maximum gap: the maximum length of codons not from the table in sequence after a stretch (can be a fraction of the length of the initial stretch)
-Minimum Secondary Stretch: The minimum length for a stretch so that the chain continues counting after a gap (can be a fraction of the length of the initial stretch)
-Minimum overall codons: the minimum number of codons from the table to be present in the overall chain for it to appear in the scoring results

## Dependencies

This project uses the following Python standard library modules:
- csv: for reading and writing CSV files
- logging: for error logging and debugging
- re: for regular expression operations
- os: for operating system dependent functionality
- sys: for system-specific parameters and functions
- json: for JSON data handling
- time: for time-related functions

External libraries required are listed in `requirements.txt`.
>>>>>>> origin/project
