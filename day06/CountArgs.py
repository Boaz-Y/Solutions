import csv

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

input_csv_path = "proteome.csv"
output_csv_path = "analyzed_proteome.csv"

process_proteins(input_csv_path, output_csv_path)