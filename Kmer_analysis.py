import streamlit as st
from collections import Counter
import plotly.express as px

st.title("K-mer Analysis")

# get inputs
use_sample = st.sidebar.checkbox("Use sample sequence", value=True)
if use_sample:
	default = "GATCACAGGTCTATCACCCTATTAACCACTCACGGGAGCTCTCCATGCATTTGGTATTTTCGTC"
else:
	default = ""
sequence = st.text_area("Enter your sequence:", default).upper()
k = st.sidebar.slider("Select k-mer size:", 2, 5, 3)

if sequence:
	# compute, count and sort k-mers
	kmers = [sequence[i:i+k] for i in range(len(sequence)-k+1)]
	kmer_counts = Counter(kmers)
	sorted_items = sorted(kmer_counts.items(), key=lambda x: x[1])
	kmers, counts = zip(*sorted_items)  # unzip  into two lists
	
	# output
	st.success(f"Found {len(kmer_counts)} unique {k}-mers:")
	fig = px.bar(x=counts, y=kmers, title=f"{k}-mer Frequencies",
		labels={'x': 'Frequency', 'y': 'k-mer'}, 
		height=len(kmer_counts) * 20 + 100,  # dynamic height
		orientation = 'h'  # horizontal bar
	)
	st.plotly_chart(fig)
else:
	st.warning("Please enter sequence or use sample sequence")