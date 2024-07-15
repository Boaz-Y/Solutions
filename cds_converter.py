import re
import csv

class CDSConverter:
    def __init__(self):
        self.cds_data = []

    def separate_into_codons(self, sequence):
        return [sequence[i:i+3] for i in range(0, len(sequence), 3)]
    
    def convert_to_cds(self, transcriptome):
        self.cds_data = []  # Reset cds_data before processing
        for transcript_id, data in transcriptome.items():
            sequence = data['sequence']
            cds_regions = self.find_all_cds(sequence)
            
            for cds_number, cds in enumerate(cds_regions, 1):
                codons = self.separate_into_codons(cds)
                self.cds_data.append({
                    'transcript_id': transcript_id,
                    'cds_id': f"{transcript_id}_CDS#{cds_number}",
                    'gene_name': data['gene_name'],
                    'gene_id': data['gene_id'],
                    'cds_length': len(cds),
                    'codon_count': len(codons),
                    'cds_sequence': cds
                })
        return self.cds_data

    def save_cds_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['transcript_id', 'cds_id', 'gene_name', 'gene_id', 'cds_length', 'codon_count', 'cds_sequence'])
            writer.writeheader()
            for cds in self.cds_data:
                writer.writerow(cds)

    def load_cds_from_csv(self, filename):
        self.cds_data = []
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.cds_data.append(row)
        return self.cds_data

    def find_all_cds(self, sequence):
        cds_regions = []
        start_codon = [m.start() for m in re.finditer('ATG', sequence)]
        stop_codons = ['TAA', 'TAG', 'TGA']
        
        for start in start_codon:
            for i in range(start, len(sequence), 3):
                codon = sequence[i:i+3]
                if codon in stop_codons:
                    cds = sequence[start:i+3]
                    if len(cds) % 3 == 0 and len(cds) >= 100:  # Minimum length filter
                        cds_regions.append(cds)
                    break
        
        return cds_regions

