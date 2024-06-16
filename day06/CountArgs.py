import csv
import argparse

def process_proteins(input_csv, output_csv):
    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        csvreader = csv.reader(infile)
        csvwriter = csv.writer(outfile)

        csvwriter.writerow(["protein_ID", 'Arginine_Count', 'AA_Count', 'Ratio'])

        next(csvreader)

        for row in csvreader:
            protein_ID, sequence = row
            arginine_count = sequence.count('R')
            aa_count = len(sequence)
            ratio = arginine_count / aa_count if aa_count > 0 else 0

            csvwriter.writerow([protein_ID, arginine_count, aa_count, ratio])

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process protein sequences to count arginines and compute ratios.")
    parser.add_argument("input_csv", help="Path to the input CSV file")
    parser.add_argument("output_csv", help="Path to the output CSV file")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    process_proteins(args.input_csv, args.output_csv)
