"""
Multimodal LLMs - Project 5 - app.py: describe a picture and get one
----------------------------------------------------------------------
The mirror image of project 4: text goes in, and the picture comes out.
Run from INSIDE this folder:  python app.py
"""

import gradio as gr
import chatbot                                               # our own logic file sitting next to this one

demo = gr.Interface(
    fn=chatbot.answer,
    inputs=gr.Textbox(label="Describe the picture you want", lines=3),
    outputs=[gr.Textbox(label="What the model said about it", lines=2),
             gr.Image(label="The generated image")],
    title="Project 5 - text in, image out",
    description=f"Text goes in, a picture comes out. Pinned to {chatbot.ai.name}: {chatbot.ai.image_model} - this project ignores PROVIDER.",
    examples=["A clean flat-style icon of a house with a rupee coin beside it, for a home loan web page.",
              "A simple line-art illustration of a bank branch, plain white background.",
              "A friendly cartoon rupee coin wearing a hard hat, for a construction loan advert."],
    flagging_mode="never")

if __name__ == "__main__":
    demo.launch(theme="soft")