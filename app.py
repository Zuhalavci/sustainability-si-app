import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dynamic Sustainability Index Tool", layout="centered")
st.title("🌀 Dynamic Sustainability Index Calculator")
st.markdown("This tool allows users to compare the Sustainability Index (SI) of different micro-drilling methods by adjusting the importance weights of various sustainability criteria.")

# Criteria and default weights
criteria = ['Energy', 'CO2', 'Cost', 'Tool Wear', 'Fluid Usage', 'Social Impact']
def_weights = {
    "Energy": 0.30,
    "CO2": 0.30,
    "Cost": 0.18,
    "Tool Wear": 0.12,
    "Fluid Usage": 0.06,
    "Social Impact": 0.04
}

# Normalized SI data for three methods
normalized_values = {
    "HP EDM": [0.53, 1.00, 0.00, 0.00, 0.00, 0.00],
    "LP EDM": [1.00, 1.00, 1.00, 1.00, 0.09, 0.78],
    "Conventional": [0.00, 0.00, 0.30, 0.10, 1.00, 1.00]
}

st.markdown("### 🎛️ Adjust Criteria Weights")

with st.expander("Click here to set your own criteria weights", expanded=True):
    weights = {}
    total_weight = 0
    for crit in criteria:
        val = st.slider(crit, 0.0, 1.0, def_weights[crit], 0.01)
        weights[crit] = val
        total_weight += val

    if total_weight == 0:
        st.warning("Total weight cannot be zero.")
        st.stop()

    for crit in weights:
        weights[crit] /= total_weight

# Calculate Sustainability Index
methods = list(normalized_values.keys())
scores = {}
for method in methods:
    values = normalized_values[method]
    score = sum(weights[criteria[i]] * values[i] for i in range(len(criteria)))
    scores[method] = score

# Display results
results_df = pd.DataFrame(list(scores.items()), columns=["Method", "Dynamic SI"])
results_df.sort_values("Dynamic SI", ascending=False, inplace=True)

st.subheader("🔢 Calculated Sustainability Index Scores")
st.dataframe(results_df.set_index("Method"))

# Bar chart
fig = px.bar(results_df, x="Method", y="Dynamic SI", title="Sustainability Index Comparison",
             color="Method", text="Dynamic SI")
fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
fig.update_layout(yaxis=dict(range=[0, 1]))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("💡 This version is optimized for mobile devices. Sliders are available above via expandable section.")