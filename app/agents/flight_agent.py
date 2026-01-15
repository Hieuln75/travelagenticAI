from langchain_core.messages import AIMessage
from langchain_groq import ChatGroq
import json
import re
import os

# ===============================
# INIT LLM (GIỐNG receptionist)
# ===============================

llm = ChatGroq(
     temperature=0,
     model_name="llama-3.1-8b-instant",
     groq_api_key="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" # Hoặc để trong .env
)


# ===============================
# FLIGHT AGENT
# ===============================
def flight_agent(state):
    plan = state.get("plan_data", {})
    destination = plan.get("destination", "Unknown")
    duration = plan.get("duration", 3)

    prompt = f"""
Bạn là một dịch vụ backend, KHÔNG phải trợ lý tư vấn.

Nhiệm vụ: chọn CHÍNH XÁC MỘT chuyến bay tốt nhất.

Thông tin chuyến đi:
- Điểm đến: {destination}
- Số ngày: {duration}

QUY ĐỊNH BẮT BUỘC (vi phạm = lỗi):
- Chỉ trả về JSON hợp lệ
- KHÔNG dùng mảng
- KHÔNG đổi tên field
- KHÔNG dịch sang tiếng Việt
- KHÔNG thêm field
- KHÔNG giải thích
- KHÔNG markdown
- KHÔNG text ngoài JSON

SCHEMA DUY NHẤT HỢP LỆ:
{{
  "code": "string",
  "arrival": "string"
}}

"""

    response = llm.invoke(prompt)
    raw = response.content.strip()

    # ===============================
    # PARSE JSON
    # ===============================
    try:
        flight_data = json.loads(raw)
    except json.JSONDecodeError:
        # fallback: LLM trả bẩn
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise ValueError(f"Không parse được flight JSON: {raw}")
        flight_data = json.loads(match.group())

    # ===============================
    # VALIDATE TỐI THIỂU
    # ===============================
    if "code" not in flight_data or "arrival" not in flight_data:
        raise ValueError(f"Flight JSON thiếu field: {flight_data}")

    return {
        "plan_data": {
            **plan,
            "flight": flight_data
        },
        "next_step": "hotel",
        "messages": [
            AIMessage(
                content=f"✈️ Đã tìm chuyến bay {flight_data['code']} – hạ cánh lúc {flight_data['arrival']}"
            )
        ]
    }



# rem code cũ

# from langchain_core.messages import AIMessage

# def flight_agent(state):
#    return {
#        "plan_data": {
#            "flight": {
#                "code": "VN123",
#                "arrival": "10:00"
#            }
#        },
#        "next_step": "hotel",
#        "messages": [
#            AIMessage(content="Đã tìm chuyến bay, hạ cánh lúc 10:00")
#        ]
#    }
