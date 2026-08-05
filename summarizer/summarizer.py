from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

template = """
Your task is to create detailed and concise summary of given table & text.

provide clear summary of given table or text chunk.

Chunk:
{chunk}
"""

prompt = PromptTemplate(
    input_variables=["chunk"],
    template=template
)

llm = OpenAI()

summary_chain = prompt | llm


def summarize_text(text_data):

    return summary_chain.batch(text_data)


def summarize_tables(table_data):

    return summary_chain.batch(table_data)

# test12