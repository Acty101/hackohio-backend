from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS
from langchain.indexes import VectorstoreIndexCreator
from collections import defaultdict
from typing import List
import os
import shutil
from enum import Enum


class LangChainOutput(Enum):
    ITEM = 0
    SUPERCATEGORY = 1
    INSTRUCTIONS = 2


class LangChainURL:
    """LangChain class to answer based on data found from URL"""

    def __init__(
        self,
        prompt: str,
        url: List[str] = [
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
        #vectordb = Chroma.from_documents(
        #    documents=splits, embedding=embedding, persist_directory=PERSIST_DIRECTORY
        #)

        vectordb = FAISS.from_documents(
            documents = splits, embedding = embedding
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

    def infer(self, question: List[str]) -> List[dict]:
        """Run inference on question"""

        # {LangChainOutput.ITEM: str, LangChainOutput.SUPERCATEGORY: str }
        self.sc_count = defaultdict(int)
        questionStr = ", ".join(question)
        output = self.qa_chain({"query": questionStr})["result"]
        outputList = output.split("\n")
        objList = []
        for str in outputList:
            list = str.split("~")
            temp = {
                LangChainOutput.ITEM: list[0],
                LangChainOutput.SUPERCATEGORY: list[1],
                LangChainOutput.INSTRUCTIONS: list[2],
            }
            self.sc_count[list[1]] += 1
            objList.append(temp)
        return objList
