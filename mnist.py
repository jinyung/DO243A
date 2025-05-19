import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import keras

# Load model directly from Hugging Face Hub (with cache)
@st.cache_resource
def load_model():
  return keras.saving.load_model("hf://jin-yung/mnist")

model = load_model()

def preprocess(img):
  # gray: take first layer
  gray = img[..., 0].astype("float32")

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

# st.write(canvas)

# Predict button
if st.button("Predict"):
  if canvas.image_data is not None:
    x = preprocess(canvas.image_data)

    # Predict with model
    probs = model.predict(x, verbose=0)[0]
    pred = int(np.argmax(probs))

    # Show result
    st.subheader(f"Prediction: **{pred}**")
    st.bar_chart(probs, y_label='Probability', horizontal = True)
  else:
    st.warning("Please draw a digit before predicting.")
