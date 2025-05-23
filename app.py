import streamlit as st
import plotly.graph_objs as go

questions = [
    "Have you ever felt worthy of love from your parents only when you pleased them by grades, titles, prizes, etc.?",
    "Has this made you feel like you’re lying to yourself about your capabilities?",
    "Have you ever done something you didn't want to do only to please someone?",
    "Did you strive for perfection to gain approval or a sense of control?",
    "Have you ever felt like you’re the reason for your parents/friends/teachers emotions?",
    "Did you associate your self-worth with achievements or external validation?",
    "Have you ever taken on a responsibility just because it is expected from your gender even though you’re not consenting to this responsibility?",
    "If you have a sibling from the other gender, have you ever felt discriminated against because of this reason?",
    "Have you ever felt that you weren't accepted in society?",
    "Has people’s words ever affected you negatively or positively? (encouraged/discouraged you)?",
    "Have your thoughts and expectations (negative or positive) about yourself influenced your actions and contributed to making those expectations a reality?"
]

# Initialize session state only once
if "index" not in st.session_state:
    st.session_state.index = 0
if "counts" not in st.session_state:
    st.session_state.counts = {"yes": [0]*len(questions), "no": [0]*len(questions)}

def handle_response():
    choice = st.session_state["choice"]
    st.session_state.counts[choice][st.session_state.index] += 1
    st.session_state.index = (st.session_state.index + 1) % len(questions)
    # Clear choice for next question
    st.session_state["choice"] = None

st.title("Interactive Media Art: Response Cycle")

st.markdown(f"### Q{st.session_state.index + 1}: {questions[st.session_state.index]}")

with st.form(key='response_form', clear_on_submit=True):
    st.radio(
        label="Select your answer:",
        options=["yes", "no"],
        key="choice",
        horizontal=True
    )
    submitted = st.form_submit_button("Submit", on_click=handle_response)

col1, col2 = st.columns(2)

with col1:
    bubble_fig = go.Figure()
    bubble_fig.add_trace(go.Scatter(
        x=list(range(len(questions))),
        y=st.session_state.counts["yes"],
        mode='markers',
        marker=dict(size=[x+5 for x in st.session_state.counts["yes"]], color="green"),
        name="Yes"
    ))
    bubble_fig.add_trace(go.Scatter(
        x=list(range(len(questions))),
        y=st.session_state.counts["no"],
        mode='markers',
        marker=dict(size=[x+5 for x in st.session_state.counts["no"]], color="red"),
        name="No"
    ))
    bubble_fig.update_layout(title="Bubble Chart")
    st.plotly_chart(bubble_fig, use_container_width=True)

with col2:
    stream_fig = go.Figure()
    stream_fig.add_trace(go.Scatter(
        x=list(range(len(questions))),
        y=st.session_state.counts["yes"],
        stackgroup='one',
        name='Yes',
        line=dict(color='green')
    ))
    stream_fig.add_trace(go.Scatter(
        x=list(range(len(questions))),
        y=st.session_state.counts["no"],
        stackgroup='one',
        name='No',
        line=dict(color='red')
    ))
    stream_fig.update_layout(title="Stream Graph")
    st.plotly_chart(stream_fig, use_container_width=True)
