import gradio as gr
import openai
import tempfile
import os
import scipy.io.wavfile

openai_api_key = os.getenv("OPENAI_API_KEY")

LANG_PROMPTS = {
    "English": (
        "You are an ICF-certified coaching assistant. "
        "You never give advice or instructions. Instead, you respond only with short, powerful, open-ended questions "
        "that help the client reflect and discover their own insights. Do not provide solutions, tips, or suggestions. "
        "Do not use more than 70 words in your reply. "
        "Reply in English."
    ),
    "Hindi": (
        "आप एक ICF-प्रमाणित कोचिंग असिस्टेंट हैं। आप कभी भी सलाह या निर्देश नहीं देते। "
        "इसके बजाय, आप केवल छोटे, शक्तिशाली, खुले-आम सवाल पूछते हैं जो क्लाइंट को विचार करने और अपनी अंतर्दृष्टि खोजने में मदद करते हैं। "
        "समाधान, सुझाव या टिप्स न दें। अपने उत्तर में 70 शब्दों से अधिक न लिखें। "
        "हमेशा हिंदी में उत्तर दें।"
    ),
    "Kannada": (
        "ನೀವು ICF ಪ್ರಮಾಣಿತ ಕೋಚಿಂಗ್ ಸಹಾಯಕನಾಗಿದ್ದೀರಿ. ನೀವು ಎಂದಿಗೂ ಸಲಹೆ ಅಥವಾ ನಿರ್ದೇಶನಗಳನ್ನು ನೀಡುವುದಿಲ್ಲ. "
        "ಬದಲಾಗಿ, ನೀವು ಕೇವಲ ಚಿಕ್ಕ, ಶಕ್ತಿಶಾಲಿ, ತೆರೆಯಲ್ಪಟ್ಟ ಪ್ರಶ್ನೆಗಳನ್ನು ಕೇಳುತ್ತೀರಿ "
        "ಅವು ಕ್ಲೈಂಟ್ ಅವರನ್ನು ಚಿಂತಿಸಲು ಮತ್ತು ತಮ್ಮ ಅನ್ವೇಷಣೆಗಳನ್ನು ಕಂಡುಹಿಡಿಯಲು ಸಹಾಯ ಮಾಡುತ್ತವೆ. "
        "ಪರಿಹಾರ, ಸಲಹೆ ಅಥವಾ ಟಿಪ್ಪಣಿಗಳನ್ನು ನೀಡಬೇಡಿ. ನಿಮ್ಮ ಉತ್ತರದಲ್ಲಿ 70 ಪದಗಳನ್ನು ಮೀರಬೇಡಿ. "
        "ಯಾವಾಗಲು ಕನ್ನಡದಲ್ಲಿ ಉತ್ತರಿಸಿ."
    )
}

def transcribe(audio):
    if audio is None:
        return ""
    sr, audio_data = audio
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        scipy.io.wavfile.write(temp_wav.name, sr, audio_data)
        temp_wav.flush()
        temp_wav_name = temp_wav.name
    client = openai.OpenAI(api_key=openai_api_key)
    with open(temp_wav_name, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        ).text
    os.remove(temp_wav_name)
    return transcript

def ask_gpt(conversation):
    client = openai.OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=120,
        temperature=0.7
    )
    return response.choices[0].message.content

def tts(text):
    if not text:
        return None
    client = openai.OpenAI(api_key=openai_api_key)
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",  # Nova supports multilingual output
        input=text
    )
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as out_f:
        out_f.write(response.content)
        tts_path = out_f.name
    return tts_path

def add_user_message(transcript, conversation, lang):
    if not conversation:
        conversation = [{"role": "system", "content": LANG_PROMPTS[lang]}]
    conversation.append({"role": "user", "content": transcript})
    return conversation

def add_assistant_message(response, conversation):
    conversation.append({"role": "assistant", "content": response})
    return conversation

def reset_conversation():
    return [], "", "", None, None, "English"

def chat_step(transcript, conversation, lang):
    conversation = add_user_message(transcript, conversation, lang)
    ai_response = ask_gpt(conversation)
    conversation = add_assistant_message(ai_response, conversation)
    audio_path = tts(ai_response)
    chat_text = "\n".join([
        f"{m['role']}: {m['content']}" for m in conversation if m['role'] != "system"
    ])
    return audio_path, conversation, chat_text, None

with gr.Blocks() as demo:
    gr.Markdown("# 🗣️ AI Coaching Assistant (ICF Style)\nSpeak, reflect, and hear a coach's question. The context continues until you end the session.")
    gr.Markdown("**Note:** After recording, please close the microphone window to continue.")

    conversation_state = gr.State([])
    language_state = gr.State("English")

    with gr.Row():
        # Left column: User
        with gr.Column(scale=1):
            gr.Markdown("### You (Coachee)")
            language_selector = gr.Dropdown(
                choices=["English", "Hindi", "Kannada"],
                value="English",
                label="Choose language for conversation"
            )
            audio_input = gr.Audio(
                sources=["microphone"],
                type="numpy",
                label="Record your message",
                show_label=True
            )
            transcript = gr.Textbox(label="Transcript (editable, correct if needed)", lines=3)
            submit_btn = gr.Button("Submit")

        # Right column: Coach
        with gr.Column(scale=1):
            gr.Markdown("### Coach")
            ai_voice = gr.Audio(label="Coach Reads Question", interactive=False)
            chat_history = gr.Textbox(label="Conversation so far", interactive=False, lines=8)
            end_session_btn = gr.Button("End Session", variant="stop")

    # Auto-transcribe after recording
    audio_input.change(
        fn=transcribe,
        inputs=audio_input,
        outputs=transcript
    )

    # User reviews/edits transcript, selects language, then submits for coaching response and voice
    submit_btn.click(
        fn=chat_step,
        inputs=[transcript, conversation_state, language_selector],
        outputs=[ai_voice, conversation_state, chat_history, audio_input]
    )

    # Update language state when dropdown changes
    language_selector.change(
        fn=lambda lang: lang,
        inputs=language_selector,
        outputs=language_state
    )

    end_session_btn.click(
        fn=reset_conversation,
        inputs=None,
        outputs=[conversation_state, chat_history, transcript, ai_voice, language_selector]
    )

demo.launch()
