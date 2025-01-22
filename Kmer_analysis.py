import streamlit as st
from collections import Counter
import plotly.express as px

st.title("K-mer Analysis")

# Input sequence
sequence = st.text_area("Enter your sequence:", 
"GATCACAGGTCTATCACCCTATTAACCACTCACGGGAGCTCTCCATGCATTTGGTATTTTCGTCTGGGGGGTATGCACGCGATAGCATTGCGAGACGCTGGAGCCGGAGCACCCTATGTCGCAGTATCTGTCTTTGATTC").upper()

# K-mer size
k = st.slider("Select k-mer size:", 2, 5, 3)

if sequence:
	# Generate k-mers using sliding window
	kmers = [sequence[i:i+k] for i in range(len(sequence)-k+1)]

	# Count k-mers
	kmer_counts = Counter(kmers)

	# Sort k-mers by frequency in descending order
	sorted_items = sorted(kmer_counts.items(), key=lambda x: x[1])
	kmers, counts = zip(*sorted_items)  # unzip  into two lists

	# Display results
	st.write(f"**Found {len(kmer_counts)} unique {k}-mers:**")

	# Dynamic bar chart height depending on kmers number
	dynamic_height = len(kmer_counts) * 20 + 100

	# Create bar chart
	fig = px.bar(
		x=counts,
		y=kmers,
		title=f"{k}-mer Frequencies",
		orientation='h',  # makes it horizontal
		labels={'x': 'Frequency', 'y': 'k-mer'},  # rename axes
		height=dynamic_height
	)

	st.plotly_chart(fig)