import glob
from unstructured.partition.pdf import partition_pdf
from config import settings
def load_documents():

    docs = []
    pdf_files = glob.glob(settings.DOCUMENT_PATH)
    for pdf in pdf_files:
        elements = partition_pdf(
            filename=pdf,
            strategy="hi_res",
            infer_table_structure=True,
            extract_images_in_pdf=False,
        )

        docs.extend(elements)

    return docs