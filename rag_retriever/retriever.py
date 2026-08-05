import uuid

from langchain_core.stores import InMemoryStore

from langchain_classic.retrievers.multi_vector import MultiVectorRetriever

from langchain_chroma import Chroma
from cache.redis_docstore import RedisDocStore
from langchain_core.documents import Document
from config import settings

def build_retriever(embedding_model):

    vectordb = Chroma(
        collection_name=settings.COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=settings.CHROMA_PATH,
    )

    # store = InMemoryStore()
    store = RedisDocStore(
    host="localhost",
    port=6379,
    db=0,
)
# 
    retriever = MultiVectorRetriever(
        vectorstore=vectordb,
        docstore=store,
        id_key="doc_id",
    )

    return retriever


def add_documents(retriever, text_data, table_data, text_summaries, table_summaries):

    table_ids = [str(uuid.uuid4()) for _ in table_summaries]

    table_docs = []

    for idx, summary in enumerate(table_summaries):

        table_docs.append(
            Document(
                page_content=summary,
                metadata={
                    "doc_id": table_ids[idx]
                }
            )
        )

    text_ids = [str(uuid.uuid4()) for _ in text_summaries]

    text_docs = []

    for idx, summary in enumerate(text_summaries):

        text_docs.append(
            Document(
                page_content=summary,
                metadata={
                    "doc_id": text_ids[idx]
                }
            )
        )

    retriever.vectorstore.add_documents(table_docs)
    retriever.vectorstore.add_documents(text_docs)

    retriever.docstore.mset(
        list(zip(table_ids, table_data))
    )

    retriever.docstore.mset(
        list(zip(text_ids, text_data))
    )

    return retriever