# from Bio import SeqIO
# import csv

# fasta_file = "C:\work\Boaz-Y.github.io\day06\proteome.fasta"
# csv_file = "proteome.csv"

# with open(fasta_file) as fasta, open(csv_file, "w", newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(["Protein_ID", "Sequence"])
#     for record in SeqIO.parse(fasta, "fasta"):
#         csvwriter.writerow([record.id, str(record.seq)])

import csv
import argparse
from Bio import SeqIO

def convert_fasta_to_csv(fasta_file, csv_file):
    with open(fasta_file) as fasta, open(csv_file, "w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Protein_ID", "Sequence"])
        for record in SeqIO.parse(fasta, "fasta"):
            csvwriter.writerow([record.id, str(record.seq)])

def parse_arguments():
    parser = argparse.ArgumentParser(description="Convert a FASTA file to a CSV file.")
    parser.add_argument("fasta_file", help="Path to the input FASTA file")
    parser.add_argument("csv_file", help="Path to the output CSV file")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    convert_fasta_to_csv(args.fasta_file, args.csv_file)
