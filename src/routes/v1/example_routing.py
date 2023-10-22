from controllers import example_controller
from fastapi import APIRouter
from handlers.errors import has_errors
from typing import Union
from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
import sys
import os
import json
import openai
import re


openai.api_key = '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'

os.environ["OPENAI_API_KEY"] = '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'
example_router = APIRouter()
tags = ['example'] 
diretorio_atual = os.path.dirname(__file__)
caminho_relativo = os.path.join(diretorio_atual, "index.json")
docsPath = os.path.join(diretorio_atual, "docs")
indexDocs = ""

def construct_index(directory_path):
    global indexDocs
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.2, model_name="text-embedding-ada-002", max_tokens=num_outputs))
    documents = SimpleDirectoryReader(directory_path).load_data()
    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index.save_to_disk(caminho_relativo)
    indexDocs = GPTSimpleVectorIndex.load_from_disk(caminho_relativo)
    return "Training finished"

def chatbot(input_text):
    response = indexDocs.query(input_text, response_mode="compact")
    return response.response


@example_router.get("/training")
async def read_root():
    construct_index(docsPath)
    return "Training..."


@example_router.get("/gpt/assistant")
def read_question(q: Union[str, None] = None):
    prompt = (
        "Classify the text into question or request\n"
        f"text: {q}"
    )
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0,
        max_tokens=20,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    response_message = response["choices"][0]["message"]["content"]

    if response_message == 'question':
        return json.dumps({
            "action": "print",
            "message": chatbot(q)
        })
    else:
        prompt = (
        "Classify the text into insights, payments, reconciliations, connections, routing, checkout-builder or developers\n"
        "context: We are a payment orchestration company where every category is a dashboard section\n"
        f"text: {q}\n"
        "section:"
        )
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0,
            max_tokens=20,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        response_message = response["choices"][0]["message"]["content"]

        if response_message != 'payments':
            response = {
                "action": "redirect",
                "url": "/{response_message}"
            }
            return json.dumps(response)
        else:
            # Regular expression pattern for UUID
            pattern = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}"

            # Find all matches in the text
            matches = re.findall(pattern, q)

            if len(matches) > 0:
                response = {
                    "action": "find",
                    "payments": matches
                }
                return json.dumps(response)
    
    return "I don't understand your request"

