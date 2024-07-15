import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from scoring_system import ScoringSystem
from cds_converter import CDSConverter

class Analyzer:
    def __init__(self, cds_converter, scoring_system):
        self.results = []
        self.cds_converter = cds_converter
        self.scoring_system = scoring_system

    def create_parameter_widgets(self, parent):
        ttk.Label(parent, text="Minimum Initial Stretch:").grid(row=0, column=0, padx=5, pady=5)
        self.min_initial_stretch = ttk.Entry(parent, width=10)
        self.min_initial_stretch.grid(row=0, column=1, padx=5, pady=5)
        self.min_initial_stretch.insert(0, "4")

        ttk.Label(parent, text="Maximum Gap:").grid(row=1, column=0, padx=5, pady=5)
        self.max_gap = ttk.Entry(parent, width=10)
        self.max_gap.grid(row=1, column=1, padx=5, pady=5)
        self.max_gap.insert(0, "3")
        
        self.max_gap_type = tk.StringVar(value="value")
        ttk.Radiobutton(parent, text="Value", variable=self.max_gap_type, value="value").grid(row=1, column=2)
        ttk.Radiobutton(parent, text="Fraction of Initial Stretch", variable=self.max_gap_type, value="fraction").grid(row=1, column=3)

        ttk.Label(parent, text="Minimum Secondary Stretch:").grid(row=2, column=0, padx=5, pady=5)
        self.min_secondary_stretch = ttk.Entry(parent, width=10)
        self.min_secondary_stretch.grid(row=2, column=1, padx=5, pady=5)
        self.min_secondary_stretch.insert(0, "2")
        
        self.min_secondary_stretch_type = tk.StringVar(value="value")
        ttk.Radiobutton(parent, text="Value", variable=self.min_secondary_stretch_type, value="value").grid(row=2, column=2)
        ttk.Radiobutton(parent, text="Fraction of Previous Gap", variable=self.min_secondary_stretch_type, value="fraction").grid(row=2, column=3)

        ttk.Label(parent, text="Minimum Overall Codons:").grid(row=3, column=0, padx=5, pady=5)
        self.min_overall_codons = ttk.Entry(parent, width=10)
        self.min_overall_codons.grid(row=3, column=1, padx=5, pady=5)
        self.min_overall_codons.insert(0, "10")

        ttk.Button(parent, text="Run Analysis", command=self.run_analysis).grid(row=4, column=0, columnspan=2, pady=10)

    def run_analysis(self):
        try:
            min_initial_stretch = int(self.min_initial_stretch.get())
            max_gap = float(self.max_gap.get())
            min_secondary_stretch = float(self.min_secondary_stretch.get())
            min_overall_codons = int(self.min_overall_codons.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid parameter values")
            return

        self.results = []

        for cds in self.cds_converter.cds_data:
            codons = self.cds_converter.separate_into_codons(cds['cds_sequence'])
            chains = self.find_chains(codons, min_initial_stretch, max_gap, min_secondary_stretch, min_overall_codons)
            
            for chain in chains:
                chain_score = sum(self.scoring_system.scoring_table.get(codon, 0) for codon in chain['codons'])
                self.results.append({
                    'gene_name': cds['gene_name'],
                    'transcript_id': cds['transcript_id'],
                    'cds_id': cds['cds_id'],
                    'chain_id': f"{cds['cds_id']}_chain{len(self.results) + 1}",
                    'score': chain_score,
                    'codon_count': len(chain['codons']),
                    'stretch_count': chain['stretch_count'],
                    'gap_count': chain['gap_count'],
                    'sequence': ''.join(chain['codons'])
                })

        self.save_results()

    def find_chains(self, codons, min_initial_stretch, max_gap, min_secondary_stretch, min_overall_codons):
        chains = []
        i = 0
        while i < len(codons):
            chain = self.find_chain(codons[i:], min_initial_stretch, max_gap, min_secondary_stretch)
            if chain and len(chain['codons']) >= min_overall_codons:
                chains.append(chain)
                i += len(chain['codons'])
            else:
                i += 1
        return chains

    def find_chain(self, codons, min_initial_stretch, max_gap, min_secondary_stretch):
        chain = {'codons': [], 'stretch_count': 0, 'gap_count': 0}
        stretch = []
        gap = []
        previous_stretch_length = 0
        previous_gap_length = 0

        for codon in codons:
            if codon in self.scoring_system.scoring_table:
                if gap:
                    max_gap_value = max_gap if self.max_gap_type.get() == "value" else previous_stretch_length * max_gap
                    min_secondary_stretch_value = min_secondary_stretch if self.min_secondary_stretch_type.get() == "value" else previous_gap_length * min_secondary_stretch
                    
                    if len(gap) <= max_gap_value and len(stretch) >= min_secondary_stretch_value:
                        chain['codons'].extend(gap)
                        chain['codons'].extend(stretch)
                        chain['gap_count'] += 1
                        previous_gap_length = len(gap)
                    else:
                        break
                    gap = []
                stretch.append(codon)
            else:
                if stretch:
                    if len(stretch) >= min_initial_stretch:
                        chain['codons'].extend(stretch)
                        chain['stretch_count'] += 1
                        previous_stretch_length = len(stretch)
                        gap.append(codon)
                    else:
                        break
                    stretch = []
                elif gap:
                    gap.append(codon)
                    max_gap_value = max_gap if self.max_gap_type.get() == "value" else previous_stretch_length * max_gap
                    if len(gap) > max_gap_value:
                        break

        if stretch and len(stretch) >= min_initial_stretch:
            chain['codons'].extend(stretch)
            chain['stretch_count'] += 1

        return chain if chain['codons'] else None

    def save_results(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv")
        if filename:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Gene Name', 'Transcript ID', 'CDS ID', 'Chain ID', 'Score', 'Codon Count', 'Stretch Count', 'Gap Count', 'Sequence'])
                for result in self.results:
                    writer.writerow([
                        result['gene_name'],
                        result['transcript_id'],
                        result['cds_id'],
                        result['chain_id'],
                        result['score'],
                        result['codon_count'],
                        result['stretch_count'],
                        result['gap_count'],
                        result['sequence']
                    ])
            messagebox.showinfo("Info", "Results saved successfully")