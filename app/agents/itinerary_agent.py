from langchain_core.messages import AIMessage
from langchain_groq import ChatGroq
import json
import re
import os

# ===============================
# INIT LLM (GIỐNG CÁC AGENT KHÁC)
# ===============================
llm = ChatGroq(
    temperature=0,
    model_name="llama-3.1-8b-instant",
    groq_api_key="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" # Hoặc để trong .env
)

# ===============================
# ITINERARY AGENT
# ===============================
def itinerary_agent(state):
    plan_data = state.get("plan_data", {})
    flight = plan_data.get("flight", {})
    hotel = plan_data.get("hotel", {})
    destination = plan_data.get("destination", "Unknown")
    duration = plan_data.get("duration", 3)

    prompt = f"""
Bạn là trợ lý du lịch.

Thông tin đã có:
- Điểm đến: {destination}
- Số ngày: {duration}
- Chuyến bay: {flight}
- Khách sạn: {hotel}

Hãy tạo lịch trình du lịch đơn giản.

CHỈ trả về JSON hợp lệ.
KHÔNG giải thích.
KHÔNG markdown.
KHÔNG text ngoài JSON.

Schema:
{{
  "itinerary": string
}}
"""

    response = llm.invoke(prompt)
    raw = response.content.strip()

    # ===============================
    # PARSE JSON
    # ===============================
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise ValueError(f"Không parse được itinerary JSON: {raw}")
        data = json.loads(match.group())

    if "itinerary" not in data:
        raise ValueError(f"Itinerary JSON thiếu field: {data}")

    itinerary = data["itinerary"]

# Ép itinerary về string an toàn
    if isinstance(itinerary, dict):
      itinerary_text = json.dumps(itinerary, ensure_ascii=False, indent=2)
    else:
     itinerary_text = str(itinerary)

    return {
    "messages": [
        AIMessage(content="Lịch trình hoàn chỉnh:\n\n" + itinerary_text)
    ]
    }
 