"""
Multimodal LLMs - config.py: every provider, in one file
---------------------------------------------------------
This is the only file that knows a provider exists. Change a model here and all
seven projects follow. Add a provider by adding a block - no other file changes.

The API KEYS themselves stay in the .env, which is never committed; this file
only says which key belongs to which provider.

In any chatbot.py:                ai = use("openrouter")
"""

import os
from types import SimpleNamespace
from dotenv import load_dotenv                               # loads the .env sitting two folders above
from openai import OpenAI                                    # ONE SDK - all three speak its wire format

load_dotenv()

PROVIDERS = {
    "openrouter": {
        "base_url":    "https://openrouter.ai/api/v1",
        "api_key":     os.getenv("OPENROUTER_API_KEY"),      # https://openrouter.ai/keys
        "model":       "google/gemini-2.5-flash",            # text + vision + audio
        "audio":       True,                                 # can this model listen? (projects 2 and 3)
        "image_model": "google/gemini-2.5-flash-image",      # project 5 only
        "web_search":  "native",                             # project 6: ":online", the provider searches
    },
    "google": {
        "base_url":    "https://generativelanguage.googleapis.com/v1beta/openai/",
        "api_key":     os.getenv("GOOGLE_API_KEY"),          # https://aistudio.google.com/apikey
        "model":       "gemma-4-31b-it",                     # open model, generous free limits, text + vision
        "audio":       False,                                # Gemma cannot listen: "Audio input modality not enabled"
        "image_model": None,                                 # the free tier allows zero images anyway (limit: 0)
        "web_search":  "ddgs",                               # project 6: we search ourselves
    },
    "ollama": {
        "base_url":    "http://localhost:11434/v1",          # this laptop -  ollama pull gemma4:e2b
        "api_key":     "ollama-needs-no-key",                # nothing to authenticate, but the SDK wants a value
        "model":       "gemma4:e2b",                         # one 7 GB pull: text + vision + audio + tools
        "audio":       True,
        "image_model": None,                                 # Ollama serves no image models
        "web_search":  "ddgs",
    },
}


def use(name: str):
    """Hand back the provider called `name`, ready to use: .client .model .label ..."""
    name = os.getenv("FORCE_PROVIDER", name)                 # only check_providers.py sets this; normally ignored
    if name not in PROVIDERS:
        raise SystemExit(f"Unknown provider {name!r}. config.py knows: {', '.join(PROVIDERS)}")
    conf = PROVIDERS[name]
    if not conf["api_key"]:
        raise SystemExit(f"Provider {name!r} needs its API key set in the .env")
    return SimpleNamespace(
        name=name,
        client=OpenAI(base_url=conf["base_url"], api_key=conf["api_key"]),
        model=conf["model"],
        audio=conf["audio"],
        image_model=conf["image_model"],
        web_search=conf["web_search"],
        label=f"{name}: {conf['model']}")


def text_of(reply) -> str:
    """The words out of a reply. Some models (Gemma) narrate their reasoning in
    <thought> tags inside the content - students should not see that, so drop it."""
    content = reply.choices[0].message.content or ""         # content can be None: a refusal, or a filter
    return content.split("</thought>")[-1].strip()
