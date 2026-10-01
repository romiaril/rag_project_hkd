from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config


BASE = Path(__file__).resolve().parent


def get_store(rebuild=False):
    index_path = Path(config.INDEX_PATH)
    if not index_path.is_absolute():
        index_path = BASE / index_path

    embeddings = OpenAIEmbeddings(model=config.EMBED_MODEL)

    if (index_path / "index.faiss").is_file() and (index_path / "index.pkl").is_file() and not rebuild:
        return FAISS.load_local(
            str(index_path),
            embeddings,
            allow_dangerous_deserialization=True,
        )

    documents = PyPDFLoader(str(config.DOC_PATH)).load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)

    for document in chunks:
        document.metadata["filename"] = Path(config.DOC_PATH).name
        document.metadata["page_no"] = document.metadata.get("page", 0) + 1

    store = FAISS.from_documents(chunks, embeddings)
    store.save_local(str(index_path))
    return store
