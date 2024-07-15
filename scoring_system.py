import tkinter as tk
from tkinter import ttk, filedialog
import csv

class ScoringSystem:
    def __init__(self):
        self.hek_scoring = {
            'TCG': 18.74, 'GTT': 25.57, 'GCT': 8.72, 'TAT': 7.9,
            'CCT': 7.38, 'CGT': 7.34, 'AGC': 7.25
        }
        self.ineuron_scoring = {
            'TCG': 18.36, 'TAT': 8.1, 'TTC': 4.9, 'CCG': 6.67, 'CAA': 2.86
        }
        self.scoring_table = self.hek_scoring.copy()

    def create_widgets(self, parent):
        ttk.Label(parent, text="Select Scoring System:").pack(pady=10)
        self.scoring_var = tk.StringVar(value="hek")
        ttk.Radiobutton(parent, text="HEK", variable=self.scoring_var, value="hek", command=self.update_scoring_table).pack()
        ttk.Radiobutton(parent, text="iNeuron", variable=self.scoring_var, value="ineuron", command=self.update_scoring_table).pack()
        ttk.Radiobutton(parent, text="Custom", variable=self.scoring_var, value="custom", command=self.update_scoring_table).pack()

        self.custom_frame = ttk.Frame(parent)
        self.custom_frame.pack(pady=10)
        ttk.Label(self.custom_frame, text="Codon:").grid(row=0, column=0)
        ttk.Label(self.custom_frame, text="Score:").grid(row=0, column=1)
        self.custom_codon = ttk.Entry(self.custom_frame, width=10)
        self.custom_codon.grid(row=1, column=0)
        self.custom_score = ttk.Entry(self.custom_frame, width=10)
        self.custom_score.grid(row=1, column=1)
        ttk.Button(self.custom_frame, text="Add", command=self.add_custom_score).grid(row=1, column=2)

        self.scoring_display = tk.Text(parent, height=10, width=30)
        self.scoring_display.pack(pady=10)

        ttk.Button(parent, text="Load Scoring Table", command=self.load_scoring_table).pack()

        self.update_scoring_display()

    def update_scoring_table(self):
        selected = self.scoring_var.get()
        if selected == "hek":
            self.scoring_table = self.hek_scoring.copy()
        elif selected == "ineuron":
            self.scoring_table = self.ineuron_scoring.copy()
        elif selected == "custom":
            self.scoring_table = {}
        self.update_scoring_display()

    def add_custom_score(self):
        codon = self.custom_codon.get().upper()
        score = self.custom_score.get()
        if len(codon) != 3 or not score.replace('.', '').isdigit():
            tk.messagebox.showerror("Error", "Invalid codon or score")
            return
        self.scoring_table[codon] = float(score)
        self.update_scoring_display()
        self.custom_codon.delete(0, tk.END)
        self.custom_score.delete(0, tk.END)

    def update_scoring_display(self):
        self.scoring_display.delete('1.0', tk.END)
        for codon, score in self.scoring_table.items():
            self.scoring_display.insert(tk.END, f"{codon}: {score}\n")

    def load_scoring_table(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                self.scoring_table = {row[0]: float(row[1]) for row in reader}
            self.scoring_var.set("custom")
            self.update_scoring_display()