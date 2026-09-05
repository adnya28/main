import gradio as gr
from chatbot import get_streaming_response, DOCUMENT_PATH


def chat_interface(message, history):
    response_text = ""

    for kind, text in get_streaming_response(message):
        if kind == "response":
            response_text += text
            yield response_text

rag_text = gr.ChatInterface(
    fn=chat_interface,
    title="Caramel AI - Text Document RAG BOT",
    description=f"Ask questions about the content of the loaded document: {DOCUMENT_PATH}"
)

if __name__ == "__main__":
    rag_text.launch()