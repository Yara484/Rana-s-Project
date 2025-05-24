import streamlit as st
import plotly.graph_objs as go
import plotly.express as px

# Define your questions
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

# Define color pairs: one pair (yes/no) per question
color_pairs = [
    ("#FF69B4", "#1E90FF"),  # Q1: pink / blue
    ("#32CD32", "#006400"),  # Q2: light green / dark green
    ("#FFD700", "#FFA500"),  # Q3: gold / orange
    ("#8A2BE2", "#4B0082"),  # Q4: blue violet / indigo
    ("#FF6347", "#800000"),  # Q5: tomato / maroon
    ("#00CED1", "#4682B4"),  # Q6: dark turquoise / steel blue
    ("#DC143C", "#2F4F4F"),  # Q7: crimson / dark slate gray
    ("#FF8C00", "#B8860B"),  # Q8: dark orange / dark goldenrod
    ("#9932CC", "#6A5ACD"),  # Q9: dark orchid / slate blue
    ("#7CFC00", "#228B22"),  # Q10: lawn green / forest green
    ("#00FA9A", "#008080")   # Q11: medium spring green / teal
]

# Initialize session state
if "index" not in st.session_state:
    st.session_state.index = 0
if "counts" not in st.session_state:
    st.session_state.counts = {"yes": [0]*len(questions), "no": [0]*len(questions)}

def handle_response():
    choice = st.session_state["choice"]
    st.session_state.counts[choice][st.session_state.index] += 1
    st.session_state.index = (st.session_state.index + 1) % len(questions)
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

# Create bubble chart data
bubble_data = []
for i in range(len(questions)):
    bubble_data.append(dict(
        x=i,
        y=1,
        size=st.session_state.counts["yes"][i] + 1,
        color=color_pairs[i][0],
        label=f"Q{i+1} Yes ({st.session_state.counts['yes'][i]})"
    ))
    bubble_data.append(dict(
        x=i,
        y=2,
        size=st.session_state.counts["no"][i] + 1,
        color=color_pairs[i][1],
        label=f"Q{i+1} No ({st.session_state.counts['no'][i]})"
    ))

# Bubble Chart
with st.expander("Bubble Chart", expanded=True):
    bubble_fig = go.Figure()
    for item in bubble_data:
        bubble_fig.add_trace(go.Scatter(
            x=[item["x"]],
            y=[item["y"]],
            mode='markers+text',
            marker=dict(size=item["size"]*5, color=item["color"], sizemode='area'),
            text=[item["label"]],
            textposition='bottom center',
            hoverinfo='text'
        ))
    bubble_fig.update_layout(
        title="Bubble Chart (Each Question: Yes & No)",
        xaxis=dict(title='Questions'),
        yaxis=dict(title='Response Type (1 = Yes, 2 = No)', showticklabels=False),
        showlegend=False,
        height=600
    )
    st.plotly_chart(bubble_fig, use_container_width=True)

# Stream Graph
with st.expander("Stream Graph", expanded=True):
    stream_fig = go.Figure()
    for i in range(len(questions)):
        stream_fig.add_trace(go.Scatter(
            x=list(range(st.session_state.counts["yes"][i] + 1)),
            y=[1]*(st.session_state.counts["yes"][i] + 1),
            stackgroup='yes',
            name=f"Q{i+1} Yes",
            line=dict(color=color_pairs[i][0])
        ))
        stream_fig.add_trace(go.Scatter(
            x=list(range(st.session_state.counts["no"][i] + 1)),
            y=[1]*(st.session_state.counts["no"][i] + 1),
            stackgroup='no',
            name=f"Q{i+1} No",
            line=dict(color=color_pairs[i][1])
        ))
    stream_fig.update_layout(
        title="Stream Graph (Stacked Responses per Question)",
        xaxis=dict(title='Total Submissions'),
        yaxis=dict(title='Frequency'),
        height=600
    )
    st.plotly_chart(stream_fig, use_container_width=True)
