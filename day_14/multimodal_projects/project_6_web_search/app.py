"""
Multimodal LLMs - Project 6 - app.py: the chatbot that reads today's news
--------------------------------------------------------------------------
Back to an ordinary chat window - which is the point. Nothing about the page
changed except one checkbox; the model simply gained the ability to look
things up, and the toggle lets you take it away again.
Run from INSIDE this folder:  python app.py
"""

import gradio as gr
import chatbot                                               # our own logic file sitting next to this one

demo = gr.ChatInterface(
    fn=chatbot.answer,                                       # (message, history, search_on) - the checkbox is arg 3
    title="Project 6 - a model with web search",
    description=f"Ask about something that happened after the model was trained. {chatbot.ai.label}, search: {chatbot.ai.web_search}.",
    additional_inputs=[gr.Checkbox(value=True, label="Search the web",
                                   info="Untick to answer from training memory alone")],
    additional_inputs_accordion=gr.Accordion("Options", open=True),   # open, so the toggle is on screen not hidden
    examples=[["What is the RBI repo rate right now?", True],        # same question, ticked ...
              ["What is the RBI repo rate right now?", False],       # ... and unticked: that contrast is the demo
              ["What did the RBI announce at its most recent policy meeting?", True]])

if __name__ == "__main__":
    demo.launch(theme="soft")
