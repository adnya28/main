"""
Multimodal LLMs - Project 2 - app.py: speak, and read the answer
-----------------------------------------------------------------
The input box is not a textbox any more - it is a microphone. That single
change is what "multimodal" means in a user interface.
Run from INSIDE this folder:  python app.py
"""

import gradio as gr
import chatbot                                               # our own logic file sitting next to this one

demo = gr.Interface(                                         # gr.Interface, not ChatInterface: one input, one output
    fn=chatbot.answer,
    inputs=gr.Audio(sources=["microphone", "upload"], type="filepath", label="Ask out loud"),
    outputs=gr.Textbox(label="What the model heard, and its answer", lines=6),
    title="Project 2 - audio in, text out",
    description=f"No speech-to-text step. The model listens itself. Now running on {chatbot.ai.label}.",
    flagging_mode="never")

if __name__ == "__main__":
    demo.launch(theme="soft")                      # opens http://127.0.0.1:7860