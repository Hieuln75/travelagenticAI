from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage
import os
import json


# Khởi tạo LLM (Đảm bảo bạn đã set biến môi trường GROQ_API_KEY)
llm = ChatGroq(
     temperature=0,
     model_name="llama-3.1-8b-instant",
     groq_api_key="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" # Hoặc để trong .env
)

def receptionist_agent(state):
    user_msg = state["messages"][-1].content

#     # Tạo prompt để ép model trả về thông tin cấu trúc
    prompt = f"""
    Phân tích yêu cầu du lịch sau của khách hàng: "{user_msg}"
    Trả về kết quả dưới dạng JSON với 2 trường: 
    - destination: Tên địa điểm (ví dụ: Đà Lạt, Nha Trang)
    - duration: Số ngày đi (chỉ lấy số).
    Nếu không rõ, mặc định là destination: "Unknown" và duration: 3.
    """

    # Gọi Groq
    response = llm.invoke(prompt)
    
    # Ở đây chúng ta tạm thời parse thủ công hoặc dùng JsonOutputParser
    # Để đơn giản cho bạn chạy ngay:
    content = response.content.strip()
    
    try:
        data = json.loads(content)
        destination = data.get("destination", "Unknown")
        duration = data.get("duration", 3)
    except Exception:
        destination = "Unknown"
        duration = 3

    return {
        "next_step": "flight",
        "messages": [
            AIMessage(
                content=f"Đã ghi nhận chuyến đi tới {destination} trong {duration} ngày. Đang tìm chuyến bay."
            )
        ],
        "plan_data": {
            "destination": destination,
            "duration": duration
        }
    }

