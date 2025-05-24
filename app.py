import streamlit as st
import pandas as pd
import plotly.express as px

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

# Colors for Yes/No for each question (pairs)
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

# Display current question
q_num = st.session_state.question_index + 1
st.markdown(
    f"<p style='text-align: center; font-size:20px;'>(Q{q_num}) {questions[st.session_state.question_index]}</p>",
    unsafe_allow_html=True
)

# Buttons for Yes / No answers
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

# Prepare data for visualization if we have responses
if st.session_state.responses:
    data = pd.DataFrame(st.session_state.responses, columns=["Question", "Answer"])
    counts = data.groupby(["Question", "Answer"]).size().reset_index(name="Count")

    # Safe function to assign colors based on question number and answer
    def get_color(row):
        try:
            idx = int(row["Question"][1:]) - 1  # Extract question number (e.g., Q3 -> 2)
            if row["Answer"] == "Yes":
                return color_pairs[idx][0]
            else:
                return color_pairs[idx][1]
        except Exception as e:
            st.error(f"Error processing row: {row} - {e}")
            return "#000000"  # fallback black color

    counts["Color"] = counts.apply(get_color, axis=1)

    # Bubble chart
    bubble_chart = px.scatter(
        counts,
        x="Question",
        y="Count",
        size="Count",
        color="Color",
        color_discrete_map="identity",
        hover_name="Question",
        size_max=100,
        height=550
    )
    bubble_chart.update_traces(marker=dict(sizemode="diameter"))
    bubble_chart.update_layout(margin=dict(t=20, b=20, l=0, r=0))

    # Prepare data for stream graph
    stream_data = data.groupby(["Question", "Answer"]).size().unstack(fill_value=0).reset_index()

    # Flatten color pairs for stream graph: each question has two colors (Yes and No)
    stream_colors = []
    for yes_color, no_color in color_pairs:
        stream_colors.extend([yes_color, no_color])

    # Adjust colors to match number of columns (excluding 'Question')
    stream_colors = stream_colors[:len(stream_data.columns) - 1]

    stream_chart = px.area(
        stream_data,
        x="Question",
        y=stream_data.columns[1:],
        color_discrete_sequence=stream_colors,
        height=550
    )
    stream_chart.update_layout(margin=dict(t=20, b=20, l=0, r=0))

    # Display charts side by side
    st.markdown("<hr>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(bubble_chart, use_container_width=True)
    with col2:
        st.plotly_chart(stream_chart, use_container_width=True)
else:
    st.info("Please answer the questions to see the charts.")
