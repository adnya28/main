import os
import matplotlib.pyplot as plt 
import matplotlib; matplotlib.use('Agg')

import numpy as np
from sklearn.decomposition import PCA
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv
from pydantic import SecretStr
import gradio as gr

load_dotenv()

EMBEDDING_MODEL= os.environ["EMBEDDING_MODEL"]
BASE_URL= os.environ["BASE_URL"]

API_KEY = SecretStr(os.environ["OPENROUTER_API_KEY"])

embeddings =OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    base_url=BASE_URL,
    api_key= API_KEY,
    check_embedding_ctx_length=False 

)

def word_map(text):
    words = [w.strip() for w in text.split(",") if w.strip()]
    vectors =np.array(embeddings.embed_documents(words))
    xy=PCA(n_components=3).fit_transform(vectors)
    flg, ax=plt.subplots()
    for word,point in zip(words,xy):
        ax.scatter(point[0], point[1], color="purple")
        ax.annotate(word,point)
    return flg

# 
demo = gr.Interface(
    word_map,
    gr.Textbox(label="Words (comma separated)", value="king, queen, man, women, cycle, bike,car, truck"),
    gr.Plot(),
    title="word Map-close dots mean similar meaning"
    )

if __name__ == "__main__":
    demo.launch()