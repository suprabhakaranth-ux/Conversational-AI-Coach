# 🧘 AI Coaching Assistant (ICF-Style Conversational AI)

An AI-powered reflective coaching assistant built using OpenAI APIs, multilingual prompting, voice interaction, and conversational memory.

The application simulates an ICF-style coaching interaction where the assistant avoids giving direct advice and instead responds using reflective, open-ended coaching questions.

---

# Demo

## 🎥 Product Demo

[Watch Demo Video](./demo.mp4)

Recommended:

* Upload your MP4 to GitHub Releases, YouTube (unlisted/public), or Loom
* Embed a GIF preview in README
* Add screenshots below

Example:

```md
![AI Coach Demo](assets/demo.gif)
```

---

# Problem Statement

Most conversational AI assistants are optimized for:

* answering questions
* giving advice
* solving tasks

Professional coaching works differently.

ICF-style coaching focuses on:

* reflective listening
* self-discovery
* open-ended questioning
* emotional processing
* insight generation

This project explores how conversational AI can simulate a reflective coaching experience using structured prompting, voice interfaces, and multilingual conversational flow.

---

# Features

## 🎙️ Voice-Based Coaching

* Record speech directly from microphone
* AI transcribes using Whisper
* Editable transcript before submission
* AI responds with generated voice

## 🧠 Context-Aware Conversations

* Maintains conversational memory across session
* Multi-turn coaching flow
* Reflective questioning behavior

## 🌍 Multilingual Support

Supports:

* English
* Hindi
* Kannada

## 🔊 AI Voice Output

* OpenAI TTS integration
* Natural spoken coaching responses

## 🧭 Coaching Constraints

The assistant is intentionally constrained to:

* avoid giving advice
* avoid direct solutions
* ask open-ended reflective questions
* maintain concise coaching responses

---

# Tech Stack

| Layer             | Technology          |
| ----------------- | ------------------- |
| Frontend UI       | Gradio              |
| Speech-to-Text    | OpenAI Whisper      |
| Conversational AI | OpenAI GPT          |
| Text-to-Speech    | OpenAI TTS          |
| Deployment        | Hugging Face Spaces |
| Language          | Python              |

---

# Architecture Overview

```text
User Speech
   ↓
Whisper Transcription
   ↓
Editable Transcript Layer
   ↓
Prompt-Engineered Coaching System
   ↓
GPT Conversational Response
   ↓
OpenAI TTS Voice Generation
   ↓
Audio Coaching Reply
```

---

# Prompt Engineering Approach

The coaching layer was designed with strict behavioral constraints.

Core prompt objectives:

* never provide direct advice
* never instruct the user what to do
* respond only through reflective questioning
* simulate ICF-style coaching presence
* maintain brevity and conversational clarity

Example behaviors:

✅ "What feels most important about this situation for you right now?"

❌ "You should communicate more clearly with your manager."

---

# Example Interaction

## User

> I feel stuck in my career and I don't know whether I should quit.

## AI Coach

> What part of your current situation feels most emotionally draining to you?

---

# Screenshots

## Main Interface

*Add screenshot here*

## Voice Interaction

*Add screenshot here*

## Multilingual Coaching

*Add screenshot here*

---

# Deployment

## Hugging Face Spaces

This project was designed for deployment using Hugging Face Spaces with Gradio.

Environment variables required:

```bash
OPENAI_API_KEY=your_key_here
```

---

# Installation

```bash
git clone <your-repo-url>
cd ai-coaching-assistant
pip install -r requirements.txt
python app.py
```

---

# Future Improvements

Potential future enhancements:

* persistent user sessions
* vector memory/RAG
* emotional state tracking
* coaching analytics dashboard
* conversation summaries
* custom coach personalities
* live streaming voice conversations
* local/open-source model support
* mobile responsive UI

---

# Key Learnings

This project helped explore:

* conversational AI design
* prompt engineering constraints
* voice AI workflows
* multilingual prompting
* AI interaction UX
* session management
* AI behavior shaping
* human-centered conversational systems

---

# Why This Project Matters

Most AI applications optimize for:

* speed
* direct answers
* automation

This project instead experiments with:

* reflection
* conversational pacing
* guided self-discovery
* emotionally-aware interaction patterns

The goal was to explore whether AI can facilitate reflective dialogue rather than simply provide solutions.

---

# Repository Structure

```text
.
├── app.py
├── requirements.txt
├── README.md
├── assets/
│   ├── demo.gif
│   ├── screenshots/
│   └── architecture.png
```

---

# Author

Built as an experimental conversational AI project exploring reflective coaching workflows using large language models, voice interfaces, and multilingual conversational systems.

---

# License

MIT License
