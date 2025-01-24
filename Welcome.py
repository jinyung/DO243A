import streamlit as st

st.write("# Welcome to DO243A!")

st.sidebar.success("Select a demo above.")

st.markdown(
  """
  Welcome to **Introduction to Programming with Python** of Department of Oceanography, 
  National Sun Yat-sen University. In this course we will learn how to program in `Python` 
  and build some interactive web app with it.

  **👈 Select a demo from the sidebar** to see some examples. Note that in each demo the app options are in the sidebar.
  
  **More advanced examples(takes some times to load):**
  - [Plotting vector fields on map](https://jinyung.github.io/DO243A/Ocean_current.html)
  - [Perform K-means clustering and visualize how it works](https://jinyung.github.io/DO243A/K_means.html)
""")
 