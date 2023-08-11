from dotenv import load_dotenv
import os
from logger import logger
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from llama_index import download_loader
load_dotenv()
download_loader("GithubRepositoryReader")
from llama_index.readers.llamahub_modules.github_repo import (
    GithubRepositoryReader, GithubClient)


os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["GITHUB_TOKEN"] = os.getenv('GITHUB_TOKEN')
github_client = GithubClient(os.getenv("GITHUB_TOKEN"))


def load_documents():
    loader = GithubRepositoryReader(
        github_client,
        owner="CivicActions",
        repo="guidebook",
        filter_file_extensions=([
            ".md"], GithubRepositoryReader.FilterType.INCLUDE),
        concurrent_requests=10,
    )

    documents = loader.load_data(branch="master")
    for doc in documents:
        logger.debug(doc.extra_info)

    documents = [doc.to_langchain_format() for doc in documents]
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    retriever = FAISS.from_documents(documents, embeddings).as_retriever(k=4)
    return retriever


llm = ChatOpenAI(temperature=1, model_name="gpt-4", max_tokens=4096,
                 streaming=True)

memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    return_messages=True,
    k=6
)

retriever = load_documents()

conversation = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    verbose=False,
    memory=memory,
    max_tokens_limit=4096
)


def chatbot(pt):
    res = conversation({'question': pt})['answer']
    return res


def reset():
    global retriever
    global conversation
    retriever = load_documents()
    conversation = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        verbose=False,
        memory=memory,
        max_tokens_limit=4096
    )


if __name__ == '__main__':
    while True:
        print('########################################\n')
        pt = input('ASK: ')
        if pt.lower() == 'end':
            logger.info('Ending chat session.')
            break
        response = chatbot(pt)
        print('\n----------------------------------------\n')
        print('ChatGPT says: \n')
        print(response, '\n')
