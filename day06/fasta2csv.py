from Bio import SeqIO
import csv

fasta_file = "proteome.fasta"
csv_file = "proteome.csv"

with open(fasta_file) as fasta, open(csv_file, "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Protein_ID", "Sequence"])
    for record in SeqIO.parse(fasta, "fasta"):
        csvwriter.writerow([record.id, str(record.seq)])
