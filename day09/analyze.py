import argparse
from Bio import SeqIO
from Bio.Seq import Seq

def find_longest_duplicate_subsequence(seq):
    """
    Find the longest sub-sequence that appears twice in the sequence.
    """
    n = len(seq)
    longest_subseq = ""
    
    for length in range(n, 0, -1):
        seen = set()
        for start in range(n - length + 1):
            subseq = seq[start:start + length]
            if subseq in seen:
                return subseq
            seen.add(subseq)
    return longest_subseq

def find_cds(seq):
    """
    Identify the potential coding sequence (CDS) if a start and stop codon
    exist within the same frame. Translate the CDS to amino acids if found.
    """
    start_codon = "ATG"
    stop_codons = {"TAA", "TAG", "TGA"}
    seq = seq.upper()
    n = len(seq)
    
    for frame in range(3):
        for i in range(frame, n, 3):
            codon = seq[i:i+3]
            if codon == start_codon:
                for j in range(i, n, 3):
                    next_codon = seq[j:j+3]
                    if next_codon in stop_codons:
                        cds_seq = seq[i:j+3]
                        protein = str(Seq(cds_seq).translate())
                        return f"CDS: {cds_seq}, Protein: {protein}"
    return "Not a CDS"

def main(file, duplicate, cds):
    for record in SeqIO.parse(file, "fasta"):
        seq = str(record.seq)
        if duplicate:
            longest_dup = find_longest_duplicate_subsequence(seq)
            print(f"Longest duplicate sub-sequence: {longest_dup}")
        if cds:
            cds_result = find_cds(seq)
            print(cds_result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze DNA sequences from a FASTA file.")
    parser.add_argument("file", help="Path to the FASTA file")
    parser.add_argument("--duplicate", action="store_true", help="Find the longest duplicate sub-sequence")
    parser.add_argument("--cds", action="store_true", help="Find and translate potential CDS")

    args = parser.parse_args()
    main(args.file, args.duplicate, args.cds)
