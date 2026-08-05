import logging

from langchain_openai import OpenAIEmbeddings
from config import settings
from loaders.pdf_loader import load_documents
from chunking.chunker import make_chunks
from summarizer.summarizer import summarize_text, summarize_tables
from rag_retriever.retriever import build_retriever, add_documents

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


def ingest():

    logger.info("Step 1: Loading PDF documents")
    elements = load_documents()
    logger.info(f"{len(elements)} elements loaded")

    logger.info("Step 2: Chunking")
    text_data, table_data = make_chunks(elements)
    logger.info(f"Text Chunks: {len(text_data)}")
    logger.info(f"Table Chunks: {len(table_data)}")

    logger.info("Step 3: Generating summaries")
    text_summaries = summarize_text(text_data)
    table_summaries = summarize_tables(table_data)

    logger.info("Step 4: Building retriever")

    embedding_model = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)

    retriever = build_retriever(embedding_model)

    add_documents(
        retriever,
        text_data,
        table_data,
        text_summaries,
        table_summaries
    )

    logger.info("Documents successfully indexed.")


if __name__ == "__main__":
    ingest()