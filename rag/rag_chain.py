import logging
from config import settings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)

template = """
Answer the question based only on the following context.

If the question cannot be answered using the information provided answer with "I don't know".

Context:
{context}

Question:
{que}
"""

prompt = PromptTemplate(
    input_variables=["context", "que"],
    template=template
)

llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY)

from langchain_openai import ChatOpenAI


def log_input(question):
    logger.info("=" * 80)
    logger.info("RAG Request Started")
    logger.info("Question: %s", question)
    return question


def log_context(inputs):
    logger.info("Retriever completed")
    logger.info("Retrieved Context:\n%s", inputs["context"])
    return inputs


def log_prompt(prompt_value):
    logger.info("Prompt sent to LLM:\n%s", prompt_value.to_string())
    return prompt_value


def log_response(response):
    logger.info("LLM Response:\n%s", response)
    logger.info("RAG Request Finished")
    logger.info("=" * 80)
    return response


def build_chain(retriever):

    chain = (
        RunnableLambda(log_input)
        | {
            "context": retriever,
            "que": RunnablePassthrough(),
        }
        | RunnableLambda(log_context)
        | prompt
        | RunnableLambda(log_prompt)
        | llm
        | RunnableLambda(log_response)
    )

    return chain