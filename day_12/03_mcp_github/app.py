import gradio  as gr
import chatbot

demo = gr.ChatInterface(
    fn=chatbot.anwser,
    title="MCP Client for Github copilot",
    description="You can provide information for Github Copilot",
    examples=["Who am I on Github?",
              "how many public repositories do I have?"]
)

if __name__ =="__main__":
    demo.launch(theme=gr.themes.Soft())
