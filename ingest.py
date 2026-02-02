from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import os

def run_ingest():
    # 1. Khởi tạo mô hình Embedding (chạy local trên máy bạn)
    print("Đang khởi tạo Embedding model (lần đầu sẽ hơi chậm)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 2. Đọc dữ liệu từ file text
    with open("travel_data.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    documents = []
    for line in lines:
        if line.strip():
            # Tách metadata đơn giản dựa trên nhãn [HOTEL] hoặc [FLIGHT]
            category = "hotel" if "[HOTEL]" in line else "flight"
            doc = Document(
                page_content=line.replace("[HOTEL]", "").replace("[FLIGHT]", "").strip(),
                metadata={"category": category}
            )
            documents.append(doc)

    # 3. Lưu vào Vector DB (thư mục ./db_travel)
    print(f"Đang nạp {len(documents)} dữ liệu vào database...")
    vector_db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="./db"
    )
    print("Thành công! Dữ liệu đã được lưu vào thư mục ./db_travel")

if __name__ == "__main__":
    run_ingest()