import sys
import os
import csv
from datetime import datetime
from Bio import Entrez
import xml.etree.ElementTree as ET

Entrez.email = "boazayaari@gmail.com"#the email has been registered with NCBI as I was running into lots of problems

def search_input():
    if len(sys.argv) != 3:
        exit(f"Usage: {sys.argv[0]} TERM NUMBER")
    if not sys.argv[2].isnumeric():
        raise Exception("NUMBER needs to be a number")
    term = sys.argv[1]
    number_of_matches = int(sys.argv[2])
    return term, number_of_matches

def search_ncbi(term, number_of_matches):
    search = Entrez.esearch(db="snp", term=term, retmax=number_of_matches)
    record = Entrez.read(search)
    return record

def fetch_ncbi(record):
    data = []
    for Id in record["IdList"]:
        fetch = Entrez.efetch(db="snp", id=Id, rettype="docsum", retmode="xml")
        data.append(fetch.read())
    return data

def parse_snp_data(xml_data):
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
            
            print(f"Parsed SNP: {snp}")
            
            if snp['SNP_ID'] != 'N/A' or snp['GLOBAL_MAF'] != 'N/A' or snp['CHRPOS'] != 'N/A':
                snps.append(snp)
    
    return snps

def save_snp_data(snps, term):
    filename = f"{term}_snps.csv"
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['SNP_ID', 'GLOBAL_MAF', 'CHRPOS'])
        writer.writeheader()
        for snp in snps:
            if snp['SNP_ID'] != 'N/A' or snp['GLOBAL_MAF'] != 'N/A' or snp['CHRPOS'] != 'N/A':
                writer.writerow(snp)
                print(f"Saved SNP: {snp}")
            else:
                print(f"Skipped SNP with all fields as 'N/A': {snp}")
    
    print(f"Saved: {filename}")
    return filename

def csv_creator(term, number_of_matches, count):
    filename = 'search_metadata.csv'
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["date", "term", "max", "total"])
        writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), term, number_of_matches, count])

def main():
    term, number_of_matches = search_input()
    record = search_ncbi(term, number_of_matches)
    xml_data = fetch_ncbi(record)
    snps = parse_snp_data(xml_data)
    save_snp_data(snps, term)
    csv_creator(term, number_of_matches, record['Count'])

if __name__ == "__main__":
    main()

