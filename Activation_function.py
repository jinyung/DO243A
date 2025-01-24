import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def relu(x):
    return np.maximum(0, x)

def tanh(x):
    return np.tanh(x)

def softmax(x):
    exp_x = np.exp(x)
    return exp_x / exp_x.sum()

def main():
    st.title('Activation Function Transformations')
    
    # Activation function selection
    activation_function = st.selectbox(
        'Select Activation Function', 
        ['Softmax', 'Sigmoid', 'ReLU', 'Tanh']
    )
    
    # Data generation
    num_samples = st.slider('Number of Samples', 3, 10, 5)
    
    if st.button('Generate Random Data'):
        st.session_state.random_data = np.random.uniform(-3, 3, num_samples)
    
    # Ensure random data exists
    if 'random_data' not in st.session_state:
        st.session_state.random_data = np.random.uniform(-3, 3, num_samples)
    
    # Get current random data
    current_data = st.session_state.random_data
    
    # Apply transformation
    if activation_function == 'Softmax':
        transformed_data = softmax(current_data)
    elif activation_function == 'Sigmoid':
        transformed_data = sigmoid(current_data)
    elif activation_function == 'ReLU':
        transformed_data = relu(current_data)
    elif activation_function == 'Tanh':
        transformed_data = tanh(current_data)
    
    # Prepare data for animation
    df = []
    for i, (orig, trans) in enumerate(zip(current_data, transformed_data)):
        df.append({
            'input_index': f'x{i}',
            'value': orig,
            'state': 'Input',
            'frame': 1
        })
        df.append({
            'input_index': f'x{i}',
            'value': trans,
            'state': 'Output',
            'frame': 2
        })
    
    df = pd.DataFrame(df)
    
    # Create animated plot
    fig = px.bar(
        df, 
        x='input_index', 
        y='value', 
        color='state',
        animation_frame='frame',
        animation_group='input_index',
        range_y=[min(df['value']), max(df['value'])]
    )
    
    fig.update_layout(
        title=f'{activation_function} Transformation',
        xaxis_title='Input Index',
        yaxis_title='Values',
        legend_y=1.2,
        legend_x=0.8,
    )
    
    # Display Plotly chart
    st.plotly_chart(fig)
    
    # Display values
    col1, col2 = st.columns(2)
    with col1:
        st.write("Input Values:", current_data)
    with col2:
        st.write("Transformed Values:", transformed_data)
    
    # Function descriptions
    descriptions = {
        'Sigmoid': 'Maps input to a value between 0 and 1. Commonly used in binary classification.',
        'ReLU': 'Returns 0 for negative inputs and the input itself for positive inputs.',
        'Tanh': 'Maps input to a value between -1 and 1, zero-centered.',
        'Softmax': 'Converts input values to probabilities that sum to 1, used in multi-class classification.'
    }
    st.write(descriptions[activation_function])

if __name__ == '__main__':
    main()
    
    
    #-----
    
    
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# Define activation functions
def relu(x):
    return np.maximum(0, x)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def tanh(x):
    return np.tanh(x)

def softmax(x):
    exp_x = np.exp(x - np.max(x))  # Shift for numerical stability
    return exp_x / np.sum(exp_x)

# Streamlit app
def main():
    st.title("Activation Function Visualizer")

    # Sidebar options
    activation_functions = {
        "ReLU": relu,
        "Sigmoid": sigmoid,
        "Tanh": tanh,
        "Softmax": softmax,
    }
    activation_name = st.sidebar.selectbox("Select Activation Function", list(activation_functions.keys()))

    # Generate uniform data points
    x = np.linspace(-2, 2, 20)  # Generate 20 evenly spaced points between -2 and 2

    # Apply selected activation function
    activation_fn = activation_functions[activation_name]
    if activation_name == "Softmax":
        y = activation_fn(x)  # Softmax works on the entire array
    else:
        y = activation_fn(x)

    # Combined plot linking before and after transformation
    fig, ax = plt.subplots(figsize=(5, 10))  # Tall plot

    # Scatter plot showing before and after transformation
    ax.scatter(np.zeros_like(x), x, label="Before", color='blue', alpha=0.7)
    ax.scatter(np.ones_like(y), y, label="After", color='green', alpha=0.7)

    # Draw linking lines
    for i in range(len(x)):
        ax.plot([0, 1], [x[i], y[i]], color='gray', linestyle='--', alpha=0.5)

    ax.set_title(f"Before and After {activation_name} Transformation")
    ax.set_ylabel("Values")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Before", "After"])
    ax.legend()
    ax.grid(True)

    # Display the plot
    st.pyplot(fig)

if __name__ == "__main__":
    main()

