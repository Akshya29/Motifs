# Load motifs
motifs_genome = pd.read_csv("fimo.tsv", sep='\t')
motifs = list(zip(motifs_genome["motif_id"].astype(str), motifs_genome["matched_sequence"].astype(str)))

# Load promoters
promoters_file = "promoter.txt"
promoters = []

# Read tthrough the sequences
with open(promoters_file, "r") as file:
    for record in SeqIO.parse(file, "fasta"):
        promoter_id = record.id
        promoter_sequence = str(record.seq)
        promoters.append((promoter_id, promoter_sequence))  

# Scan FASTA file for motif matches
for promoter_id, promoter_sequence in promoters:
    for motif_id, motif in motifs:
        start_pos = promoter_sequence.find(motif)
        while start_pos != -1:
            end_pos = start_pos + len(motif) - 1
            print(f"Promoter: {promoter_id} | Motif: {motif} | Motif ID: {motif_id} | Start: {start_pos+1} | End: {end_pos+1}")
            start_pos = promoter_sequence.find(motif, start_pos + 1)
