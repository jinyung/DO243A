import streamlit as st
import plotly.express as px
import random

def generate_toy_data(num_points=100, seed = 24601):
    random.seed(seed)
    toy = [random.normalvariate(0, 1) + 5 * (i/50 - 1)**2 for i in range(num_points)]
    return toy
    
def sliding_window_average(data, window_size):
    smoothed = []
    for i in range(len(data)):
        window = data[i:i + window_size]
        smoothed.append(sum(window) / len(window))
    return smoothed

# Set up the Streamlit interface
st.title("Sliding Window Average (1D)")

# User control
st.sidebar.header("Options")
use_toy_data = st.sidebar.checkbox('Use example data', value=True)
window_size = st.sidebar.slider('Window Size', 3, 21, 3, 2)

if use_toy_data:
    data = generate_toy_data()
else:
    data_input = st.text_area('Enter your numbers (one per line or comma-separated):')
    try:
        data = [float(x.strip()) for x in data_input.replace('\n', ',').split(',') if x.strip()]
    except:
        st.error('Invalid input. Please enter numbers.')

if data: 
    smoothed_data = sliding_window_average(data, window_size)

    # plot            
    plot_data = [{'index': i, 'value': val, 'type': 'Original'} for i, val in enumerate(data)
        ] + [{'index': i, 'value': val, 'type': 'Smoothed'} for i, val in enumerate(smoothed_data)]
        
    fig = px.line(plot_data, x='index', y='value', color='type', 
        title=f'Sliding Window Average (Window Size: {window_size})')
    st.plotly_chart(fig)