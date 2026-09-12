"""
Multimodal LLMs - Project 1 - app.py: the text chatbot as a web page
---------------------------------------------------------------------
All the thinking is in chatbot.py; this file is only the page.
Run from INSIDE this folder:  python app.py
"""

import gradio as gr                                          # turns a Python function into a local web page
import chatbot                                               # our own logic file sitting next to this one

demo = gr.ChatInterface(                                     # a ready-made chat window wrapped around one function
    fn=chatbot.answer,                                       # every message the user types goes to chatbot.answer
    title="Project 1 - text in, text out",
    description=f"One modality. Now running on {chatbot.ai.label}. Type a question - that is all this box accepts.",
    examples=["What is an EMI?",
              "Explain a floating interest rate to a first-time borrower.",
              "What documents does a home loan application need?"])

if __name__ == "__main__":
    demo.launch(theme="soft")                      # opens http://127.0.0.1:7860