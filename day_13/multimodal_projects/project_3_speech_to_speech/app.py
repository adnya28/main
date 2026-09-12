"""
Multimodal LLMs - Project 3 - app.py: talk to it, and it talks back
--------------------------------------------------------------------
Microphone in, speaker out. The text box in the middle is there on purpose, so
the class can see the words the two models pass between them.
Run from INSIDE this folder:  python app.py
"""

import gradio as gr
import chatbot                                               # our own logic file sitting next to this one

demo = gr.Interface(
    fn=chatbot.answer,
    inputs=gr.Audio(sources=["microphone", "upload"], type="filepath", label="Speak"),
    outputs=[gr.Textbox(label="What it decided to say", lines=3),   # the seam between the two models
             gr.Audio(label="Hear it", autoplay=True)],
    title="Project 3 - audio in, audio out",
    description=f"Two models in a row: {chatbot.ai.label} listens and answers, gTTS speaks.",
    flagging_mode="never")

if __name__ == "__main__":
    demo.launch(theme="soft")