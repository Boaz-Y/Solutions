import logging
from pybiomart import Dataset
import pandas as pd
from tqdm import tqdm
import time
from requests.exceptions import RequestException
import csv
import tkinter as tk
from tkinter import filedialog, messagebox

# Configure logging
logging.basicConfig(filename='transcriptome_handler.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TranscriptomeHandler:
    def __init__(self):
        self.transcriptome = {}
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler('transcriptome_handler.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    #Comvert typical gene symbol format to ENSEMBL, otherwise you will have to pick the ENSEMBL ID manually
    def convert_gene_symbols_to_ensembl(self, gene_symbols):
        logger.info("Converting gene symbols to Ensembl Gene IDs")
        logger.info(f"Input gene symbols: {gene_symbols}")
        
        dataset = Dataset(name='hsapiens_gene_ensembl', host='http://www.ensembl.org')
        
        attributes = ['external_gene_name', 'ensembl_gene_id']
        filters = {'chromosome_name': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', 'X', 'Y', 'MT']}
        
        logger.info("Querying dataset")
        results = dataset.query(attributes=attributes, filters=filters)
        
        logger.info(f"Query results shape: {results.shape}")
        logger.info(f"Query results columns: {results.columns}")
        logger.info(f"First few rows of results:\n{results.head()}")
        
        # Use the correct column names from the results
        gene_name_col = 'Gene name'
        gene_id_col = 'Gene stable ID'
        
        gene_id_map = dict(zip(results[gene_name_col], results[gene_id_col]))
        
        converted_ids = [gene_id_map.get(symbol) for symbol in gene_symbols if gene_id_map.get(symbol)]
        logger.info(f"Converted IDs: {converted_ids}")
        
        return converted_ids

    def download_human_transcriptome(self, limit=None, gene_symbols=None, progress_callback=None):
        logger.info("Starting download of human transcriptome")
        logger.info(f"Limit: {limit}, Gene symbols: {gene_symbols}")
        
        dataset = Dataset(name='hsapiens_gene_ensembl', host='http://www.ensembl.org')

        # Print dataset info
        self.print_dataset_info()

        attributes = [
            'ensembl_transcript_id',
            'ensembl_gene_id',
            'external_gene_name',
            'transcript_biotype',
            'cdna'
        ]
        filters = {
            'transcript_biotype': 'protein_coding',
            'chromosome_name': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', 'X', 'Y', 'MT']
        }

        if gene_symbols:
            gene_ids = self.convert_gene_symbols_to_ensembl(gene_symbols)
            if gene_ids:
                filters['link_ensembl_gene_id'] = gene_ids
                logger.info(f"Using filter 'link_ensembl_gene_id' for gene IDs: {gene_ids}")

        logger.info(f"Query attributes: {attributes}")
        logger.info(f"Query filters: {filters}")

        logger.info("Querying the database")
        max_retries = 5
        retry_delay = 1

        for attempt in range(max_retries):#don't make the max too high, or the program will crash the computer
            try:
                logger.info(f"Attempt {attempt + 1} of {max_retries}")
                results = dataset.query(attributes=attributes, filters=filters)
                logger.info(f"Query returned {len(results)} results")
                break
            except RequestException as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Error occurred: {e}. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    logger.error(f"Failed to retrieve data after {max_retries} attempts.")
                    raise

        logger.info(f"Query results shape: {results.shape}")
        logger.info(f"Query results columns: {results.columns}")
        logger.info(f"First few rows of results:\n{results.head()}")

        # Map the column names to the expected names
        column_map = {
            'Transcript stable ID': 'ensembl_transcript_id',
            'Gene stable ID': 'ensembl_gene_id',
            'Gene name': 'external_gene_name',
            'Transcript type': 'transcript_biotype',
            'cDNA sequences': 'cdna'
        }
        results = results.rename(columns=column_map)

        if limit:
            logger.info(f"Limiting results to {limit}")
            results = results.head(limit)

        logger.info("Processing results")
        self.transcriptome = {}
        for i, row in tqdm(results.iterrows(), total=len(results), desc="Processing transcripts"):
            transcript_id = row.get('ensembl_transcript_id')
            if transcript_id and row['cdna'] and not pd.isna(row['cdna']):
                self.transcriptome[transcript_id] = {
                    'gene_id': row['ensembl_gene_id'],
                    'gene_name': row['external_gene_name'],
                    'biotype': row['transcript_biotype'],
                    'sequence': row['cdna']
                }
            if progress_callback:
                progress_callback(i + 1, len(results))

        logger.info(f"Downloaded {len(self.transcriptome)} protein-coding transcripts")

    def save_transcriptome(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv")
        if filename:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Transcript ID', 'Gene ID', 'Gene Name', 'Biotype', 'Sequence'])
                for transcript_id, data in self.transcriptome.items():
                    writer.writerow([transcript_id, data['gene_id'], data['gene_name'], data['biotype'], data['sequence']])
            messagebox.showinfo("Info", f"Transcriptome saved to {filename}")

    def load_existing_transcriptome(self):#preferred to save the transcriptome, so you don't have to keep re-downloading
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            self.transcriptome = {}
            with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.transcriptome[row['Transcript ID']] = {
                        'gene_id': row['Gene ID'],
                        'gene_name': row['Gene Name'],
                        'biotype': row['Biotype'],
                        'sequence': row['Sequence']
                    }
            messagebox.showinfo("Info", f"Loaded {len(self.transcriptome)} transcripts")

    def print_dataset_info(self):
        dataset = Dataset(name='hsapiens_gene_ensembl', host='http://www.ensembl.org')
        logger.info("Available filters:")
        for filter_name, filter_info in dataset.filters.items():
            logger.info(f"  {filter_name}: {filter_info}")
        logger.info("\nAvailable attributes:")
        for attr_name, attr_info in dataset.attributes.items():
            logger.info(f"  {attr_name}: {attr_info}")
