from controllers import example_controller
from fastapi import APIRouter
from handlers.errors import has_errors
from typing import Union
from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
import sys
import os

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
def read_root():
    return construct_index(docsPath)


@example_router.get("/")
def read_item(q: Union[str, None] = None):
    return chatbot(q) 

