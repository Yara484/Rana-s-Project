import streamlit as st
import pandas as pd
import plotly.express as px

# Questions list (in the new order)
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

# Unique color pairs for each question
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

# Title and current question
st.markdown("<h2 style='text-align: center; font-size:24px;'>Emotional Reflection Survey</h2>", unsafe_allow_html=True)
q_num = st.session_state.question_index + 1
st.markdown(f"<h4 style='text-align: center; font-size:18px;'>(Q{q_num}) {questions[st.session_state.question_index]}</h4>", unsafe_allow_html=True)

# Answer buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Yes", use_container_width=True):
        st.session_state.responses.append((f"Q{q_num}", "Yes"))
        st.session_state.question_index = (st.session_state.question_index + 1) % len(questions)
        st.experimental_rerun()
with col2:
    if st.button("No", use_container_width=True):
        st.session_state.responses.append((f"Q{q_num}", "No"))
        st.session_state.question_index = (st.session_state.question_index + 1) % len(questions)
        st.experimental_rerun()

# Prepare data
if st.session_state.responses:
    df = pd.DataFrame(st.session_state.responses, columns=["Question", "Answer"])
    count_df = df.groupby(["Question", "Answer"]).size().reset_index(name="Count")

    # Create color column for bubble chart
    def get_color(row):
        q_index = int(row["Question"][1:]) - 1
        return color_pairs[q_index][0] if row["Answer"] == "Yes" else color_pairs[q_index][1]
    count_df["Color"] = count_df.apply(get_color, axis=1)

    # Bubble Chart
    bubble_fig = px.scatter(
        count_df,
        x="Question",
        y="Count",
        size="Count",
        color="Color",
        color_discrete_map="identity",
        hover_name="Question",
        size_max=100,
        height=500
    )
    bubble_fig.update_traces(marker=dict(sizemode="diameter"))
    bubble_fig.update_layout(margin=dict(t=20, b=20))

    # Stream Chart Data
    stream_df = df.groupby(["Question", "Answer"]).size().unstack(fill_value=0).reset_index()

    # Map answer-color combos
    answer_colors = []
    for i in range(len(questions)):
        answer_colors.append(color_pairs[i][0])  # Yes
        answer_colors.append(color_pairs[i][1])  # No

    # Create the stream chart
    melted_stream_df = df.groupby(["Question", "Answer"]).size().reset_index(name="Count")
    stream_fig = px.area(
        melted_stream_df,
        x="Question",
        y="Count",
        color="Answer",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"],  # fallback colors
        line_group="Answer",
        height=500
    )
    stream_fig.update_layout(margin=dict(t=20, b=20), showlegend=True)

    # Display both charts
    st.markdown("<hr>", unsafe_allow_html=True)
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.plotly_chart(bubble_fig, use_container_width=True)
    with chart_col2:
        st.plotly_chart(stream_fig, use_container_width=True)
