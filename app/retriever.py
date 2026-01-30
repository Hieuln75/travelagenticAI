from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Khởi tạo embedding model (miễn phí, chạy cục bộ)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Giả sử bạn đã có dữ liệu trong thư mục ./db
vector_db = Chroma(persist_directory="./db", embedding_function=embeddings)

def get_relevant_info(query: str, category: str):
    # Tìm kiếm theo category (hotel/flight) và nội dung
    docs = vector_db.similarity_search(f"{category}: {query}", k=2)
    return "\n".join([d.page_content for d in docs])
def search_rag(query: str, category: str):
    return get_relevant_info(query, category)
