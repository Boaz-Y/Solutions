import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from transcriptome_handler import TranscriptomeHandler
from cds_converter import CDSConverter
from scoring_system import ScoringSystem
from analysis import Analyzer
import logging

logger = logging.getLogger(__name__)#For troubleshooting, will make a txt file with a log of the programs actions. 

class CodonAnalyzerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Codon Analyzer")
        master.geometry("800x600")

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.transcriptome_handler = TranscriptomeHandler()
        self.cds_converter = CDSConverter()
        self.scoring_system = ScoringSystem()
        self.analyzer = Analyzer(self.cds_converter, self.scoring_system)

        self.create_transcriptome_tab()
        self.create_cds_tab()
        self.create_scoring_tab()
        self.create_parameters_tab()
        self.create_results_tab()

    def create_transcriptome_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Transcriptome")

        # Download options
        ttk.Label(tab, text="Download Options:").pack(pady=(10, 5))
        
        # Limit number of transcripts, keep it low so that the computer doesn't crash
        ttk.Label(tab, text="Limit number of transcripts:").pack()
        self.limit_entry = ttk.Entry(tab, width=10)
        self.limit_entry.pack()

        # Gene list for non-entire transcriptome
        ttk.Label(tab, text="Gene list (comma-separated gene symbols):").pack()
        self.gene_list_entry = ttk.Entry(tab, width=50)
        self.gene_list_entry.pack()

        # Download button
        ttk.Button(tab, text="Download Human Protein-Coding Transcriptome", 
                   command=self.download_transcriptome).pack(pady=10)

        # Progress bar (relevant for large gene lists)
        self.progress_bar = ttk.Progressbar(tab, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=10)

        # Load existing transcriptome button
        ttk.Button(tab, text="Load Existing Transcriptome", 
                   command=self.transcriptome_handler.load_existing_transcriptome).pack(pady=10)

        # Save transcriptome button
        ttk.Button(tab, text="Save Transcriptome to CSV", 
                   command=self.transcriptome_handler.save_transcriptome).pack(pady=10)

        # Info text
        self.transcriptome_info = tk.Text(tab, height=10, width=60)
        self.transcriptome_info.pack(pady=10)

    def download_transcriptome(self):
        try:
            limit = int(self.limit_entry.get()) if self.limit_entry.get() else None
            gene_symbols = [gene.strip() for gene in self.gene_list_entry.get().split(',')] if self.gene_list_entry.get() else None

            self.progress_bar["value"] = 0
            self.master.update_idletasks()

            def update_progress(current, total):
                self.progress_bar["value"] = (current / total) * 100
                self.master.update_idletasks()

            self.transcriptome_handler.download_human_transcriptome(
                limit=limit, 
                gene_symbols=gene_symbols, 
                progress_callback=update_progress
            )

            self.transcriptome_info.delete('1.0', tk.END)
            self.transcriptome_info.insert(tk.END, f"Downloaded {len(self.transcriptome_handler.transcriptome)} protein-coding transcripts.")
        except Exception as e:
            logger.error(f"Error in download_transcriptome: {str(e)}")
            logger.exception("Exception details:")
            messagebox.showerror("Error", f"An error occurred: {str(e)}\nCheck the log file for more details.")

    def create_cds_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="CDS Conversion")

        ttk.Button(tab, text="Convert Transcripts to CDS", 
                   command=self.convert_to_cds).pack(pady=10)
        self.cds_info = tk.Text(tab, height=10, width=60)
        self.cds_info.pack(pady=10)

        ttk.Button(tab, text="Save CDS as CSV", 
                   command=self.save_cds_as_csv).pack(pady=10)

        # Add click buttons for CDS source selection
        self.cds_source = tk.StringVar(value="loaded_cds")
        ttk.Radiobutton(tab, text="Use Loaded CDS Table", 
                        variable=self.cds_source, value="loaded_cds").pack()
        ttk.Radiobutton(tab, text="Use Loaded CSV", 
                        variable=self.cds_source, value="loaded_csv").pack()
        
        # Add button to load CSV
        ttk.Button(tab, text="Load CDS from CSV", 
                   command=self.load_cds_from_csv).pack(pady=10)

    def convert_to_cds(self):
        if not self.transcriptome_handler.transcriptome:
            messagebox.showerror("Error", "No transcriptome data loaded. Please load or download transcriptome first.")
            return
        cds_data = self.cds_converter.convert_to_cds(self.transcriptome_handler.transcriptome)
        self.cds_info.delete('1.0', tk.END)
        self.cds_info.insert(tk.END, f"Converted {len(cds_data)} CDS sequences.")

    def save_cds_as_csv(self):
        if not self.cds_converter.cds_data:
            messagebox.showerror("Error", "No CDS data available. Please convert transcripts to CDS first.")
            return
        
        filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv")])
        if filename:
            self.cds_converter.save_cds_to_csv(filename)
            messagebox.showinfo("Success", f"CDS data saved to {filename}")

    def load_cds_from_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            cds_data = self.cds_converter.load_cds_from_csv(filename)
            self.cds_info.delete('1.0', tk.END)
            self.cds_info.insert(tk.END, f"Loaded {len(cds_data)} CDS sequences from CSV.")

    def create_scoring_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Scoring Table")

        self.scoring_system.create_widgets(tab)

    def create_parameters_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Chain Parameters")

        self.analyzer.create_parameter_widgets(tab)

    def create_results_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Scoring Results")

        self.results_text = tk.Text(tab, height=20, width=80)
        self.results_text.pack(pady=10)
        ttk.Button(tab, text="Save Results", command=self.analyzer.save_results).pack()
