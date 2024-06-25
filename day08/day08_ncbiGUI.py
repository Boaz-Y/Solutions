import sys
import os
import csv
from datetime import datetime
from Bio import Entrez
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk, messagebox

Entrez.email = "boazayaari@gmail.com"  # The email has been registered with NCBI

FORMAT_OPTIONS = {
    "nucleotide": ["GenBank", "FASTA", "Native", "DocSum"],
    "protein": ["GenPept", "FASTA", "Native", "DocSum"],
    "gene": ["GeneTable", "DocSum", "ASN.1"],
    "snp": ["DocSum", "XML", "ASN.1"]
}

class SNPDownloaderApp:
    def __init__(self, master):
        self.master = master
        master.title("SNP Downloader")

        self.label1 = tk.Label(master, text="Search Term:")
        self.label1.grid(row=0, column=0, padx=5, pady=5)

        self.search_term = tk.Entry(master)
        self.search_term.grid(row=0, column=1, padx=5, pady=5)

        self.label2 = tk.Label(master, text="Number of Records:")
        self.label2.grid(row=1, column=0, padx=5, pady=5)

        self.number_of_records = tk.Entry(master)
        self.number_of_records.grid(row=1, column=1, padx=5, pady=5)

        self.label3 = tk.Label(master, text="Database:")
        self.label3.grid(row=2, column=0, padx=5, pady=5)

        self.database = ttk.Combobox(master, values=list(FORMAT_OPTIONS.keys()))
        self.database.grid(row=2, column=1, padx=5, pady=5)
        self.database.set("snp")
        self.database.bind("<<ComboboxSelected>>", self.update_format_options)

        self.label4 = tk.Label(master, text="File Format:")
        self.label4.grid(row=3, column=0, padx=5, pady=5)

        self.file_format = ttk.Combobox(master)
        self.file_format.grid(row=3, column=1, padx=5, pady=5)
        self.update_format_options()

        self.download_button = tk.Button(master, text="Download Data", command=self.download_data)
        self.download_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def update_format_options(self, event=None):
        db = self.database.get()
        formats = FORMAT_OPTIONS.get(db, [])
        self.file_format['values'] = formats
        if formats:
            self.file_format.set(formats[0])
        else:
            self.file_format.set('')

    def download_data(self):
        term = self.search_term.get()
        number_of_matches = self.number_of_records.get()
        db = self.database.get()
        format_type = self.file_format.get().lower()

        if not number_of_matches.isnumeric():
            messagebox.showerror("Error", "Number of records must be a number")
            return

        number_of_matches = int(number_of_matches)
        
        try:
            record = self.search_ncbi(term, number_of_matches, db)
            xml_data = self.fetch_ncbi(record, db, format_type)
            snps = self.parse_snp_data(xml_data)
            self.save_snp_data(snps, term)
            self.csv_creator(term, number_of_matches, record['Count'])
            messagebox.showinfo("Success", f"Data downloaded and saved for term '{term}'")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_ncbi(self, term, number_of_matches, db):
        search = Entrez.esearch(db=db, term=term, retmax=number_of_matches)
        record = Entrez.read(search)
        return record

    def fetch_ncbi(self, record, db, format_type):
        data = []
        for Id in record["IdList"]:
            fetch = Entrez.efetch(db=db, id=Id, rettype="docsum", retmode="xml")
            data.append(fetch.read())
        return data

    def parse_snp_data(self, xml_data):
        snps = []
        for data in xml_data:
            root = ET.fromstring(data)
            for docsum in root.findall(".//DocumentSummary"):
                snp = {}

                snp_id_elem = docsum.find('SNP_ID')
                snp['SNP_ID'] = snp_id_elem.text if snp_id_elem is not None else 'N/A'

                global_maf_elem = docsum.find('GLOBAL_MAFS/MAF/FREQ')
                snp['GLOBAL_MAF'] = global_maf_elem.text.split('=')[1] if global_maf_elem is not None else 'N/A'

                chrpos_elem = docsum.find('CHRPOS')
                snp['CHRPOS'] = chrpos_elem.text if chrpos_elem is not None else 'N/A'

                if snp['SNP_ID'] != 'N/A' or snp['GLOBAL_MAF'] != 'N/A' or snp['CHRPOS'] != 'N/A':
                    snps.append(snp)

        return snps

    def save_snp_data(self, snps, term):
        filename = f"{term}_snps.csv"
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['SNP_ID', 'GLOBAL_MAF', 'CHRPOS'])
            writer.writeheader()
            for snp in snps:
                writer.writerow(snp)
        return filename

    def csv_creator(self, term, number_of_matches, count):
        filename = 'search_metadata.csv'
        file_exists = os.path.isfile(filename)
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["date", "term", "max", "total"])
            writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), term, number_of_matches, count])

if __name__ == "__main__":
    root = tk.Tk()
    app = SNPDownloaderApp(root)
    root.mainloop()
