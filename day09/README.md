# DNA Sequence Analyzer

This program analyzes DNA sequences from a FASTA file. It can perform two types of analyses:
1. Find the longest sub-sequence that appears twice.
2. Identify potential coding sequences (CDS) and translate them to amino acids.

## How to use
Write the following in your cmd terminal
```
python analyze.py file --duplicate --cds
```
file: Path to the FASTA file containing the DNA sequences.
--duplicate: (Optional) Find the longest duplicate sub-sequence.
--cds: (Optional) Find and translate potential CDS.

## Test sequences
You can use my troubleshooting files, 8 total, in FASTA format to test the program.