import streamlit as st
import plotly.graph_objs as go
import random

# Updated question list
questions = [
    "Have you ever felt worthy of love from your parents only when you pleased them by grades, titles, prizes, etc.?",
    "Did your parents expectations make you feel like you’re lying to yourself about your capabilities?",
    "Have you ever felt that you weren't accepted in society?",
    "Did you strive for perfection to gain approval or a sense of control?",
    "Did you associate your self-worth with achievements or external validation?",
    "Has people’s words ever affected you negatively or positively? (Encouraged/discouraged you)",
    "Have your thoughts and expectations (negative or positive) about yourself influenced your actions and contributed to making those expectations a reality?",
    "Have you ever done something you didn't want to do only to please someone?",
    "Have you ever felt like you’re the reason for your parents’, friends’, or teachers’ emotions?",
    "Have you ever taken on a responsibility just because it is expected from your gender, even though you’re not consenting to this responsibility?",
    "If you have a sibling from the other gender, have you ever felt discriminated against because of this reason?"
]

# Generate dummy yes/no counts
yes_counts = [random.randint(5, 20) for _ in range(len(questions))]
no_counts = [random.randint(5, 20) for _ in range(len(questions))]

# Define unique colors for each question
color_pairs = [
    ("#ff69b4", "#1e90ff"), ("#32cd32", "#006400"), ("#ffa500", "#8b0000"),
    ("#9370db", "#4b0082"), ("#00ced1", "#2f4f4f"), ("#ffd700", "#b8860b"),
    ("#ff7f50", "#dc143c"), ("#00fa9a", "#008080"), ("#ba55d3", "#9400d3"),
    ("#20b2aa", "#4682b4"), ("#ff6347", "#800000")
]

# Initialize layout
st.set_page_config(layout="wide")

# Display questions and voting buttons
st.markdown("### **Questions** (Click 'Yes' or 'No' for each):", unsafe_allow_html=True)
for i, question in enumerate(questions):
    cols = st.columns([4, 1, 1])
    with cols[0]:
        st.markdown(f"<span style='font-size:13px'>{question}</span>", unsafe_allow_html=True)
    with cols[1]:
        if cols[1].button("Yes", key=f"yes_{i}"):
            yes_counts[i] += 1
    with cols[2]:
        if cols[2].button("No", key=f"no_{i}"):
            no_counts[i] += 1

# Prepare bubble chart data
bubble_x, bubble_y, bubble_size, bubble_color, bubble_label = [], [], [], [], []

for i, q in enumerate(questions):
    bubble_x.append(random.uniform(-1, 1) * 10)
    bubble_y.append(random.uniform(-1, 1) * 10)
    bubble_size.append(yes_counts[i] * 3 + 10)
    bubble_color.append(color_pairs[i][0])
    bubble_label.append(f"{q[:40]}... - Yes: {yes_counts[i]}")

    bubble_x.append(random.uniform(-1, 1) * 10)
    bubble_y.append(random.uniform(-1, 1) * 10)
    bubble_size.append(no_counts[i] * 3 + 10)
    bubble_color.append(color_pairs[i][1])
    bubble_label.append(f"{q[:40]}... - No: {no_counts[i]}")

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
    height=500
)

# Stream graph with same color pairs
x_values = list(range(len(questions)))
stream_fig = go.Figure()

for i in range(len(questions)):
    stream_fig.add_trace(go.Scatter(
        x=[i],
        y=[yes_counts[i]],
        stackgroup='one',
        name=f"{questions[i][:20]} - Yes",
        line=dict(color=color_pairs[i][0])
    ))
    stream_fig.add_trace(go.Scatter(
        x=[i],
        y=[no_counts[i]],
        stackgroup='one',
        name=f"{questions[i][:20]} - No",
        line=dict(color=color_pairs[i][1])
    ))

stream_fig.update_layout(title="Stream Graph", height=500, showlegend=False)

# Display both charts side-by-side
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bubble_fig, use_container_width=True)
with col2:
    st.plotly_chart(stream_fig, use_container_width=True)
