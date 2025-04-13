#load the fimo file derived from the MEME Suite
motifs = pd.read_csv("fimo.tsv",  sep='\t')
motifs = list(zip(motifs_genome["motif_id"].astype(str), motifs_genome["matched_sequence"].astype(str)))

#load the genome file
genome_file = Zea_mays_genome_trial.txt

# Read the entire file as a string
with open(genome_file, "r") as file:
    genome_data = file.read()

# Split the genome data into sequence records by identifying FASTA headers (lines starting with '>')
sequence_records = genome_data.split(">")

# Iterate through each sequence record
for record in sequence_records:
    if record.strip():  # Skip empty records
        # Split the header and sequence (e.g., "header\nsequence")
        lines = record.splitlines()
        header = lines[0]
        sequence = ''.join(lines[1:])  # Join the sequence lines into a single string

        # Search for motifs in the sequence
        for motif_id, motif in motifs:
            start_pos = sequence.find(motif)
            
            # If the motif is found in the sequence
            while start_pos != -1:
                end_pos = start_pos + len(motif) - 1  # Calculate the end position of the motif
                
                print(f"motif_sequence: {motif} | motif_id: {motif_id} | start: {start_pos+1} | end: {end_pos+1}")
                
                # Find the next occurrence of the motif
                start_pos = sequence.find(motif, start_pos + 1)
