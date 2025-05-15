import streamlit as st
import plotly.express as px
import numpy as np

@st.cache_data
def load_gapminder():
    return px.data.gapminder()

gapminder = load_gapminder()
all_countries = sorted(gapminder["country"].unique())

st.title("Gapminder Animated Bubble Chart")
st.markdown("Track countries' development over time: GDP per capita, life expectancy, and population.")

def expand_select_all():
    if "Select all" in st.session_state.countries:
        st.session_state.countries = all_countries  

selected_countries = st.multiselect(
    "Select countries to include:",
    ["Select all"] + all_countries,
    default=["Taiwan", "Korea, Rep.", "Japan"],
    key="countries",
    on_change=expand_select_all
)

if selected_countries:
    filtered_data = gapminder[gapminder["country"].isin(selected_countries)]

    x_min = np.log10(filtered_data["gdpPercap"].min() * 0.8)
    x_max = np.log10(filtered_data["gdpPercap"].max() * 1.3)
    y_min = filtered_data["lifeExp"].min() - 5
    y_max = filtered_data["lifeExp"].max() + 10

    fig = px.scatter(
        filtered_data,
        x="gdpPercap", y="lifeExp",
        animation_frame="year", animation_group="country",
        size="pop", color="country",
        hover_name="country",
        log_x=True, size_max=50,
        labels={
            "gdpPercap": "GDP per Capita (USD)",
            "lifeExp": "Life Expectancy (Years)",
            "pop": "Population",
            "year": "Year",
        },
        title="Development Over Time",
    )

    fig.update_layout(
        xaxis=dict(range=[x_min, x_max]),
        yaxis=dict(range=[y_min, y_max]),
    )

    st.plotly_chart(fig)
else:
    st.error("Choose at least one country (or use 'Select all').")