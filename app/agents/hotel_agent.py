from langchain_core.messages import AIMessage
from langchain_groq import ChatGroq
from app.retriever import search_rag
import json
import re
import os
# ===============================
# INIT LLM (DÙNG CHUNG PATTERN)
# ===============================
llm = ChatGroq(
    temperature=0,
    model_name="llama-3.1-8b-instant",
    groq_api_key=os.environ["GROQ_API_KEY"]
)

# ===============================
# HOTEL AGENT (LLM-BASED)
# ===============================
def hotel_agent(state):
    destination = state.get("plan_data", {}).get("destination", "Đà Lạt")
    duration = state.get("plan_data", {}).get("duration", 3)
    context = search_rag(destination, "hotel")

    prompt = f"""
Bạn là trợ lý du lịch.

Người dùng đi du lịch:
- Điểm đến: {destination}
- Số ngày: {duration}
Dữ liệu từ database (có thể rỗng):
{context}

NHIỆM VỤ:
- Chọn đúng 1 khách sạn phù hợp tại {destination}.
- Nếu database có khách sạn tại {destination}, chọn từ database.
- Nếu database không có, tự chọn 1 khách sạn phổ biến tại {destination}.
- KHÔNG trả về nhiều lựa chọn.
- KHÔNG trả về thông tin khác ngoài khách sạn.

CHỈ trả về JSON đúng schema sau.
BẮT BUỘC đúng schema, không thêm field.

Schema:
{{
  "name": string,
  "location": string
}}
KHÔNG markdown.
KHÔNG giải thích.
KHÔNG text ngoài JSON.
"""

    response = llm.invoke(prompt)
    raw = response.content.strip()

    # ===============================
    # PARSE JSON AN TOÀN
    # ===============================
    try:
        hotel = json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise ValueError(f"Không parse được hotel JSON: {raw}")
        hotel = json.loads(match.group())

    if "name" not in hotel or "location" not in hotel:
        raise ValueError(f"Hotel JSON thiếu field: {hotel}")

    return {
        "plan_data": {
            **state.get("plan_data", {}),
            "hotel": hotel
        },
        "next_step": "itinerary",
        "messages": [
            AIMessage(
                content=f"Đã chọn khách sạn {hotel['name']} tại {hotel['location']}"
            )
        ]
    }
