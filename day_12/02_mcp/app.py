import gradio  as gr
import chatbot

demo = gr.ChatInterface(
    fn=chatbot.anwser,
    title="Meridian bank's loan",
    description="You can provide interest rates and calculate EMIs for home, car, personal",
    examples=["What is the home loan rate today?",
              "What is the EMI on a 500,000 home loan for 20 years?"]
)

if __name__ =="__main__":
    demo.launch(theme=gr.themes.Soft())