import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np

# Load weights
@st.cache_resource
def load_weights():
  weights = np.load("mnist_mlp_weights.npz")
  return weights

weights = load_weights()

def relu(x):
  return np.maximum(0, x)

def softmax(x):
  e_x = np.exp(x - np.max(x))
  return e_x / e_x.sum(axis=1, keepdims=True)

# Forward pass for Flatten -> Dense(32, relu) -> Dense(10, softmax)
def forward(x):
  W1, b1 = weights['W1'], weights['b1']
  W2, b2 = weights['W2'], weights['b2']
  x = x.reshape((1, -1))  # Flatten
  a1 = relu(np.dot(x, W1) + b1)
  a2 = np.dot(a1, W2) + b2
  return softmax(a2)

def preprocess(img):
  # gray: take first layer
  gray = img[..., 0].astype("float32")
  
  # Check if the image is blank (all white)
  if np.all(gray == 255):
    return None

  # shift
  ys, xs = np.where(gray==0)
  cy, cx = ys.mean(), xs.mean()
  shift_y = int(140 - cy)
  shift_x = int(140 - cx)
  shifted = np.roll(gray, shift=(shift_y, shift_x), axis=(0, 1))

  # scale down and change to 0-1 and invert
  gray_small = 1 - shifted.reshape(28, 10, 28, 10).mean(axis=(1, 3)) / 255.0

  return gray_small.reshape(1, 28, 28)

st.title("Hand written digit predictor")
st.info("Draw a digit (0-9) on the canvas, then press **Predict** to classify it.")

# Drawing canvas (28x28 ×10)
canvas = st_canvas(stroke_color="black", background_color="white",
  width=280, height=280, stroke_width=20, drawing_mode="freedraw")

# Predict button
if st.button("Predict"):
  x = preprocess(canvas.image_data)
  if x is not None:
    probs = forward(x)[0]
    pred = int(np.argmax(probs))
    st.subheader(f"Prediction: **{pred}**")
    st.bar_chart(probs, y_label='Probability', horizontal=True)
  else:
    st.warning("Please draw a digit on the canvas.")
