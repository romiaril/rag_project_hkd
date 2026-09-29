from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader(
    "../../data/notice.txt", 
    encoding="utf-8"
)

documents = loader.load()

# 문서를 청크로 나누기 
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 150,
    chunk_overlap = 30,
)

chuncks = splitter.split_documents(documents)
print("="*50)
print(f" chunk 갯수 => {len(chuncks)}")
for i, chunck in enumerate(chuncks, 1):
    print(f"[{i}] \n {chunck.page_content}")
    print()


