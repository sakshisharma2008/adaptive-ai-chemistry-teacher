import streamlit as st
from google import genai

# ---------------- GEMINI ----------------

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

MODEL = "gemini-3.6-flash"


# ---------------- SESSION ----------------

if "question" not in st.session_state:
    st.session_state.question = ""

if "topic" not in st.session_state:
    st.session_state.topic = ""

if "history" not in st.session_state:
    st.session_state.history = []


# ---------------- APP ----------------

st.title("👩‍🏫 AI Teacher")
st.caption(
    "AI that teaches according to how you think."
)

topic = st.text_input(
    "Choose a Chemistry topic",
    placeholder="Example: Atomic Structure"
)


# ============================================================
# START
# ============================================================

if st.button("🚀 START LEARNING", type="primary"):

    if not topic:
        st.warning("Please enter a topic.")
    else:

        prompt = f"""
You are an adaptive Chemistry teacher.

Topic: {topic}

Do not give a lecture.

First understand the student's existing knowledge.

Give:
1. A short friendly introduction.
2. Why the topic matters.
3. EXACTLY ONE simple conceptual question.
4. Ask the student to explain their thinking.

Do not give the answer.

The question should test understanding,
not memorization.

Make it simple, professional and engaging.
"""

        with st.spinner("🧠 Preparing your lesson..."):

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )

        st.session_state.topic = topic
        st.session_state.question = response.text

        st.rerun()


# ============================================================
# TEACHER
# ============================================================

if st.session_state.question:

    st.divider()

    st.subheader("👩‍🏫 Your Teacher")

    st.write(st.session_state.question)

    answer = st.text_area(
        "✍️ Explain your thinking",
        placeholder="Write what you think and why..."
    )

    if st.button("📤 Submit Answer", type="primary"):

        if not answer:
            st.warning("Please write your answer.")
        else:

            prompt = f"""
You are an adaptive Chemistry teacher.

Topic:
{st.session_state.topic}

Previous teacher question:
{st.session_state.question}

Student answer:
{answer}

Your job is to understand the student's thinking.

Analyze:

1. Is the answer Correct, Partially Correct,
   Incorrect, or Unclear?

2. What does the student understand?

3. What misconception or knowledge gap exists?

4. Choose the best teaching approach:
   Hint, Analogy, Simple Explanation,
   Guided Practice, or Challenge Question.

5. Adapt the difficulty.

6. Give short encouraging feedback.

7. Decide what the student should learn next.

8. Ask EXACTLY ONE next question.

IMPORTANT:

If incorrect:
do not immediately give the complete answer.
Give a hint and guide the student.

If partially correct:
keep the correct idea and address the missing concept.

If correct:
increase the difficulty.

The next question MUST depend on the student's answer.

Return:

ASSESSMENT:
...

UNDERSTANDS:
...

KNOWLEDGE_GAP:
...

TEACHING_STRATEGY:
...

FEEDBACK:
...

NEXT_STEP:
...

NEXT_QUESTION:
...

DIFFICULTY:
...
"""

            with st.spinner(
                "🧠 Understanding how you think..."
            ):

                response = client.models.generate_content(
                    model=MODEL,
                    contents=prompt
                )

            # Save learning history
            st.session_state.history.append(
                {
                    "question": st.session_state.question,
                    "answer": answer,
                    "teacher": response.text
                }
            )

            # Continue adaptive lesson
            st.session_state.question = response.text

            st.rerun()


# ============================================================
# HISTORY
# ============================================================

if st.session_state.history:

    st.divider()

    st.subheader("📚 Learning History")

    for i, item in enumerate(
        st.session_state.history,
        1
    ):

        with st.expander(
            f"Interaction {i}"
        ):

            st.write("👩‍🏫 **Question**")
            st.write(item["question"])

            st.write("✍️ **Your Answer**")
            st.write(item["answer"])

            st.write("🧠 **Teacher Response**")
            st.write(item["teacher"])