import streamlit as st
import plotly.graph_objs as go
import random

# Simulated data
questions = [f"Q{i+1}" for i in range(11)]
yes_counts = [random.randint(5, 20) for _ in range(11)]
no_counts = [random.randint(5, 20) for _ in range(11)]

# Define colors
colors = [
    "#ff69b4", "#1e90ff", "#32cd32", "#006400",
    "#ffa500", "#8b0000", "#9370db", "#4b0082",
    "#00ced1", "#2f4f4f", "#ffd700", "#b8860b",
    "#ff7f50", "#dc143c", "#00fa9a", "#008080",
    "#ba55d3", "#9400d3", "#20b2aa", "#4682b4",
    "#ff6347", "#800000"
]

# Generate scattered bubble data
bubble_x, bubble_y, bubble_size, bubble_color, bubble_label = [], [], [], [], []

for i in range(11):
    # yes
    bubble_x.append(random.uniform(-1, 1) * 10)
    bubble_y.append(random.uniform(-1, 1) * 10)
    bubble_size.append(yes_counts[i] * 3 + 10)
    bubble_color.append(colors[i * 2])
    bubble_label.append(f"{questions[i]} - Yes: {yes_counts[i]}")

    # no
    bubble_x.append(random.uniform(-1, 1) * 10)
    bubble_y.append(random.uniform(-1, 1) * 10)
    bubble_size.append(no_counts[i] * 3 + 10)
    bubble_color.append(colors[i * 2 + 1])
    bubble_label.append(f"{questions[i]} - No: {no_counts[i]}")

# Bubble chart
bubble_fig = go.Figure(data=[go.Scatter(
    x=bubble_x,
    y=bubble_y,
    mode='markers',
    marker=dict(
        size=bubble_size,
        color=bubble_color,
        sizemode='diameter',
        opacity=0.7,
        line=dict(width=2, color='white')
    ),
    text=bubble_label,
    hoverinfo='text'
)])
bubble_fig.update_layout(
    title="Bubble Chart (Scattered Layout)",
    showlegend=False,
    xaxis=dict(showgrid=False, zeroline=False, visible=False),
    yaxis=dict(showgrid=False, zeroline=False, visible=False),
    height=600
)

# Stream (area) chart
x_values = list(range(11))
stream_fig = go.Figure()
stream_fig.add_trace(go.Scatter(
    x=x_values,
    y=yes_counts,
    stackgroup='one',
    name='Yes',
    line=dict(color='green')
))
stream_fig.add_trace(go.Scatter(
    x=x_values,
    y=no_counts,
    stackgroup='one',
    name='No',
    line=dict(color='red')
))
stream_fig.update_layout(title="Stream Graph", height=600)

# Streamlit layout
st.set_page_config(layout="wide")
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(bubble_fig, use_container_width=True)

with col2:
    st.plotly_chart(stream_fig, use_container_width=True)
