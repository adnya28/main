"""
Multimodal LLMs - Project 4 - app.py: upload a picture and ask about it
------------------------------------------------------------------------
Two inputs this time - an image and a question - because a picture on its own
is not a request. Try a screenshot, a payslip, a whiteboard, a handwritten form.
Run from INSIDE this folder:  python app.py
"""

import gradio as gr
import chatbot                                               # our own logic file sitting next to this one

demo = gr.Interface(
    fn=chatbot.answer,
    inputs=[gr.Image(type="filepath", label="The image"),
            gr.Textbox(label="Your question about it", value="What is the car loan rate?")],
    outputs=gr.Textbox(label="Answer only from the image, your are an expert debugger and you have to provide the solution fro the same", lines=5),
    title="Project 4 - image in, text out",
    description=f"The image is sent as a data URL inside the message. Now running on {chatbot.ai.label}.",
    flagging_mode="never")

if __name__ == "__main__":
    demo.launch(theme="soft")