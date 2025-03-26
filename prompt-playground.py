import streamlit as st
import openai
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Prompt Playground", page_icon="🧠")

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Configure OpenAI
client = openai.OpenAI(api_key=api_key)

# Initialize session history and favorites
if "history" not in st.session_state:
    st.session_state.history = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "enable_comparison" not in st.session_state:
    st.session_state.enable_comparison = False

st.title("🧠 Prompt Playground")
st.write("Test how different prompts affect GPT's response.")

# Model selection
default_model = "gpt-3.5-turbo"
model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
model = st.selectbox("Choose a model:", model_options, index=model_options.index(default_model))

st.session_state.enable_comparison = st.checkbox("🔀 Enable Side-by-Side Style Comparison")

style_options = [
    "Default",
    "Casual",
    "Formal",
    "Technical",
    "Jargon-Free",
    "Explain like I'm 5",
    "Twitter Thread"
]

if st.session_state.enable_comparison:
    style1 = st.selectbox("Choose first style:", style_options, key="style1")
    style2 = st.selectbox("Choose second style:", style_options, key="style2")
else:
    style = st.selectbox("Choose a style for GPT's response:", style_options)

prompt_templates = {
    "Custom": "",
    "Summarize this text": "Summarize the following text:\n\n",
    "Turn into a tweet": "Write a tweet based on this:\n\n",
    "Refactor this code": "Refactor this code:\n\n",
    "Generate quiz questions": "Generate quiz questions based on this content:\n\n"
}

template_choice = st.selectbox("Choose a template:", list(prompt_templates.keys()))

prompt_title = st.text_input("Optional: Add a title for this prompt (for easier tracking in history or favorites)")

user_input = st.text_area(
    label="Enter your prompt here:",
    value=prompt_templates[template_choice],
    key=template_choice
)

def get_system_msg(style):
    return {
        "Default": "You are a helpful assistant.",
        "Casual": "Respond in a laid-back, conversational tone like you're texting a friend.",
        "Formal": "Respond in a professional and polished tone suitable for academic or business writing.",
        "Technical": "Respond with highly technical language appropriate for experts in the field.",
        "Jargon-Free": "Explain things using simple, everyday language without any technical jargon.",
        "Explain like I'm 5": "Explain it very simply, like you're talking to a 5-year-old.",
        "Twitter Thread": "Write the response like a viral Twitter thread with short, punchy paragraphs and emojis if relevant."
    }.get(style, "You are a helpful assistant.")

if st.button("Generate"):
    if user_input:
        with st.spinner("Thinking..."):
            try:
                if st.session_state.enable_comparison:
                    responses = {}
                    for s in [style1, style2]:
                        system_msg = get_system_msg(s)
                        response = client.chat.completions.create(
                            model=model,
                            messages=[
                                {"role": "system", "content": system_msg},
                                {"role": "user", "content": user_input}
                            ],
                            temperature=0.7,
                            max_tokens=250
                        )
                        responses[s] = response.choices[0].message.content

                    st.markdown("### 💬 GPT Response (Comparison Mode):")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader(style1)
                        st.write(responses[style1])
                    with col2:
                        st.subheader(style2)
                        st.write(responses[style2])

                    st.session_state.history.append({
                        "title": prompt_title,
                        "prompt": user_input,
                        "styles": [style1, style2],
                        "responses": responses,
                        "model": model
                    })

                else:
                    system_msg = get_system_msg(style)
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": system_msg},
                            {"role": "user", "content": user_input}
                        ],
                        temperature=0.7,
                        max_tokens=250
                    )
                    reply = response.choices[0].message.content
                    st.markdown("### 💬 GPT Response:")
                    st.write(reply)

                    st.session_state.history.append({
                        "title": prompt_title,
                        "prompt": user_input,
                        "styles": [style],
                        "responses": {style: reply},
                        "model": model
                    })

                    st.download_button(
                        label="💾 Download Response as .txt",
                        data=reply,
                        file_name="gpt_response.txt",
                        mime="text/plain"
                    )
            except Exception as e:
                st.warning("⚠️ Using demo mode (API error or quota reached)")
                st.write(f"🧪 [Demo Mode] This is a simulated GPT response.\n\n(Error: {e})")
    else:
        st.warning("Please enter a prompt before clicking Generate.")

# ⭐ Show Starred (Favorites) panel
if st.session_state.favorites:
    st.markdown("---")
    st.markdown("### ⭐ Starred Responses")
    for i, item in enumerate(reversed(st.session_state.favorites), 1):
        with st.expander(f"{i}. {item['title'] or 'Prompt'}: {item['prompt'][:50]}..."):
            if item['title']:
                st.markdown(f"**Title:** {item['title']}")
            st.markdown(f"**Prompt:**\n{item['prompt']}")
            for s in item["styles"]:
                st.markdown(f"**Style - {s}:**\n{item['responses'][s]}")
            st.markdown(f"**Model:** {item['model']}")
            if st.button("❌ Remove from Favorites", key=f"unfav_{i}"):
                st.session_state.favorites.remove(item)
                st.rerun()

# 📜 Show history panel with Clear History option
if st.session_state.history:
    st.markdown("---")
    st.markdown("### 📜 Response History")

    if st.button("🗑️ Clear History"):
        st.session_state.history.clear()
        st.rerun()

    recent_history = st.session_state.history[-10:]
    for i, item in enumerate(reversed(recent_history), 1):
        with st.expander(f"{i}. {item['title'] or 'Prompt'}: {item['prompt'][:50]}..."):
            if item['title']:
                st.markdown(f"**Title:** {item['title']}")
            st.markdown(f"**Prompt:**\n{item['prompt']}")
            for s in item["styles"]:
                st.markdown(f"**Style - {s}:**\n{item['responses'][s]}")
            st.markdown(f"**Model:** {item['model']}")
            if item not in st.session_state.favorites:
                if st.button("⭐ Favorite", key=f"fav_{i}"):
                    st.session_state.favorites.append(item)
                    st.rerun()
            else:
                st.markdown("✅ Already in favorites")
