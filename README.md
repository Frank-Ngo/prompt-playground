# 🧠 Prompt Playground

**Prompt Playground** is an interactive app built with **Streamlit** and the **OpenAI API** to explore how prompt phrasing influences GPT responses. It started as a fun side project and evolved into a functional tool that helps visualize the impact of tone, clarity, and structure in real-time.

I designed it to experiment with prompt engineering principles and simplify the process of refining instructions — especially for non-technical users.

---

## ✨ What It Can Do

- 🎨 Adjust GPT's tone using styles like Casual, Technical, “Explain Like I’m 5”, or Twitter Thread
- 📋 Plug in templates for common tasks: Summarizing, Tweeting, Refactoring code, etc.
- 🧠 Automatically rewrite vague prompts into clear, GPT-friendly instructions
- 🔀 Compare two response styles side-by-side to test tone or delivery
- ⭐ Save your favorite responses and prompts
- 📜 Keep track of your latest 10 prompt interactions
- 💾 Download responses as `.txt` files
- 🔁 Switch models on the fly (GPT-3.5, GPT-4, GPT-4o)

---

## 🧠 Behind the Scenes

Prompt Playground is more than just a chat UI — it’s a structured interface for testing how instruction design affects model behavior.

When “Auto-Enhance Prompt” is enabled, the app passes your casual or unclear input through GPT-3.5 to rewrite it as a more effective instruction. That enhanced prompt is then used for the actual completion. You can compare how different tones or styles affect responses without needing to rewrite everything yourself.

This helps visualize prompt engineering in action and is especially useful when fine-tuning tone, clarity, or intention.

---

## 🤹‍♂️ Why I Built It

I wanted to get better at writing prompts — not just for coding, but for communication. This project became a sandbox where I could test how small tweaks changed everything.

It also gave me the chance to:
- Work with OpenAI's API
- Build something people could use instantly
- Practice real-world UX thinking and iteration

---

## 🧰 Tools Used

- Python
- Streamlit
- OpenAI API
- dotenv

---

## 🚀 Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/Frank-Ngo/prompt-playground.git
   cd prompt-playground
   ```

2. Install dependencies:
   ```bash
    pip install -r requirements.txt
   ```

3. Set up your .env file:
    ```ini
    OPENAI_API_KEY=your-api-key-here
    ```

4. Run the app
    ```bash
    streamlit run app.py
    ```



