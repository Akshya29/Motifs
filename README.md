# Motifs
Motifs are short, recurring patterns in DNA, RNA, or protein sequences that serve as highly informative features for machine learning models in genomics. Often corresponding to transcription factor binding sites (TFBS), these motifs provide critical insights into where transcription factors bind and which genes may be regulated. In classification tasks, the presence or absence of specific motifs helps distinguish between genomic elements such as enhancers, promoters, and inactive regions. Models trained on motif-based features can therefore predict the functionality of a genomic region or determine whether it is bound by a transcription factor in experiments like ChIP-seq. In deep learning models, motifs frequently emerge as patterns captured by convolutional filters, offering a means to interpret what the model has learned and lending biological meaning to otherwise opaque predictions. Additionally, motif information plays a valuable role in predicting gene regulatory networks (GRNs) and enhancer-gene interactions, making it a powerful component in decoding complex regulatory landscapes.

# MEME Suite
MEME Suite is a collection of tools used to find and analyse motifs in sequences.
The tools include:
| Tool      | Function                                                                                                      |
|-----------|---------------------------------------------------------------------------------------------------------------|
| FIMO      | Scans sequences for motif matches and returns the location(s), p-value for each hit and the strand (+ or -)   |
| MEME      | Discovers motifs in a sequence. It returns the motif(s) it found, position weight matrix (PWM), E-values showing how significant the motifs are, and graphs showing the pattern in your sequences |
| TOMTOM    | Compares motifs to the database of known motifs (like JASPAR or TRANSFAC), aligns them, ranks matches based on similarity, and tells you which known motif is the closest match to yours, and how significant that match is |
| AME       | Take in a set of sequences (like promoters or enhancers) as input and a database of known motifs (like JASPAR). It then compares the frequency of each motif in your sequences vs a background and tells you which motifs are enriched, and gives you p-values for statistical significance |
| MEME-ChIP | Takes DNA sequences from ChIP-seq peaks (usually FASTA format) as input and performs multiple analyses such as; Motif discovery using MEME and DREME, motif enrichment using AME, motif comparison with Tomtom (matches your motifs to known ones), motif scanning using FIMO to find motif locations, and CentriMo to see if motifs are enriched at the center of peaks (typical for TF binding) |
| MAST      | A known motif file (from MEME, DREME, or another database like JASPAR) and a  FASTA file of sequences (like promoter regions, genes, etc.) are used as input. The tool then searches the sequences and finds matches to the motifs, and calculates E-values and p-values for how well the sequences match the motif model |
| XSTREME   | Is similar to MEME but more flexible. It discovers motifs in DNA, RNA, or protein sequences, searches for both known and new motifs, and works well even if motifs are not centrally located (like MEME-ChIP assumes) |


This page provides a guide on how to install and use tools from the MEME Suite, a powerful collection of bioinformatics tools for motif discovery and analysis. It also includes a basic Python script that reads motif sequences (from FIMO output) and scans promoter sequences to identify the locations of potential Transcription Factor Binding Sites (TFBS)

# References
Bailey TL, Johnson J, Grant CE, Noble WS. The MEME Suite. Nucleic Acids Res. 2015 Jul 1;43(W1):W39-49. doi: 10.1093/nar/gkv416. Epub 2015 May 7. PMID: 25953851; PMCID: PMC4489269.






