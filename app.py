import streamlit as st
import plotly.graph_objs as go
import random

# List of questions
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

# Define color pairs for each question
def get_color_pairs(n):
    base_colors = [
        ("#ff69b4", "#1e90ff"), ("#32cd32", "#006400"), ("#ffa500", "#8b0000"),
        ("#9370db", "#4b0082"), ("#00ced1", "#2f4f4f"), ("#ffd700", "#b8860b"),
        ("#ff7f50", "#dc143c"), ("#00fa9a", "#008080"), ("#ba55d3", "#9400d3"),
        ("#20b2aa", "#4682b4"), ("#ff6347", "#800000")
    ]
    return base_colors[:n]

# Initialize state
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'yes_counts' not in st.session_state:
    st.session_state.yes_counts = [0] * len(questions)
if 'no_counts' not in st.session_state:
    st.session_state.no_counts = [0] * len(questions)

color_pairs = get_color_pairs(len(questions))

# Function to generate bubble chart with bigger, more scattered bubbles
def generate_bubble_chart():
    bubble_x, bubble_y, bubble_size, bubble_color, bubble_label = [], [], [], [], []
    for i in range(len(questions)):
        # Scatter more by using wider random range, e.g. -15 to 15 instead of -10 to 10
        bubble_x.append(random.uniform(-1, 1) * 15)
        bubble_y.append(random.uniform(-1, 1) * 15)
        bubble_size.append(st.session_state.yes_counts[i] * 8 + 10)  # Keep size bigger
        bubble_color.append(color_pairs[i][0])
        bubble_label.append(f"Q{i+1} - Yes: {st.session_state.yes_counts[i]}")

        bubble_x.append(random.uniform(-1, 1) * 15)
        bubble_y.append(random.uniform(-1, 1) * 15)
        bubble_size.append(st.session_state.no_counts[i] * 8 + 10)
        bubble_color.append(color_pairs[i][1])
        bubble_label.append(f"Q{i+1} - No: {st.session_state.no_counts[i]}")

    return go.Figure(data=[go.Scatter(
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
    )]).update_layout(
        title="Bubble Chart",
        showlegend=False,
        height=500,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )

# Function to generate wider stream graph
def generate_stream_chart():
    fig = go.Figure()
    for i in range(len(questions)):
        fig.add_trace(go.Scatter(
            x=[i],
            y=[st.session_state.yes_counts[i]],
            stackgroup='one',
            name=f"Q{i+1} - Yes",
            line=dict(color=color_pairs[i][0])
        ))
        fig.add_trace(go.Scatter(
            x=[i],
            y=[st.session_state.no_counts[i]],
            stackgroup='one',
            name=f"Q{i+1} - No",
            line=dict(color=color_pairs[i][1])
        ))
    return fig.update_layout(
        title="Stream Graph",
        height=500,
        width=1100,   # wider width
        showlegend=False
    )

# Display current question, looping infinitely
index = st.session_state.question_index % len(questions)

st.markdown(f"### Q{index + 1}. {questions[index]}")

cols = st.columns([1, 1])
if cols[0].button("Yes"):
    st.session_state.yes_counts[index] += 1
    st.session_state.question_index += 1
if cols[1].button("No"):
    st.session_state.no_counts[index] += 1
    st.session_state.question_index += 1

# Show charts side by side
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(generate_bubble_chart(), use_container_width=True)
with col2:
    st.plotly_chart(generate_stream_chart(), use_container_width=True)
