import streamlit as st

# Genetic code dictionary
GENETIC_CODE = {
    'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
    'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
    'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
    'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
    'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
    'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
    'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
    'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
    'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
    'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
    'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
    'TAC': 'Y', 'TAT': 'Y', 'TAA': '*', 'TAG': '*',
    'TGC': 'C', 'TGT': 'C', 'TGA': '*', 'TGG': 'W',
}

def parse_fasta(content):
    sequences = {}
    current_id = None
    current_seq = []
    
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('>'):
            if current_id:
                sequences[current_id] = ''.join(current_seq)
            current_id = line[1:]
            current_seq = []
        else:
            current_seq.append(line)
    
    if current_id:
        sequences[current_id] = ''.join(current_seq)
    
    return sequences

def translate_dna(sequence):
    sequence = sequence.upper().replace('\n', '').replace(' ', '')
    protein = []
     
    # Translate codons to amino acids
    for i in range(0, len(sequence)-2, 3):
        codon = sequence[i:i+3]     
        amino_acid = GENETIC_CODE.get(codon, 'X')
        protein.append(amino_acid)
    
    return ''.join(protein)

# Set up the Streamlit interface
st.title("Translate DNA to protein sequences")
st.write("Upload a file or paste DNA sequences to translate them to protein sequences.")

# Create tabs for different input methods
tab1, tab2 = st.tabs(["Paste Sequence", "Upload File"])

# display module to be used in both module
def display_translation_results(sequences):
    # Check if sequences is in FASTA format
    if '>' in sequences:
        sequences = parse_fasta(sequences)
    else:
        # Treat as single sequence
        sequences = {'Sequence': sequences}
    
    # Create a text area to display all sequences in FASTA format
    st.subheader("Translation Results:")
    fasta_output = []
    for seq_id, dna in sequences.items():
        protein = translate_dna(dna)
        fasta_output.append(f">{seq_id}_protein")
        fasta_output.append(protein)
    
    # Join all sequences with newlines and display in a single text area
    fasta_text = "\n".join(fasta_output)
    st.text_area("", fasta_text, height=200)

    # Add download button
    st.download_button(
        label="Download FASTA file",
        data=fasta_text,
        file_name="translated_proteins.fasta",
        mime="text/plain"  # let browser know file type
    )

with tab1:
    use_sample = st.sidebar.checkbox("Use sample sequence", value=False)
    default_seq = ">sequence_1\nATGCCTAAGGTTAAATAAG\n>sequence_2\nATGGCTACTCAGGAGAGGT"
    sequences = st.text_area("Paste your sequence here (FASTA format or plain sequence):",  
        default_seq if use_sample else "", height=200)
    if st.button("Translate") and sequences:
        display_translation_results(sequences)

with tab2:     
    uploaded_file = st.file_uploader("Choose a file", type=None)  # Accept any file extension
    if uploaded_file:
        sequences = uploaded_file.read().decode('utf-8')
        display_translation_results(sequences)

# Add instructions
st.markdown("""
---
**Notes:**

**FASTA format example:**
```
>sequence_1
ATGCCTAAGGTTAAATAAG
>sequence_2
ATGGCTACTCAGGAGAGGT
```

**Plain sequence example:**
```
ATGCCTAAGGTTAAATAAG
```
""")