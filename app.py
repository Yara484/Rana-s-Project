import streamlit as st
import pandas as pd
import plotly.express as px

# List of questions (reordered as requested)
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

# Distinct color pairs (Yes/No) for each question
color_pairs = [
    ("#FF69B4", "#90EE90"), ("#FFD700", "#00CED1"), ("#FF4500", "#7B68EE"),
    ("#FF1493", "#ADFF2F"), ("#1E90FF", "#F08080"), ("#20B2AA", "#FFA07A"),
    ("#BA55D3", "#5F9EA0"), ("#FF6347", "#48D1CC"), ("#DA70D6", "#66CDAA"),
    ("#FF8C00", "#6A5ACD"), ("#7FFF00", "#DC143C")
]

# Session state setup
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "responses" not in st.session_state:
    st.session_state.responses = []

# Get current question number
q_num = st.session_state.question_index + 1
q_code = f"Q{q_num}"

# Display the question in larger font
st.markdown(
    f"<p style='text-align: center; font-size:24px;'>{q_code}) {questions[st.session_state.question_index]}</p>",
    unsafe_allow_html=True
)

# Display Yes/No buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Yes", use_container_width=True):
        st.session_state.responses.append((q_code, "Yes"))
        st.session_state.question_index = (st.session_state.question_index + 1) % len(questions)
        st.rerun()
with col2:
    if st.button("No", use_container_width=True):
        st.session_state.responses.append((q_code, "No"))
        st.session_state.question_index = (st.session_state.question_index + 1) % len(questions)
        st.rerun()

# Data prep for charts
data = pd.DataFrame(st.session_state.responses, columns=["Question", "Answer"])
counts = data.groupby(["Question", "Answer"]).size().reset_index(name="Count")

# Assign colors based on question and answer
def assign_color(row):
    index = int(row["Question"][1:]) - 1
    return color_pairs[index][0] if row["Answer"] == "Yes" else color_pairs[index][1]

counts["Color"] = counts.apply(assign_color, axis=1)

# Bubble chart (larger bubbles)
bubble_chart = px.scatter(
    counts,
    x="Question",
    y="Count",
    size="Count",
    color="Color",
    color_discrete_map="identity",
    hover_name="Question",
    size_max=80,
    height=600
)
bubble_chart.update_traces(marker=dict(sizemode="diameter"))
bubble_chart.update_layout(margin=dict(t=20, b=20, l=0, r=0))

# Stream chart prep
pivot_data = data.groupby(["Question", "Answer"]).size().unstack(fill_value=0).reset_index()

# Assign fixed colors for answers
answer_order = ["Yes", "No"]
stream_colors = []
for i in range(len(questions)):
    stream_colors.append(color_pairs[i][0])  # Yes
    stream_colors.append(color_pairs[i][1])  # No

# Convert to long format for Plotly express
long_data = pd.melt(pivot_data, id_vars="Question", value_vars=answer_order, var_name="Answer", value_name="Count")
long_data["Color"] = long_data.apply(assign_color, axis=1)

stream_chart = px.area(
    long_data,
    x="Question",
    y="Count",
    color="Answer",
    color_discrete_sequence=[pair for pair in sum(color_pairs, ())],
    line_group="Answer",
    height=600
)
stream_chart.update_layout(margin=dict(t=20, b=20, l=0, r=0))

# Show both charts side-by-side
st.markdown("<hr>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bubble_chart, use_container_width=True)
with col2:
    st.plotly_chart(stream_chart, use_container_width=True)
