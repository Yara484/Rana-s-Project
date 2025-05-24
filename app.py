working i guess import streamlit as st
import pandas as pd
import plotly.express as px
import random

# Questions list
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

# Colors for Yes/No for each question
color_pairs = [
    ("#FF69B4", "#90EE90"), ("#FFD700", "#00CED1"), ("#FF4500", "#7B68EE"),
    ("#FF1493", "#ADFF2F"), ("#1E90FF", "#F08080"), ("#20B2AA", "#FFA07A"),
    ("#BA55D3", "#5F9EA0"), ("#FF6347", "#48D1CC"), ("#DA70D6", "#66CDAA"),
    ("#FF8C00", "#6A5ACD"), ("#7FFF00", "#DC143C")
]

# Initialize session state
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "responses" not in st.session_state:
    st.session_state.responses = []

# Title and question
st.markdown("<h2 style='text-align: center;'>Emotional Reflection Survey</h2>", unsafe_allow_html=True)
question_number = st.session_state.question_index + 1
st.markdown(f"<h4 style='text-align: center; font-size:18px;'>(Q{question_number}) {questions[st.session_state.question_index]}</h4>", unsafe_allow_html=True)

# Collect response
col1, col2 = st.columns(2)
with col1:
    if st.button("Yes", use_container_width=True):
        st.session_state.responses.append((f"Q{question_number}", "Yes"))
        st.session_state.question_index = (st.session_state.question_index + 1) % len(questions)
        st.experimental_rerun()
with col2:
    if st.button("No", use_container_width=True):
        st.session_state.responses.append((f"Q{question_number}", "No"))
        st.session_state.question_index = (st.session_state.question_index + 1) % len(questions)
        st.experimental_rerun()

# Prepare data for charts
data = pd.DataFrame(st.session_state.responses, columns=["Question", "Answer"])

# Count responses
counts = data.groupby(["Question", "Answer"]).size().reset_index(name="Count")

# Assign colors
counts["Color"] = counts.apply(lambda row: color_pairs[int(row["Question"][1:])-1][0] if row["Answer"] == "Yes" else color_pairs[int(row["Question"][1:])-1][1], axis=1)

# Bubble chart
bubble_chart = px.scatter(
    counts,
    x="Question",
    y="Count",
    size="Count",
    color="Color",
    color_discrete_map="identity",
    hover_name="Question",
    size_max=80,
    height=500
)
bubble_chart.update_traces(marker=dict(sizemode="diameter"))
bubble_chart.update_layout(margin=dict(t=20, b=20, l=0, r=0))

# Streamgraph (Area chart)
stream_data = data.groupby(["Question", "Answer"]).size().unstack(fill_value=0).reset_index()
stream_chart = px.area(
    stream_data,
    x="Question",
    y=stream_data.columns[1:],
    color_discrete_sequence=[pair for pair in sum(color_pairs, ())],
    height=500
)
stream_chart.update_layout(margin=dict(t=20, b=20, l=0, r=0))

# Layout for charts
st.markdown("<hr>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bubble_chart, use_container_width=True)
with col2:
    st.plotly_chart(stream_chart, use_container_width=True)
