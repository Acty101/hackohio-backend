from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os
import shutil
from dotenv import load_dotenv

load_dotenv()


class LangChainURL:
    """LangChain class to answer based on data found from URL"""

    def __init__(
        self,
        prompt: str,
        url: list[str] = [
            "https://www.a2gov.org/departments/trash-recycling/pages/recycling.aspx"
        ],
    ) -> None:
        # constants
        LLM_NAME = "gpt-3.5-turbo"
        PERSIST_DIRECTORY = "/tmp/chroma/"

        # Loading URL into a data variable
        loader = UnstructuredURLLoader(urls=url)
        data = loader.load()

        # Split the data into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10, chunk_overlap=5)
        splits = text_splitter.split_documents(data)
        # len(splits)

        # Create a persistent directory to store the vector database
        if os.path.isdir(PERSIST_DIRECTORY):
            # Clear directory if found
            shutil.rmtree(PERSIST_DIRECTORY)
        os.mkdir(PERSIST_DIRECTORY)

        # Create embeddings to use in the vectordb
        embedding = OpenAIEmbeddings()

        # Create the vectordb
        vectordb = Chroma.from_documents(
            documents=splits, embedding=embedding, persist_directory=PERSIST_DIRECTORY
        )

        # Create the llm
        llm = ChatOpenAI(model_name=LLM_NAME, temperature=0)

        # Create the prompt
        QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt)

        # Run the chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=vectordb.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
        )

    def infer(self, question: str) -> str:
        """Run inference on question"""
        return self.qa_chain({"query": question})["result"]
