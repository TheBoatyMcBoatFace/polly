"""
From: https://gpt-index.readthedocs.io/en/latest/guides/primer/usage_pattern.html#parse-the-documents-into-nodes
"""
import os
import sys
# from llama_index import download_loader, SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper

from llama_index.readers.download import download_loader
from llama_index.readers.file.base import SimpleDirectoryReader
from llama_index.node_parser import SimpleNodeParser
from llama_index import GPTVectorStoreIndex


# from llama_index.indices.prompt_helper import PromptHelper

# from llama_index.indices.vector_store.base import GPTVectorStoreIndex
# from llama_index.llm_predictor.base import LLMPredictor

from langchain.chat_models import ChatOpenAI
from logger import logger

print(sys.path)

os.environ["OPENAI_API_KEY"] = ''

file_path = input('Enter the path of the file/doc: ')
# file_path = 'samples/handbook.txt'
logger.info(f'Importing content of: {file_path}')


# Get the Data for Documents
documents = SimpleDirectoryReader(input_files=[file_path]).load_data()

# Make Nodes from Docs
parser = SimpleNodeParser()
nodes = parser.get_nodes_from_documents(documents)
logger.debug(f'Nodes: {nodes}')

# Index Construction
index = GPTVectorStoreIndex(nodes)






# def build_index(file_path):
 #   max_input_size = 4096
 #   num_outputs = 512
 #   max_chunk_overlap = 20
 #   chunk_size_limit = 256

   #  prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

   #  llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs))








  #  download_loader('SimpleDirectoryReader')
  #  documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
    # index = GPTVectorStoreIndex.from_documents(documents)
  #  index = GPTVectorStoreIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
  #  return index


# index = build_index(file_path=file_path)


def chatbot(prompt):
    return index.query(prompt, response_mode="compact")


while True:
    print('########################################')
    pt = input('ASK: ')
    if pt.lower()=='end':
        break
    response = chatbot(pt)
    print('----------------------------------------')
    print('ChatGPT says: ')
    print(response)