from langchain_core.messages import AIMessage
from langchain_groq import ChatGroq
import json
import re

# ===============================
# INIT LLM (DÙNG CHUNG PATTERN)
# ===============================
llm = ChatGroq(
    temperature=0,
    model_name="llama-3.1-8b-instant",
    groq_api_key="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"  # demo thì hardcode, production để ENV
)

# ===============================
# HOTEL AGENT (LLM-BASED)
# ===============================
def hotel_agent(state):
    destination = state.get("plan_data", {}).get("destination", "Đà Lạt")
    duration = state.get("plan_data", {}).get("duration", 3)

    prompt = f"""
Bạn là trợ lý du lịch.

Người dùng đi du lịch:
- Điểm đến: {destination}
- Số ngày: {duration}

Hãy đề xuất 1 khách sạn phù hợp.

CHỈ trả về JSON hợp lệ.
KHÔNG markdown.
KHÔNG giải thích.
KHÔNG text ngoài JSON.

Schema:
{{
  "name": string,
  "location": string
}}
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
            "hotel": hotel
        },
        "next_step": "itinerary",
        "messages": [
            AIMessage(
                content=f"Đã chọn khách sạn {hotel['name']} tại {hotel['location']}"
            )
        ]
    }
