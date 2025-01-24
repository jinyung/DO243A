import numpy as np
import streamlit as st
import plotly.graph_objects as go
from sklearn.datasets import make_blobs

def find_nearest_centroids(data, centroids):
    n_points = len(data)
    n_centroids = len(centroids)
    labels = np.zeros(n_points, dtype=int)
    
    # For each point, find the nearest centroid
    for i in range(n_points):
        min_distance = float('inf')
        # Calculate distance to each centroid
        for j in range(n_centroids):
            # Euclidean distance between point i and centroid j
            distance = np.sqrt(np.sum((data[i] - centroids[j])**2))
            # Update label if this centroid is closer
            if distance < min_distance:
                min_distance = distance
                labels[i] = j
    return labels

def update_centroids(data, labels, k):
    new_centroids = np.array([data[labels == i].mean(axis=0) for i in range(k)])
    return new_centroids

def kmeans(data, k):
    data = np.array(data)
    centroids = data[np.random.choice(len(data), k, replace=False)]
    centroid_history = [centroids.copy()]
    label_history = []

    while True:
        # Step 1: Assign points to the nearest centroid
        labels = find_nearest_centroids(data, centroids)
        label_history.append(labels.copy())
        
        # Step 2: Update centroids
        new_centroids = update_centroids(data, labels, k)
        if np.allclose(new_centroids, centroids):
            break
        centroids = new_centroids
        centroid_history.append(centroids.copy())

    return centroid_history, label_history

st.title("Visualize K-means clustering iterations")

# Sidebar for user inputs
st.sidebar.header("Data generation and K-means parameters")
n_samples = st.sidebar.slider("Number of samples", 100, 1000, 300, step = 50)
k = st.sidebar.slider("Number of K-Means Clusters (k)", 2, 10, 5)
n_clusters = st.sidebar.slider("Number of True Clusters", 2, 10, 5)
cluster_std = st.sidebar.slider("Cluster dispersion", 1, 3, 2)

# Generate data using sklearn make_blobs
np.random.seed(24601)  # setting global random number, important!
data, _ = make_blobs(n_samples=n_samples, centers=n_clusters, cluster_std=cluster_std, 
    random_state=24601)

# Run K-Means and get history of centroids and labels
centroid_history, label_history = kmeans(data, k=k)

# Slider for iteration selection
iteration = st.slider("Iteration", 0, len(label_history) - 1, 0)
current_centroids = centroid_history[iteration]
current_labels = label_history[iteration]

# Plot using Plotly
fig = go.Figure()

# Generate unique colors for each cluster
colors = [f"hsl({i * 360 / max(n_clusters, k)}, 70%, 50%)" for i in range(max(n_clusters, k))]
dark_colors = [f"hsl({i * 360 / max(n_clusters, k)}, 70%, 30%)" for i in range(max(n_clusters, k))]

# Add data points colored by cluster assignment at the current iteration
for cluster_idx in range(k):
    cluster_points = data[current_labels == cluster_idx]
    fig.add_trace(go.Scatter(
        x=cluster_points[:, 0],
        y=cluster_points[:, 1],
        mode='markers',
        name=f'Cluster {cluster_idx}',
        marker=dict(size=6, color=colors[cluster_idx])
    ))

# Add centroids with darker matching cluster colors
for i, centroid in enumerate(current_centroids):
    fig.add_trace(go.Scatter(
        x=[centroid[0]],
        y=[centroid[1]],
        mode='markers',
        name=f'Centroid {i}',
        marker=dict(size=12, color=dark_colors[i], symbol="x")
    ))

# Layout adjustments
fig.update_layout(
    title=f"K-Means Clustering - Iteration {iteration}",
    xaxis_title="X",
    yaxis_title="Y",
    legend_title="Clusters",
    xaxis=dict(scaleanchor="y", scaleratio=1),
    yaxis=dict(scaleanchor="x", scaleratio=1)
)

st.plotly_chart(fig)

st.markdown("""
### How to use this visualization:
1. Use the sidebar to adjust:
   - Number of samples in the dataset
   - Number of clusters (K)
   - Number of true clusters in the generated data
   - Dispersion around cluster centers in the generated data (SD)
2. Use the iteration slider to move through the clustering process
3. Observe how:
   - Centroids (X) move to the center of their clusters
   - Points are reassigned to the nearest centroid
   - The algorithm converges when centroids stop moving
""")