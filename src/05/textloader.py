from langchain_community.document_loaders import TextLoader

loader = TextLoader(
    "../../data/notice.txt", 
    encoding="utf-8"
)

documents = loader.load()
print(f"문서 길이 => {len(documents)}")
print()
print(f"문서 내용 =>\n {documents[0].page_content}")
print()
print(f"메타 =>\n {documents[0].metadata}")