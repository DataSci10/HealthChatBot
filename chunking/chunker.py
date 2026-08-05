from unstructured.chunking.basic import chunk_elements

def make_chunks(elements):
## Make chunks from elements
    chunks = chunk_elements(
        elements = elements)
# extract table elements
    table_elements = [
        ele for ele in chunks
        if ele.category in ["Table", "TableChunk"]
    ]
# extract text elements
    text_elements = [
        ele for ele in chunks
        if ele.category == "CompositeElement"
    ]

    text_data = [ele.text for ele in text_elements]

    table_data = [
        ele.metadata.text_as_html
        for ele in table_elements
    ]

    return text_data, table_data